from typing import List, Dict
from src.schemas.requests import TaskWithSkills, ExecutorWithSkills


def skill_match_score(task_skills, executor_skills):
    score = 0
    for t_skill in task_skills:
        for e_skill in executor_skills:
            if t_skill.name == e_skill.name:
                # Чем ближе уровень, тем выше балл, штраф за недобор
                diff = max(0, t_skill.level - e_skill.level)
                score += max(0, 10 - diff)
    return score


def allocate_tasks(
    tasks: List[TaskWithSkills], executors: List[ExecutorWithSkills]
) -> Dict[str, str]:
    allocation = {}
    executor_load = {e.id: 0 for e in executors}
    for task in tasks:
        best_executor = None
        best_score = -1
        for executor in executors:
            score = skill_match_score(task.soft_skills, executor.soft_skills)
            score += skill_match_score(task.hard_skills, executor.hard_skills)
            # Учитываем нагрузку: чем больше задач, тем ниже итоговый балл
            score -= executor_load[executor.id] * 5
            if score > best_score:
                best_score = score
                best_executor = executor.id
        allocation[task.id] = best_executor
        executor_load[best_executor] += 1
    return allocation
