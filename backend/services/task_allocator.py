import logging
import os
import traceback
from datetime import datetime
from src.schemas.requests import TaskWithSkills, ExecutorWithSkills, SkillLevel
from services.normalizer import SkillNormalizer

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

logger = logging.getLogger("task_allocator")
logger.setLevel(logging.INFO)
logger.propagate = False

file_handler = logging.FileHandler(os.path.join(log_dir, "task_allocator.log"))
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class TaskAllocator:
    def __init__(self):
        self.normalizer = SkillNormalizer()

    def calculate_overlap_score(self, task1_start: datetime, task1_end: datetime, 
                              task2_start: datetime, task2_end: datetime) -> float:
        """Рассчитывает степень пересечения сроков двух задач"""
        latest_start = max(task1_start, task2_start)
        earliest_end = min(task1_end, task2_end)
        
        if latest_start >= earliest_end:
            return 0.0
            
        overlap_days = (earliest_end - latest_start).days
        task1_days = (task1_end - task1_start).days
        task2_days = (task2_end - task2_start).days
        
        return overlap_days / max(task1_days, task2_days)

    def calculate_executor_load(self, executor_id: str, allocation: dict[str, str], 
                              tasks: list[TaskWithSkills]) -> tuple[int, float]:
        """Рассчитывает нагрузку на исполнителя:
        - количество текущих задач
        - среднее пересечение сроков"""
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

    def skill_match_score(self, task: TaskWithSkills, executor: ExecutorWithSkills) -> float:
        """Рассчитывает соответствие навыков исполнителя требованиям задачи"""
        try:
            # Нормализуем навыки
            task_soft_skills = self.normalizer.normalize_skills(task.soft_skills)
            task_hard_skills = self.normalizer.normalize_skills(task.hard_skills)
            executor_soft_skills = self.normalizer.normalize_skills(executor.soft_skills)
            executor_hard_skills = self.normalizer.normalize_skills(executor.hard_skills)

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
            logger.error(f"Error calculating skill match score: {str(e)}")
            return 0.0

    def allocate_tasks(self, tasks: list[TaskWithSkills], executors: list[ExecutorWithSkills]) -> dict[str, str]:
        """Распределяет задачи между исполнителями с учетом сроков и нагрузки"""
        if not tasks or not executors:
            return {}

        allocation: dict[str, str] = {}
        logger.info(f"Starting task allocation for {len(tasks)} tasks and {len(executors)} executors")

        # Сортируем задачи по количеству требуемых навыков (сначала более сложные)
        sorted_tasks = sorted(tasks, key=lambda x: len(x.soft_skills) + len(x.hard_skills), reverse=True)

        for task in sorted_tasks:
            best_executor = None
            best_score = 0.0

            for executor in executors:
                # Рассчитываем базовое соответствие по навыкам
                skill_score = self.skill_match_score(task, executor)
                
                # Рассчитываем текущую нагрузку исполнителя
                task_count, avg_overlap = self.calculate_executor_load(
                    executor.id, allocation, tasks
                )
                
                # Корректируем оценку с учетом нагрузки
                load_penalty = 0.0
                if task_count > 0:
                    # Штраф за количество задач
                    load_penalty += 0.1 * task_count
                    # Штраф за пересечение сроков
                    load_penalty += 0.15 * avg_overlap
                
                # Проверяем пересечение сроков с текущими задачами исполнителя
                executor_tasks = [t for t in tasks if allocation.get(t.id) == executor.id]
                overlap_penalty = 0.0
                for existing_task in executor_tasks:
                    overlap = self.calculate_overlap_score(
                        task.start_date, task.end_date,
                        existing_task.start_date, existing_task.end_date
                    )
                    overlap_penalty += overlap
                
                # Итоговая оценка
                final_score = skill_score * (1 - load_penalty) * (1 - overlap_penalty)
                
                if final_score > best_score:
                    best_score = final_score
                    best_executor = executor

            if best_executor and best_score > 0.3:  # Минимальный порог соответствия
                allocation[task.id] = best_executor.id
                logger.info(f"Task {task.id} allocated to executor {best_executor.id} with score {best_score:.2f}")
            else:
                allocation[task.id] = "unassigned"
                logger.warning(f"No suitable executor found for task {task.id}")

        return allocation
