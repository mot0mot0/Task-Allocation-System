from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


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
    level: int = Field(ge=1, le=10)


class TaskWithSkills(BaseModel):
    id: str
    title: str
    description: str
    start_date: datetime
    end_date: datetime
    soft_skills: list[SkillLevel] = []
    hard_skills: list[SkillLevel] = []

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ExecutorWithSkills(BaseModel):
    id: str
    name: str
    soft_skills: list[SkillLevel] = []
    hard_skills: list[SkillLevel] = []


class TaskAnalysisRequest(BaseModel):
    id: str
    title: str
    description: str
    start_date: str
    end_date: str
    project_description: str = ""


class ExecutorAnalysisRequest(BaseModel):
    id: str
    name: str
    resume: str


class AllocationRequest(BaseModel):
    tasks: list[TaskWithSkills]
    executors: list[ExecutorWithSkills]


class AllocationResponse(BaseModel):
    allocation: dict[str, str]
