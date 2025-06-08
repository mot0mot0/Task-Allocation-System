import logging
from src.schemas.requests import SkillLevel
from assets.skills.synonyms import SKILL_SYNONYMS

logger = logging.getLogger("normalizer")
logger.setLevel(logging.INFO)
logger.propagate = False

class SkillNormalizer:
    def __init__(self):
        self.synonyms = SKILL_SYNONYMS

    def normalize_skill_name(self, skill_name: str) -> str:
        """
        Нормализует название навыка, приводя его к каноническому виду.
        Если навык не найден в словаре синонимов, возвращает оригинальное название.
        """
        skill_name = skill_name.lower().strip()
        
        # Проверяем, является ли название каноническим
        if skill_name in self.synonyms:
            return skill_name
            
        # Ищем среди синонимов
        for normalized_name, synonyms in self.synonyms.items():
            if skill_name in synonyms:
                return normalized_name
                
        return skill_name

    def normalize_skills(self, skills: list[SkillLevel]) -> list[SkillLevel]:
        """
        Нормализует список навыков, объединяя дубликаты и приводя названия к каноническому виду.
        """
        normalized_skills = []
        
        for skill in skills:
            normalized_name = self.normalize_skill_name(skill["name"])
            
            # Если навык уже есть в нормализованном списке, берем максимальный уровень
            if normalized_name in normalized_skills:
                normalized_skills[normalized_name] = max(
                    normalized_skills[normalized_name],
                    skill["level"]
                )
            else:
                normalized_skills.append({
                    "name": normalized_name,
                    "level": skill["level"]
                })
                
        return normalized_skills

    def normalize_task_skills(self, task_skills: list[SkillLevel]) -> list[SkillLevel]:
        """
        Нормализует навыки задачи.
        """
        return self.normalize_skills(task_skills)

    def normalize_executor_skills(self, executor_skills: list[SkillLevel]) -> list[SkillLevel]:
        """
        Нормализует навыки исполнителя.
        """
        return self.normalize_skills(executor_skills)