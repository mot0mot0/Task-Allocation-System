import requests
from src.constants import LLAMA_INTERFACE
from src.schemas.requests import TaskWithSkills, ExecutorWithSkills
from services.llm_interface import LlamaModelInterface

url = "http://localhost:8000/matching/allocate"

test_data = {
    "tasks": [
        {
            "id": "task1",
            "soft_skills": [
                {"name": "communication", "level": 5},
                {"name": "teamwork", "level": 4},
                {"name": "leadership", "level": 3},
            ],
            "hard_skills": [
                {"name": "python", "level": 7},
                {"name": "sql", "level": 6},
                {"name": "docker", "level": 4},
            ],
        },
        {
            "id": "task2",
            "soft_skills": [
                {"name": "leadership", "level": 6},
                {"name": "problem_solving", "level": 5},
            ],
            "hard_skills": [
                {"name": "java", "level": 5},
                {"name": "spring", "level": 4},
            ],
        },
        {
            "id": "task3",
            "soft_skills": [
                {"name": "creativity", "level": 7},
                {"name": "communication", "level": 6},
            ],
            "hard_skills": [
                {"name": "javascript", "level": 8},
                {"name": "react", "level": 7},
            ],
        },
    ],
    "executors": [
        {
            "id": "user1",
            "soft_skills": [
                {"name": "communication", "level": 6},
                {"name": "teamwork", "level": 5},
                {"name": "problem_solving", "level": 4},
            ],
            "hard_skills": [
                {"name": "python", "level": 8},
                {"name": "sql", "level": 5},
                {"name": "docker", "level": 3},
            ],
        },
        {
            "id": "user2",
            "soft_skills": [
                {"name": "leadership", "level": 7},
                {"name": "creativity", "level": 6},
            ],
            "hard_skills": [
                {"name": "java", "level": 6},
                {"name": "spring", "level": 5},
            ],
        },
        {
            "id": "user3",
            "soft_skills": [
                {"name": "teamwork", "level": 8},
                {"name": "problem_solving", "level": 7},
            ],
            "hard_skills": [
                {"name": "javascript", "level": 9},
                {"name": "react", "level": 8},
            ],
        },
    ],
}

tasks = [TaskWithSkills(**t) for t in test_data["tasks"]]
executors = [ExecutorWithSkills(**e) for e in test_data["executors"]]

relationships = LlamaModelInterface.find_skill_relationships(tasks, executors)
print("Skill relationships:", relationships)

response = requests.post(url, json=test_data)
print("Status code:", response.status_code)
print("Response:", response.json())
