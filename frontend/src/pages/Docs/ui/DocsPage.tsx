import { useState } from "react"

const DocsPage = () => {
    const [activeSection, setActiveSection] = useState("overview")

    const sections = [
        { id: "overview", title: "Обзор" },
        { id: "installation", title: "Установка" },
        { id: "start", title: "Запуск" },
        { id: "api", title: "Интеграция" },
        { id: "security", title: "Безопасность" },
    ]

    const scrollToSection = (sectionId: string) => {
        setActiveSection(sectionId)
        const element = document.getElementById(sectionId)
        if (element) {
            const headerOffset = 88 // Примерный отступ для mt-22 (5.5rem * 16px)
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
                            <h2 className="(--text-color-primary) text-2xl font-semibold">
                                Установка
                            </h2>
                            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                                <div>
                                    <h3 className="(--text-color-primary) mb-2 text-xl font-medium">
                                        Frontend
                                    </h3>
                                    <ul className="(--text-color-primary) list-inside list-disc space-y-1">
                                        <li>React 18</li>
                                        <li>TypeScript</li>
                                        <li>PrimeReact</li>
                                        <li>Tailwind CSS</li>
                                        <li>React Router</li>
                                    </ul>
                                </div>
                                <div>
                                    <h3 className="(--text-color-primary) mb-2 text-xl font-medium">
                                        Backend
                                    </h3>
                                    <ul className="(--text-color-primary) list-inside list-disc space-y-1">
                                        <li>Node.js</li>
                                        <li>Express</li>
                                        <li>MongoDB</li>
                                        <li>JWT Authentication</li>
                                        <li>Mongoose</li>
                                    </ul>
                                </div>
                            </div>
                        </section>

                        <section
                            id="start"
                            className="flex flex-col gap-4 rounded-lg bg-(--bg-semi-transparent) p-6 shadow-md"
                        >
                            <h2 className="(--text-color-primary) text-2xl font-semibold">
                                Запуск
                            </h2>
                            <div className="space-y-4">
                                <div>
                                    <h3 className="(--text-color-primary) mb-2 text-xl font-medium">
                                        Требования
                                    </h3>
                                    <ul className="(--text-color-primary) list-inside list-disc space-y-1">
                                        <li>Node.js 18+</li>
                                        <li>MongoDB 6+</li>
                                        <li>Yarn 1.22+</li>
                                    </ul>
                                </div>
                                <div>
                                    <h3 className="(--text-color-primary) mb-2 text-xl font-medium">
                                        Frontend
                                    </h3>
                                    <pre className="(--text-color-primary) rounded-lg bg-gray-100 p-4 text-sm">
                                        <code>
                                            cd frontend
                                            <br />
                                            yarn install
                                            <br />
                                            yarn dev
                                        </code>
                                    </pre>
                                </div>
                                <div>
                                    <h3 className="(--text-color-primary) mb-2 text-xl font-medium">
                                        Backend
                                    </h3>
                                    <pre className="(--text-color-primary) rounded-lg bg-gray-100 p-4 text-sm">
                                        <code>
                                            cd backend
                                            <br />
                                            yarn install
                                            <br />
                                            yarn dev
                                        </code>
                                    </pre>
                                </div>
                            </div>
                        </section>

                        <section
                            id="api"
                            className="flex flex-col gap-4 rounded-lg bg-(--bg-semi-transparent) p-6 shadow-md"
                        >
                            <h2 className="(--text-color-primary) mb-4 text-2xl font-semibold">
                                API-итнеграция
                            </h2>
                            <div className="space-y-8">
                                <div>
                                    <h3 className="(--text-color-primary) mb-4 text-xl font-medium">
                                        Нативный интерфейс
                                    </h3>
                                    <p className="(--text-color-primary) mb-4">
                                        Система предоставляет удобный
                                        веб-интерфейс для работы с задачами и
                                        исполнителями. Через интерфейс вы
                                        можете:
                                    </p>
                                    <ul className="(--text-color-primary) list-inside list-disc space-y-2">
                                        <li>Создавать и управлять задачами</li>
                                        <li>
                                            Добавлять и редактировать
                                            исполнителей
                                        </li>
                                        <li>
                                            Анализировать навыки исполнителей
                                        </li>
                                        <li>
                                            Анализировать сложность и требуемые
                                            компетенции задач и компетенции,
                                            необходимые для их выполнения
                                        </li>
                                        <li>
                                            Получать рекомендации по
                                            распределению задач
                                        </li>
                                    </ul>
                                </div>

                                <div>
                                    <h3 className="(--text-color-primary) mb-4 text-xl font-medium">
                                        API интеграция
                                    </h3>
                                    <p className="(--text-color-primary) mb-4">
                                        Для автоматизации процессов и интеграции
                                        с другими системами доступны следующие
                                        API endpoints:
                                    </p>
                                    <div className="space-y-6">
                                        <div className="border-l-4 border-(--primary-app-color) pl-4">
                                            <h4 className="(--text-color-primary) text-lg font-medium">
                                                Анализ задач
                                            </h4>
                                            <ul className="(--text-color-primary) mt-2 space-y-2">
                                                <li>
                                                    <span className="inline-block rounded bg-green-100 px-2 py-1 text-xs font-semibold text-green-800">
                                                        POST
                                                    </span>
                                                    <span className="ml-2">
                                                        /analyze/tasks
                                                    </span>
                                                    <p className="mt-1 text-sm text-(--text-color-secondary)">
                                                        Анализ списка задач и их
                                                        требований. Возвращает
                                                        оценку необходимых
                                                        навыков для каждой
                                                        задачи.
                                                    </p>
                                                </li>
                                            </ul>
                                        </div>
                                        <div className="border-l-4 border-(--primary-app-color) pl-4">
                                            <h4 className="(--text-color-primary) text-lg font-medium">
                                                Анализ исполнителей
                                            </h4>
                                            <ul className="(--text-color-primary) mt-2 space-y-2">
                                                <li>
                                                    <span className="inline-block rounded bg-green-100 px-2 py-1 text-xs font-semibold text-green-800">
                                                        POST
                                                    </span>
                                                    <span className="ml-2">
                                                        /analyze/executor
                                                    </span>
                                                    <p className="mt-1 text-sm text-(--text-color-secondary)">
                                                        Анализ резюме
                                                        исполнителя. Возвращает
                                                        оценку soft и hard
                                                        навыков.
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
                            <h2 className="(--text-color-primary) text-2xl font-semibold">
                                Безопасность
                            </h2>
                            <p className="(--text-color-primary)">
                                Система разворачивается полностью в вашей
                                локальной сети, что исключает возможность взлома
                                системы. Тем не менее, если вам потребуется
                                использовать систему в глобальной сети, для
                                защиты от взлома, система использует JWT
                                аутентификацию и защиту от CSRF атак.
                            </p>
                            <div className="(--text-color-primary) space-y-4">
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
