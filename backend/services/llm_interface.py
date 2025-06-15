import json
import logging
from typing import Iterator
from llama_cpp import Llama
import sys
import time
from pathlib import Path
from src.schemas.requests import TaskWithSkills, ExecutorWithSkills
from src.logger import setup_logging

# Настраиваем логирование
setup_logging()

# Получаем логгер для llm_interface
logger = logging.getLogger("llm_interface")

log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

llm_log_file = log_dir / "llm.log"

# Настраиваем логирование
log_formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] [%(name)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

logger.setLevel(logging.INFO)
logger.propagate = False

# Очищаем существующие обработчики
logger.handlers = []

# Добавляем новый обработчик файла
file_handler = logging.FileHandler(llm_log_file, encoding="utf-8", mode="a")
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)


class StreamToLogger:
    def __init__(self, logger, level):
        self.logger = logger
        self.level = level
        self.linebuf = ""

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            if "ERROR" in line or "error" in line.lower():
                self.logger.error(line.rstrip())
            elif (
                "WARNING" in line
                or "warning" in line.lower()
                or "will not be utilized" in line
            ):
                self.logger.warning(line.rstrip())
            else:
                self.logger.info(line.rstrip())

    def flush(self):
        pass


sys.stdout = StreamToLogger(logger, logging.INFO)
sys.stderr = StreamToLogger(logger, logging.ERROR)


