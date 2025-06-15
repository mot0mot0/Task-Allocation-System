import logging
import os
import traceback
from datetime import datetime
from pathlib import Path
from src.schemas.requests import TaskWithSkills, ExecutorWithSkills, SkillLevel
from services.normalizer import SkillNormalizer
from typing import List, Dict, Any
from src.logger import setup_logging

# Настраиваем логирование
setup_logging()

# Получаем логгер для task_allocator
logger = logging.getLogger("task_allocator")

# Настройка логирования
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

logger.setLevel(logging.INFO)
logger.propagate = False

# Очищаем существующие обработчики
logger.handlers = []

# Добавляем новый обработчик файла
file_handler = logging.FileHandler(log_dir / "allocator.log", encoding="utf-8", mode="a")
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class TaskAllocator:
    def __init__(self):
        logger.info("Initializing TaskAllocator")
        self.allocated_tasks = {}
        self.normalizer = SkillNormalizer()

    def calculate_overlap_score(self, task1_start: datetime, task1_end: datetime, 
                              task2_start: datetime, task2_end: datetime) -> float:
        try:
            latest_start = max(task1_start, task2_start)
            earliest_end = min(task1_end, task2_end)
            
            if latest_start >= earliest_end:
                return 0.0
                
            overlap_days = (earliest_end - latest_start).days
            task1_days = (task1_end - task1_start).days
            task2_days = (task2_end - task2_start).days
            
            return overlap_days / max(task1_days, task2_days)
        except Exception as e:
            logger.error(f"Error in calculate_overlap_score: {str(e)}\n{traceback.format_exc()}")
            return 0.0

    def calculate_executor_load(self, executor_id: str, allocation: dict[str, str], 
                              tasks: list[TaskWithSkills]) -> tuple[int, float]:
        try:
            executor_tasks = [t for t in tasks if allocation.get(t.id) == executor_id]
            
            if not executor_tasks:
                return 0, 0.0
                
            task_count = len(executor_tasks)
            
            # Рассчитываем среднее пересечение сроков
            overlap_scores = []
            for i, task1 in enumerate(executor_tasks):
                for task2 in executor_tasks[i+1:]:
                    overlap = self.calculate_overlap_score(
                        task1.start_date, task1.end_date,
                        task2.start_date, task2.end_date
                    )
                    overlap_scores.append(overlap)
                    
            avg_overlap = sum(overlap_scores) / len(overlap_scores) if overlap_scores else 0.0
            
            return task_count, avg_overlap
        except Exception as e:
            logger.error(f"Error in calculate_executor_load: {str(e)}\n{traceback.format_exc()}")
            return 0, 0.0

    def skill_match_score(self, task: TaskWithSkills, executor: ExecutorWithSkills) -> float:
        try:
            # Нормализуем навыки
            task_soft_skills = self.normalizer.normalize_skills(task.soft_skills)
            task_hard_skills = self.normalizer.normalize_skills(task.hard_skills)
            executor_soft_skills = self.normalizer.normalize_skills(executor.soft_skills)
            executor_hard_skills = self.normalizer.normalize_skills(executor.hard_skills)

            logger.debug(f"Normalized skills for task {task.id}: soft={task_soft_skills}, hard={task_hard_skills}")
            logger.debug(f"Normalized skills for executor {executor.id}: soft={executor_soft_skills}, hard={executor_hard_skills}")

            # Рассчитываем соответствие soft skills
            soft_score = 0.0
            if task_soft_skills:
                for task_skill in task_soft_skills:
                    max_match = 0.0
                    for executor_skill in executor_soft_skills:
                        if task_skill["name"] == executor_skill["name"]:
                            match = min(task_skill["level"], executor_skill["level"]) / task_skill["level"]
                            max_match = max(max_match, match)
                    soft_score += max_match
                soft_score /= len(task_soft_skills)

            # Рассчитываем соответствие hard skills
            hard_score = 0.0
            if task_hard_skills:
                for task_skill in task_hard_skills:
                    max_match = 0.0
                    for executor_skill in executor_hard_skills:
                        if task_skill["name"] == executor_skill["name"]:
                            match = min(task_skill["level"], executor_skill["level"]) / task_skill["level"]
                            max_match = max(max_match, match)
                    hard_score += max_match
                hard_score /= len(task_hard_skills)

            # Взвешиваем soft и hard skills
            if task_soft_skills and task_hard_skills:
                return 0.4 * soft_score + 0.6 * hard_score
            elif task_soft_skills:
                return soft_score
            elif task_hard_skills:
                return hard_score
            return 0.0

        except Exception as e:
            logger.error(f"Error calculating skill match score: {str(e)}\n{traceback.format_exc()}")
            return 0.0

    def allocate_tasks(self, tasks: List[TaskWithSkills], executors: List[ExecutorWithSkills]) -> Dict[str, List[TaskWithSkills]]:
        logger.info(f"Starting task allocation for {len(tasks)} tasks among {len(executors)} executors")
        
        try:
            # Создаем словарь для хранения распределенных задач
            allocation = {executor.id: [] for executor in executors}
            
            # Сортируем задачи по сложности (количество навыков)
            sorted_tasks = sorted(
                tasks,
                key=lambda x: len(x.soft_skills) + len(x.hard_skills),
                reverse=True
            )
            
            # Сортируем исполнителей по количеству текущих задач
            def get_executor_load(executor_id: str) -> int:
                return len(self.allocated_tasks.get(executor_id, []))
            
            for task in sorted_tasks:
                logger.info(f"Processing task: {task.id}")
                
                # Сортируем исполнителей по текущей нагрузке
                available_executors = sorted(
                    executors,
                    key=lambda x: get_executor_load(x.id)
                )
                
                # Находим наиболее подходящего исполнителя
                best_executor = self._find_best_executor(task, available_executors)
                
                if best_executor:
                    allocation[best_executor.id].append(task)
                    logger.info(f"Task {task.id} allocated to executor {best_executor.id}")
                else:
                    logger.warning(f"No suitable executor found for task {task.id}")
            
            self.allocated_tasks = allocation
            logger.info("Task allocation completed successfully")
            return allocation
            
        except Exception as e:
            logger.error(f"Error during task allocation: {str(e)}", exc_info=True)
            raise

    def _find_best_executor(self, task: TaskWithSkills, executors: List[ExecutorWithSkills]) -> ExecutorWithSkills:
        try:
            best_score = -1
            best_executor = None
            
            for executor in executors:
                score = self._calculate_fit_score(task, executor)
                logger.debug(f"Executor {executor.id} fit score for task {task.id}: {score}")
                
                if score > best_score:
                    best_score = score
                    best_executor = executor
            
            # Если лучший результат слишком низкий, не назначаем задачу
            if best_score < 0.3:  # Минимальный порог соответствия
                return None
                
            return best_executor
            
        except Exception as e:
            logger.error(f"Error finding best executor: {str(e)}", exc_info=True)
            raise

    def _calculate_fit_score(self, task: TaskWithSkills, executor: ExecutorWithSkills) -> float:
        try:
            # Базовые веса для разных факторов
            skill_weight = 0.5
            load_weight = 0.3
            experience_weight = 0.2
            
            # Оценка по навыкам
            skill_score = self._calculate_skill_match(task, executor)
            
            # Оценка по нагрузке
            load_score = self._calculate_load_score(executor)
            
            # Оценка по опыту
            experience_score = self._calculate_experience_match(task, executor)
            
            # Итоговая оценка
            total_score = (
                skill_score * skill_weight +
                load_score * load_weight +
                experience_score * experience_weight
            )
            
            logger.debug(f"Fit score calculation for executor {executor.id} and task {task.id}: {total_score}")
            return total_score
            
        except Exception as e:
            logger.error(f"Error calculating fit score: {str(e)}", exc_info=True)
            raise

    def _calculate_skill_match(self, task: TaskWithSkills, executor: ExecutorWithSkills) -> float:
        try:
            # Рассчитываем соответствие soft skills
            soft_score = 0.0
            if task.soft_skills:
                for task_skill in task.soft_skills:
                    max_match = 0.0
                    for executor_skill in executor.soft_skills:
                        if task_skill.name == executor_skill.name:
                            match = min(task_skill.level, executor_skill.level) / task_skill.level
                            max_match = max(max_match, match)
                    soft_score += max_match
                soft_score /= len(task.soft_skills)

            # Рассчитываем соответствие hard skills
            hard_score = 0.0
            if task.hard_skills:
                for task_skill in task.hard_skills:
                    max_match = 0.0
                    for executor_skill in executor.hard_skills:
                        if task_skill.name == executor_skill.name:
                            match = min(task_skill.level, executor_skill.level) / task_skill.level
                            max_match = max(max_match, match)
                    hard_score += max_match
                hard_score /= len(task.hard_skills)

            # Взвешиваем soft и hard skills
            if task.soft_skills and task.hard_skills:
                return 0.4 * soft_score + 0.6 * hard_score
            elif task.soft_skills:
                return soft_score
            elif task.hard_skills:
                return hard_score
            return 0.0
            
        except Exception as e:
            logger.error(f"Error calculating skill match: {str(e)}", exc_info=True)
            raise

    def _calculate_load_score(self, executor: ExecutorWithSkills) -> float:
        try:
            current_tasks = len(self.allocated_tasks.get(executor.id, []))
            max_tasks = 5  # Можно сделать настраиваемым параметром
            
            # Чем меньше текущих задач, тем выше оценка
            return max(0.0, 1.0 - (current_tasks / max_tasks))
            
        except Exception as e:
            logger.error(f"Error calculating load score: {str(e)}", exc_info=True)
            raise

    def _calculate_experience_match(self, task: TaskWithSkills, executor: ExecutorWithSkills) -> float:
        try:
            # Рассчитываем средний уровень навыков исполнителя
            executor_skill_levels = [
                skill.level for skill in executor.soft_skills + executor.hard_skills
            ]
            if not executor_skill_levels:
                return 0.5  # Базовый уровень, если нет навыков
                
            avg_executor_level = sum(executor_skill_levels) / len(executor_skill_levels)
            
            # Рассчитываем средний требуемый уровень навыков для задачи
            task_skill_levels = [
                skill.level for skill in task.soft_skills + task.hard_skills
            ]
            if not task_skill_levels:
                return 1.0  # Если нет требований, считаем что подходит
                
            avg_task_level = sum(task_skill_levels) / len(task_skill_levels)
            
            # Нормализуем разницу уровней
            return max(0.0, 1.0 - abs(avg_executor_level - avg_task_level) / 10)
            
        except Exception as e:
            logger.error(f"Error calculating experience match: {str(e)}", exc_info=True)
            raise
