from pydantic import BaseModel, EmailStr


class Task(BaseModel):
    id: str
    title: str
    description: str


class TasksData(BaseModel):
    project_description: str
    task_list: list[Task]


class ExecutorData(BaseModel):
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
