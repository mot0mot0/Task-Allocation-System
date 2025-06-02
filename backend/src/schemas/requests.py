from typing import List, Dict
from pydantic import BaseModel, EmailStr


class Task(BaseModel):
    id: str
    title: str
    description: str
    deadline: str


class TasksData(BaseModel):
    project_description: str
    task_list: list[Task]


class ExecutorData(BaseModel):
    id: str
    name: str
    resume: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: str = "user"  # user или admin


class SingleTaskData(BaseModel):
    id: str
    title: str
    description: str
    project_description: str


class SkillLevel(BaseModel):
    name: str
    level: int


class TaskWithSkills(BaseModel):
    id: str
    soft_skills: List[SkillLevel]
    hard_skills: List[SkillLevel]


class ExecutorWithSkills(BaseModel):
    id: str
    soft_skills: List[SkillLevel]
    hard_skills: List[SkillLevel]


class AllocationRequest(BaseModel):
    tasks: List[TaskWithSkills]
    executors: List[ExecutorWithSkills]