class LlamaModelInterface:
    def __init__(self, model_path: str):
        self.__llm = Llama(
            model_path=model_path,
            n_ctx=8192,
            n_threads=6,
            n_batch=512,
            use_mmap=True,
            use_mlock=False,
            logit_bias=None,
            temperature=0.6,
            top_p=0.98,
            stop=["</s>"],
            chat_format="chatml",
            verbose=False,
        )

    def __build_tasks_prompt(self, context: str) -> list[dict[str, str]]:
        system_prompt = """\
                Ты — эксперт в управлении проектами. Всегда отвечай строго в формате JSON и без пояснений.

                Твоя задача:
                - Проанализируй описание задачи в контексте проекта.
                - Определи ключевые навыки, необходимые для её выполнения.
                - Для каждого навыка:
                    - Укажи его тип: "soft" (поведенческие, личностные) или "hard" (технические).
                    - Оцени значимость в диапазоне от 0.1 до 0.9, где:
                        * 0.1-0.3: низкая значимость (навык желателен, но не критичен)
                        * 0.4-0.6: средняя значимость (навык важен для успешного выполнения)
                        * 0.7-0.9: высокая значимость (навык критически необходим)
                    - Будь объективен в оценках:
                        * Если навык упоминается как дополнительный или опциональный - оценивай как низкую значимость (0.1-0.3)
                        * Если навык явно требуется для выполнения основных задач - оценивай как среднюю значимость (0.4-0.6)
                        * Если навык критически важен для успеха задачи или упоминается как обязательное требование - оценивай как высокую значимость (0.7-0.9)
                        * Если навык не упоминается в контексте задачи - не включай его в оценку

                Формат ответа:
                {{
                    "soft": {{
                        "навык_1": значимость,
                        ...
                    }},
                    "hard": {{
                        "навык_1": значимость,
                        ...
                    }}
                }}

                Правила:
                - Не добавляй пояснений или текста вне JSON.
                - Строго следуй структуре JSON, не меняй ключи.
                - Навыки могут быть неочевидны — делай обоснованные предположения.
                - Если нет навыков определённого типа, возвращай пустой объект.
                - Все названия навыков (soft и hard) должны быть только на английском языке.
                - Используй принятые термины, без транслитерации и перевода с русского.
                - Не придумывай собственные названия навыков — используй только существующие общепринятые термины.
                - Будь строг в оценках - не завышай значимость без явных доказательств в тексте.

                Начни после ввода задачи от пользователя.
            """

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Контекст проекта:\n{context}"},
        ]

    def __build_executor_prompt(self) -> list[dict[str, str]]:
        system_prompt = """\
                Ты — эксперт по анализу резюме и навыков. Всегда отвечай строго в формате JSON и без пояснений.

                Твоя задача:
                - Проанализируй предоставленное резюме или описание навыков исполнителя.
                - Определи все выявленные навыки и компетенции.
                - Для каждого навыка:
                    - Укажи его тип: "soft" (поведенческие, личностные) или "hard" (технические).
                    - Оцени уровень владения от 0.1 до 0.9, где:
                        * 0.1-0.3: базовый уровень (знаком с концепцией, может выполнять простые задачи)
                        * 0.4-0.6: средний уровень (имеет практический опыт, может решать типовые задачи)
                        * 0.7-0.9: продвинутый уровень (глубокое понимание, может решать сложные задачи)
                    - Будь объективен в оценках:
                        * Если навык упоминается кратко или без деталей - оценивай как базовый (0.1-0.3)
                        * Если есть примеры использования, но без сложных кейсов - оценивай как средний (0.4-0.6)
                        * Если есть примеры сложных задач и глубокого понимания - оценивай как продвинутый (0.7-0.9)
                        * Если навык не упоминается явно - не включай его в оценку

                Формат ответа:
                {{
                    "soft": {{
                        "навык_1": уровень,
                        ...
                    }},
                    "hard": {{
                        "навык_1": уровень,
                        ...
                    }}
                }}

                Правила:
                - Не добавляй пояснений или текста вне JSON.
                - Строго следуй структуре JSON, не меняй ключи.
                - Все названия навыков должны быть только на английском языке.
                - Используй общепринятые термины без транслитерации.
                - Если навык упоминается несколько раз, оценивай по максимальному уровню.
                - Если нет навыков определённого типа, возвращай пустой объект.
                - Не придумывай навыки, которых нет в тексте.
                - Будь строг в оценках - не завышай их без явных доказательств в тексте.
            """

        return [{"role": "system", "content": system_prompt}]

    def analyze_tasks(
        self, context: str, tasks: list[dict[str, str]]
    ) -> Iterator[dict]:
        start_time = time.time()
        message_base = self.__build_tasks_prompt(context)
        logger.info(f"Start analyzing {len(tasks)} tasks")

        context_tokens = self.__llm.tokenize(context.encode())
        logger.info(f"Context size: {len(context_tokens)} tokens")

        for task in tasks:
            task_start_time = time.time()
            logging.info(f'Processing task #{task["id"]}')

            messages = message_base.copy()
            messages.append(
                {
                    "role": "user",
                    "content": f'Задача: {task["title"]}\nОписание задачи: {task["description"]}',
                }
            )

            try:
                response = self.__llm.create_chat_completion(
                    max_tokens=1536,
                    messages=messages,
                    response_format={
                        "type": "json_object",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "soft": {
                                    "type": "object",
                                    "additionalProperties": {"type": "number"},
                                },
                                "hard": {
                                    "type": "object",
                                    "additionalProperties": {"type": "number"},
                                },
                            },
                            "required": ["soft", "hard"],
                        },
                    },
                )

                usage = response.get("usage", {})
                logger.info(
                    f"prompt_tokens={usage.get('prompt_tokens', 'N/A')}, "
                    f"completion_tokens={usage.get('completion_tokens', 'N/A')}, "
                    f"total_tokens={usage.get('total_tokens', 'N/A')}"
                )

                content = response["choices"][0]["message"]["content"]

                try:
                    parsed = json.loads(content)
                    task_time = time.time() - task_start_time
                    logger.info(
                        f"Task #{task['id']} processed successfully in {task_time:.2f} seconds"
                    )
                    yield {
                        "id": task["id"],
                        "title": task["title"],
                        "assessment": parsed,
                    }

                except json.JSONDecodeError as e:
                    logger.error(
                        f"Parsing JSON error for task  #{task['id']}: {str(e)}"
                    )
                    yield {
                        "id": task["id"],
                        "title": task["title"],
                        "error": "Invalid JSON output",
                        "raw_output": content,
                    }

            except Exception as e:
                logger.error(
                    f"Exception occurred while processing task #{task['id']}: {str(e)}",
                    exc_info=True,
                )
                yield {
                    "id": task["id"],
                    "title": task["title"],
                    "error": f"Exception occurred: {str(e)}",
                }

        total_time = time.time() - start_time
        logger.info(
            f"End of task analysis. Total execution time: {total_time:.2f} seconds"
        )

    def analyze_executor(self, resume_text: str) -> dict:
        start_time = time.time()
        logger.info("Starting executor skills analysis")

        messages = self.__build_executor_prompt()
        messages.append({"role": "user", "content": resume_text})

        try:
            response = self.__llm.create_chat_completion(
                max_tokens=2048,
                messages=messages,
                response_format={
                    "type": "json_object",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "soft": {
                                "type": "object",
                                "additionalProperties": {"type": "number"},
                            },
                            "hard": {
                                "type": "object",
                                "additionalProperties": {"type": "number"},
                            },
                        },
                        "required": ["soft", "hard"],
                    },
                },
            )

            usage = response.get("usage", {})
            logger.info(
                f"prompt_tokens={usage.get('prompt_tokens', 'N/A')}, "
                f"completion_tokens={usage.get('completion_tokens', 'N/A')}, "
                f"total_tokens={usage.get('total_tokens', 'N/A')}"
            )

            content = response["choices"][0]["message"]["content"]
            parsed = json.loads(content)

            total_time = time.time() - start_time
            logger.info(f"Executor analysis completed in {total_time:.2f} seconds")

            return parsed

        except json.JSONDecodeError as e:
            logger.error(f"Parsing JSON error: {str(e)}")
            raise ValueError("Invalid JSON output from model")

        except Exception as e:
            logger.error(f"Exception during executor analysis: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def find_skill_relationships(
        tasks: list[TaskWithSkills], executors: list[ExecutorWithSkills]
    ) -> dict[str, list[str]]:
        relationships = {}
        for task in tasks:
            task_skills = [s.name for s in task.soft_skills + task.hard_skills]
            for executor in executors:
                executor_skills = [
                    s.name for s in executor.soft_skills + executor.hard_skills
                ]
                common_skills = set(task_skills).intersection(set(executor_skills))
                if common_skills:
                    relationships[task.id] = list(common_skills)
        return relationships
