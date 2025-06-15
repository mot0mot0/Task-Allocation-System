import { useState } from "react"
import CodeBlock from "../../../components/CodeBlock"

const DocsPage = () => {
    const [activeSection, setActiveSection] = useState("overview")

    const sections = [
        { id: "overview", title: "Обзор" },
        { id: "installation", title: "Установка" },
        { id: "start", title: "Запуск" },
        { id: "logs", title: "Логирование" },
        { id: "api", title: "Интеграция" },
        { id: "security", title: "Безопасность" },
    ]

    const scrollToSection = (sectionId: string) => {
        setActiveSection(sectionId)
        const element = document.getElementById(sectionId)
        if (element) {
            const headerOffset = 88
            const elementPosition = element.getBoundingClientRect().top
            const offsetPosition =
                elementPosition + window.scrollY - headerOffset

            window.scrollTo({
                top: offsetPosition,
                behavior: "smooth",
            })
        }
    }

    return (
        <div className="mt-22 mb-8 min-h-screen w-full max-w-[1064px] bg-transparent px-5">
            <div className="mx-auto">
                <div className="flex gap-8">
                    <nav className="w-64 flex-shrink-0">
                        <div className="sticky top-22 rounded-lg bg-(--bg-transparent) p-4 shadow-md">
                            <ul className="space-y-2">
                                {sections.map((section) => (
                                    <li key={section.id}>
                                        <button
                                            onClick={() =>
                                                scrollToSection(section.id)
                                            }
                                            className={`w-full rounded px-4 py-2 text-left transition-colors ${
                                                activeSection === section.id
                                                    ? "text-(--primary-app-color)"
                                                    : "text-(--text-color-primary) hover:bg-(--bg-transparent-hover)"
                                            }`}
                                        >
                                            {section.title}
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </nav>

                    <div className="flex flex-1 flex-col gap-y-8">
                        <section
                            id="overview"
                            className="flex flex-col gap-4 rounded-lg bg-(--bg-semi-transparent) p-6 shadow-md"
                        >
                            <h2 className="text-2xl font-semibold text-(--text-color-primary)">
                                Обзор
                            </h2>
                            <p className="text-(--text-color-primary)">
                                PM Assistant - это интеллектуальная система
                                распределения задач, которая помогает проектным
                                менеджерам эффективно распределять задачи между
                                исполнителями. Система анализирует навыки
                                исполнителей на основе их резюме, и распределяет
                                задачи между исполнителями, в соответствии с их
                                компетенциями.
                            </p>
                        </section>

                        <section
                            id="installation"
                            className="flex flex-col gap-4 rounded-lg bg-(--bg-semi-transparent) p-6 shadow-md"
                        >
                            <h2 className=" text-2xl font-semibold">
                                Установка
                            </h2>
                            <div className="space-y-6">
                                <div>
                                    <h3 className=" mb-4 text-xl font-medium">
                                        Скачивание сборки
                                    </h3>
                                    <p className="mb-4">
                                        Для установки PM Assistant вы можете скачать готовую сборку системы. Сборка включает в себя все необходимые компоненты и зависимости.
                                    </p>
                                    <a
                                        href="http://localhost:8000/builds/pm_assistant_latest.zip"
                                        className="inline-flex items-center gap-2 rounded-lg bg-(--primary-app-color) px-4 py-2 text-[#334155] transition-all duration-300 hover:bg-[#72efddcc]"
                                    >
                                        <i className="pi pi-download" />
                                        Скачать последнюю версию
                                    </a>
                                </div>

                                <div>
                                    <h3 className=" mb-4 text-xl font-medium">
                                        Запуск системы
                                    </h3>
                                    <p className="mb-4">
                                        После скачивания сборки, распакуйте архив и запустите систему через командную строку:
                                    </p>
                                    <div className="space-y-4">
                                        <div>
                                            <h4 className="mb-2 text-lg font-medium">
                                                Распаковка архива
                                            </h4>
                                            <CodeBlock code="unzip pm_assistant_latest.zip" />
                                        </div>
                                        <div>
                                            <h4 className="mb-2 text-lg font-medium">
                                                Запуск системы
                                            </h4>
                                            <CodeBlock code="cd pm_assistant\npm_assistant.exe" />
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>

                        <section
                            id="start"
                            className="flex flex-col gap-4 rounded-lg bg-(--bg-semi-transparent) p-6 shadow-md"
                        >
                            <h2 className=" text-2xl font-semibold">
                                Запуск системы
                            </h2>
                            <div className="space-y-6">
                                <div>
                                    <h3 className=" mb-4 text-xl font-medium">
                                        Автоматическая настройка
                                    </h3>
                                    <p className="mb-4">
                                        При первом запуске система автоматически выполнит все необходимые настройки:
                                    </p>
                                    <ul className="list-inside list-disc space-y-2">
                                        <li>
                                            <span className="font-medium">Установка PocketBase</span> - автоматическая загрузка и настройка базы данных
                                        </li>
                                        <li>
                                            <span className="font-medium">Установка LLM</span> - загрузка и настройка языковой модели для анализа задач
                                        </li>
                                        <li>
                                            <span className="font-medium">Настройка портов</span> - автоматическое определение и назначение свободных портов
                                        </li>
                                    </ul>
                                </div>

                                <div>
                                    <h3 className=" mb-4 text-xl font-medium">
                                        Доступ к компонентам
                                    </h3>
                                    <p className="mb-4">
                                        После запуска система предоставляет доступ к следующим компонентам:
                                    </p>
                                    <div className="space-y-4">
                                        <h4 className="mb-2 text-lg font-medium text-white">
                                            Веб-интерфейс
                                        </h4>
                                        <CodeBlock code="http://localhost:3000" />
                                        <p className="mt-2 text-sm text-gray-400">
                                            Основной интерфейс системы для работы с задачами и исполнителями
                                        </p>
                                        <h4 className="mb-2 text-lg font-medium text-white">
                                            API
                                        </h4>
                                        <CodeBlock code="http://localhost:8000" />
                                        <p className="mt-2 text-sm text-gray-400">
                                            REST API для интеграции с другими системами
                                        </p>
                                        <h4 className="mb-2 text-lg font-medium text-white">
                                            PocketBase
                                        </h4>
                                        <CodeBlock code="http://localhost:8090" />
                                        <p className="mt-2 text-sm text-gray-400">
                                            Административный интерфейс базы данных
                                        </p>
                                    </div>
                                </div>

                                <div>
                                    <h3 className=" mb-4 text-xl font-medium">
                                        Первый вход
                                    </h3>
                                    <p className=" mb-4">
                                        При первом запуске система автоматически создаст учетную запись администратора:
                                    </p>
                                    <CodeBlock code='Email: admin@example.com
Password: admin123' />
                                    <p className="mt-4 text-sm text-(--text-color-secondary)">
                                        Рекомендуется сменить пароль администратора после первого входа в систему.
                                    </p>
                                </div>
                            </div>
                        </section>

                        <section
                            id="logs"
                            className="flex flex-col gap-4 rounded-lg bg-(--bg-semi-transparent) p-6 shadow-md"
                        >
                            <h2 className=" text-2xl font-semibold">
                                Логирование
                            </h2>
                            <div className="space-y-6">
                                <div>
                                    <h3 className=" mb-4 text-xl font-medium">
                                        Типы логов
                                    </h3>
                                    <ul className=" list-inside list-disc space-y-2">
                                        <li>
                                            <span className="font-medium">backend.log</span> - логи основного бэкенда
                                        </li>
                                        <li>
                                            <span className="font-medium">llm.log</span> - логи работы с языковой моделью
                                        </li>
                                        <li>
                                            <span className="font-medium">allocator.log</span> - логи процесса распределения задач
                                        </li>
                                        <li>
                                            <span className="font-medium">matching.log</span> - логи маршрутизатора распределения
                                        </li>
                                        <li>
                                            <span className="font-medium">startup.log</span> - логи запуска системы
                                        </li>
                                    </ul>
                                </div>

                                <div>
                                    <h3 className="mb-4 text-xl font-medium">
                                        Просмотр логов
                                    </h3>
                                    <p className=" mb-4">
                                        Для просмотра логов используйте CLI утилиту в директории backend:
                                    </p>
                                    <div className="space-y-4">
                                        <div>
                                            <h4 className=" mb-2 text-lg font-medium">
                                                Просмотр всех логов
                                            </h4>
                                            <CodeBlock code="python cli/logs.py" />
                                        </div>
                                        <div>
                                            <h4 className=" mb-2 text-lg font-medium">
                                                Просмотр конкретного лога
                                            </h4>
                                            <CodeBlock code="python cli/logs.py --type allocator" />
                                        </div>
                                        <div>
                                            <h4 className=" mb-2 text-lg font-medium">
                                                Последние N строк
                                            </h4>
                                            <CodeBlock code="python cli/logs.py --tail 10" />
                                        </div>
                                        <div>
                                            <h4 className=" mb-2 text-lg font-medium">
                                                Логи за последние N часов
                                            </h4>
                                            <CodeBlock code="python cli/logs.py --since 2" />
                                        </div>
                                    </div>
                                </div>

                                <div>
                                    <h3 className=" mb-4 text-xl font-medium">
                                        Формат логов
                                    </h3>
                                    <p className=" mb-4">
                                        Каждая запись в логе имеет следующий формат:
                                    </p>
                                    <CodeBlock code="YYYY-MM-DD HH:MM:SS - logger_name - LEVEL - message" />
                                    <ul className=" mt-4 list-inside list-disc space-y-2">
                                        <li>
                                            <span className="font-medium">YYYY-MM-DD HH:MM:SS</span> - дата и время события
                                        </li>
                                        <li>
                                            <span className="font-medium">logger_name</span> - имя логгера (компонент системы)
                                        </li>
                                        <li>
                                            <span className="font-medium">LEVEL</span> - уровень важности (INFO, WARNING, ERROR)
                                        </li>
                                        <li>
                                            <span className="font-medium">message</span> - сообщение о событии
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </section>

                        <section
                            id="api"
                            className="flex flex-col gap-4 rounded-lg bg-(--bg-semi-transparent) p-6 shadow-md"
                        >
                            <h2 className=" mb-4 text-2xl font-semibold">
                                API-интеграция
                            </h2>
                            <p className=" mb-4">
                                Вы можете интегрировать инструменты PM Assistant в собственные приложения при помощи REST API. API предоставляет доступ ко всем основным функциям системы: аутентификации пользователей, анализу задач и исполнителей, распределению задач и управлению сборками. Все запросы к API должны содержать JWT токен в заголовке Authorization для аутентификации, кроме эндпоинтов инициализации системы и входа.
                            </p>
                            <div className="space-y-8">
                                <div>
                                    <h3 className=" mb-4 text-xl font-medium">
                                        Аутентификация
                                    </h3>
                                    <div className="space-y-6">
                                        <div className="border-l-4 border-(--primary-app-color) pl-4">
                                            <h4 className="text-lg font-medium">
                                                Инициализация системы
                                            </h4>
                                            <ul className="mt-2 space-y-2">
                                                <li>
                                                    <span className="inline-block rounded bg-green-100 px-2 py-1 text-xs font-semibold text-green-800">
                                                        POST
                                                    </span>
                                                    <span className="ml-2">
                                                        /auth/init
                                                    </span>
                                                    <p className="mt-1 text-sm text-(--text-color-secondary)">
                                                        Создание первого администратора системы. Возвращает токен и данные пользователя.
                                                    </p>
                                                </li>
                                            </ul>
                                        </div>
                                        <div className="border-l-4 border-(--primary-app-color) pl-4">
                                            <h4 className="text-lg font-medium">
                                                Регистрация пользователя
                                            </h4>
                                            <ul className="mt-2 space-y-2">
                                                <li>
                                                    <span className="inline-block rounded bg-green-100 px-2 py-1 text-xs font-semibold text-green-800">
                                                        POST
                                                    </span>
                                                    <span className="ml-2">
                                                        /auth/register
                                                    </span>
                                                    <p className="mt-1 text-sm text-(--text-color-secondary)">
                                                        Создание нового пользователя (только для администраторов). Возвращает токен и данные пользователя.
                                                    </p>
                                                </li>
                                            </ul>
                                        </div>
                                        <div className="border-l-4 border-(--primary-app-color) pl-4">
                                            <h4 className="text-lg font-medium">
                                                Вход в систему
                                            </h4>
                                            <ul className="mt-2 space-y-2">
                                                <li>
                                                    <span className="inline-block rounded bg-green-100 px-2 py-1 text-xs font-semibold text-green-800">
                                                        POST
                                                    </span>
                                                    <span className="ml-2">
                                                        /auth/login
                                                    </span>
                                                    <p className="mt-1 text-sm text-(--text-color-secondary)">
                                                        Аутентификация пользователя. Возвращает токен и данные пользователя.
                                                    </p>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>

                                <div>
                                    <h3 className=" mb-4 text-xl font-medium">
                                        Анализ задач и исполнителей
                                    </h3>
                                    <div className="space-y-6">
                                        <div className="border-l-4 border-(--primary-app-color) pl-4">
                                            <h4 className="text-lg font-medium">
                                                Анализ списка задач
                                            </h4>
                                            <ul className="mt-2 space-y-2">
                                                <li>
                                                    <span className="inline-block rounded bg-green-100 px-2 py-1 text-xs font-semibold text-green-800">
                                                        POST
                                                    </span>
                                                    <span className="ml-2">
                                                        /analyzer/tasks
                                                    </span>
                                                    <p className="mt-1 text-sm text-(--text-color-secondary)">
                                                        Анализ списка задач и их требований. Возвращает оценку необходимых навыков для каждой задачи.
                                                    </p>
                                                </li>
                                            </ul>
                                        </div>
                                        <div className="border-l-4 border-(--primary-app-color) pl-4">
                                            <h4 className="text-lg font-medium">
                                                Анализ одной задачи
                                            </h4>
                                            <ul className="mt-2 space-y-2">
                                                <li>
                                                    <span className="inline-block rounded bg-green-100 px-2 py-1 text-xs font-semibold text-green-800">
                                                        POST
                                                    </span>
                                                    <span className="ml-2">
                                                        /analyzer/task
                                                    </span>
                                                    <p className="mt-1 text-sm text-(--text-color-secondary)">
                                                        Анализ отдельной задачи с учетом сроков выполнения. Возвращает оценку необходимых навыков.
                                                    </p>
                                                </li>
                                            </ul>
                                        </div>
                                        <div className="border-l-4 border-(--primary-app-color) pl-4">
                                            <h4 className="text-lg font-medium">
                                                Анализ исполнителя
                                            </h4>
                                            <ul className="mt-2 space-y-2">
                                                <li>
                                                    <span className="inline-block rounded bg-green-100 px-2 py-1 text-xs font-semibold text-green-800">
                                                        POST
                                                    </span>
                                                    <span className="ml-2">
                                                        /analyzer/executor
                                                    </span>
                                                    <p className="mt-1 text-sm text-(--text-color-secondary)">
                                                        Анализ резюме исполнителя. Возвращает оценку soft и hard навыков.
                                                    </p>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>

                                <div>
                                    <h3 className=" mb-4 text-xl font-medium">
                                        Распределение задач
                                    </h3>
                                    <div className="space-y-6">
                                        <div className="border-l-4 border-(--primary-app-color) pl-4">
                                            <h4 className="text-lg font-medium">
                                                Распределение задач
                                            </h4>
                                            <ul className="mt-2 space-y-2">
                                                <li>
                                                    <span className="inline-block rounded bg-green-100 px-2 py-1 text-xs font-semibold text-green-800">
                                                        POST
                                                    </span>
                                                    <span className="ml-2">
                                                        /allocate
                                                    </span>
                                                    <p className="mt-1 text-sm text-(--text-color-secondary)">
                                                        Распределение списка задач между исполнителями на основе их навыков и доступности.
                                                    </p>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>

                                <div>
                                    <h3 className=" mb-4 text-xl font-medium">
                                        Сборки системы
                                    </h3>
                                    <div className="space-y-6">
                                        <div className="border-l-4 border-(--primary-app-color) pl-4">
                                            <h4 className="text-lg font-medium">
                                                Список сборок
                                            </h4>
                                            <ul className="mt-2 space-y-2">
                                                <li>
                                                    <span className="inline-block rounded bg-blue-100 px-2 py-1 text-xs font-semibold text-blue-800">
                                                        GET
                                                    </span>
                                                    <span className="ml-2">
                                                        /builds
                                                    </span>
                                                    <p className="mt-1 text-sm text-(--text-color-secondary)">
                                                        Получение списка доступных сборок системы.
                                                    </p>
                                                </li>
                                            </ul>
                                        </div>
                                        <div className="border-l-4 border-(--primary-app-color) pl-4">
                                            <h4 className="text-lg font-medium">
                                                Скачивание сборки
                                            </h4>
                                            <ul className="mt-2 space-y-2">
                                                <li>
                                                    <span className="inline-block rounded bg-blue-100 px-2 py-1 text-xs font-semibold text-blue-800">
                                                        GET
                                                    </span>
                                                    <span className="ml-2">
                                                        /builds/{'{build_name}'}
                                                    </span>
                                                    <p className="mt-1 text-sm text-(--text-color-secondary)">
                                                        Скачивание конкретной сборки системы по её имени.
                                                    </p>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </section>

                        <section
                            id="security"
                            className="flex flex-col gap-4 rounded-lg bg-(--bg-semi-transparent) p-6 shadow-md"
                        >
                            <h2 className=" text-2xl font-semibold">
                                Безопасность
                            </h2>
                            <p className="">
                                Система разворачивается полностью в вашей
                                локальной сети, что исключает возможность взлома
                                системы. Тем не менее, если вам потребуется
                                использовать систему в глобальной сети, для
                                защиты от взлома, система использует JWT
                                аутентификацию и защиту от CSRF атак.
                            </p>
                            <div className=" space-y-4">
                                <ul className="list-inside list-disc space-y-2">
                                    <li>JWT аутентификация</li>
                                    <li>Защита от CSRF атак</li>
                                    <li>Валидация входных данных</li>
                                    <li>Шифрование чувствительных данных</li>
                                </ul>
                            </div>
                        </section>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default DocsPage
