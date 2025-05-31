import React, { useState } from "react"

const Docs: React.FC = () => {
    const [activeSection, setActiveSection] = useState("overview")

    const sections = [
        { id: "overview", title: "Обзор" },
        { id: "features", title: "Возможности" },
        { id: "tech-stack", title: "Технологии" },
        { id: "installation", title: "Установка" },
        { id: "api", title: "API" },
        { id: "architecture", title: "Архитектура" },
        { id: "security", title: "Безопасность" },
        { id: "deployment", title: "Развертывание" },
    ]

    const scrollToSection = (sectionId: string) => {
        setActiveSection(sectionId)
        const element = document.getElementById(sectionId)
        if (element) {
            element.scrollIntoView({ behavior: "smooth" })
        }
    }

    return (
        <div className="min-h-screen bg-gray-50 pt-18">
            <div className="container mx-auto px-4 py-8">
                <h1 className="mb-8 text-4xl font-bold text-[#72efdd]">
                    Документация PM Assistant
                </h1>

                <div className="flex gap-8">
                    {/* Боковая навигация */}
                    <nav className="w-64 flex-shrink-0">
                        <div className="sticky top-18 rounded-lg bg-white p-4 shadow-md">
                            <ul className="space-y-2">
                                {sections.map((section) => (
                                    <li key={section.id}>
                                        <button
                                            onClick={() =>
                                                scrollToSection(section.id)
                                            }
                                            className={`w-full rounded px-4 py-2 text-left transition-colors ${
                                                activeSection === section.id
                                                    ? "text-[#72efdd]"
                                                    : "text-gray-600 hover:bg-gray-100"
                                            }`}
                                        >
                                            {section.title}
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </nav>

                    {/* Основной контент */}
                    <div className="flex-1 space-y-8">
                        {/* Обзор */}
                        <section
                            id="overview"
                            className="rounded-lg bg-white p-6 shadow-md"
                        >
                            <h2 className="mb-4 text-2xl font-semibold text-gray-800">
                                Обзор
                            </h2>
                            <p className="text-gray-600">
                                PM Assistant - это интеллектуальная система
                                распределения задач, которая помогает проектным
                                менеджерам эффективно распределять задачи между
                                исполнителями. Система анализирует навыки
                                исполнителей, их текущую загрузку и историю
                                выполнения задач, чтобы предложить оптимальное
                                распределение задач.
                            </p>
                        </section>

                        {/* Возможности */}
                        <section
                            id="features"
                            className="rounded-lg bg-white p-6 shadow-md"
                        >
                            <h2 className="mb-4 text-2xl font-semibold text-gray-800">
                                Возможности
                            </h2>
                            <ul className="list-inside list-disc space-y-2 text-gray-600">
                                <li>
                                    Анализ навыков и компетенций исполнителей
                                </li>
                                <li>Учет текущей загрузки и доступности</li>
                                <li>Интеллектуальное распределение задач</li>
                                <li>
                                    Отслеживание эффективности распределения
                                </li>
                                <li>
                                    Аналитика и отчеты по распределению задач
                                </li>
                                <li>
                                    Интеграция с системами управления проектами
                                </li>
                                <li>
                                    Автоматическое обновление статусов задач
                                </li>
                            </ul>
                        </section>

                        {/* Технологии */}
                        <section
                            id="tech-stack"
                            className="rounded-lg bg-white p-6 shadow-md"
                        >
                            <h2 className="mb-4 text-2xl font-semibold text-gray-800">
                                Технологии
                            </h2>
                            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                                <div>
                                    <h3 className="mb-2 text-xl font-medium text-gray-700">
                                        Frontend
                                    </h3>
                                    <ul className="list-inside list-disc space-y-1 text-gray-600">
                                        <li>React 18</li>
                                        <li>TypeScript</li>
                                        <li>PrimeReact</li>
                                        <li>Tailwind CSS</li>
                                        <li>React Router</li>
                                    </ul>
                                </div>
                                <div>
                                    <h3 className="mb-2 text-xl font-medium text-gray-700">
                                        Backend
                                    </h3>
                                    <ul className="list-inside list-disc space-y-1 text-gray-600">
                                        <li>Node.js</li>
                                        <li>Express</li>
                                        <li>MongoDB</li>
                                        <li>JWT Authentication</li>
                                        <li>Mongoose</li>
                                    </ul>
                                </div>
                            </div>
                        </section>

                        {/* Установка */}
                        <section
                            id="installation"
                            className="rounded-lg bg-white p-6 shadow-md"
                        >
                            <h2 className="mb-4 text-2xl font-semibold text-gray-800">
                                Установка
                            </h2>
                            <div className="space-y-4">
                                <div>
                                    <h3 className="mb-2 text-xl font-medium text-gray-700">
                                        Требования
                                    </h3>
                                    <ul className="list-inside list-disc space-y-1 text-gray-600">
                                        <li>Node.js 18+</li>
                                        <li>MongoDB 6+</li>
                                        <li>Yarn 1.22+</li>
                                    </ul>
                                </div>
                                <div>
                                    <h3 className="mb-2 text-xl font-medium text-gray-700">
                                        Frontend
                                    </h3>
                                    <pre className="rounded-lg bg-gray-100 p-4 text-sm text-gray-600">
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
                                    <h3 className="mb-2 text-xl font-medium text-gray-700">
                                        Backend
                                    </h3>
                                    <pre className="rounded-lg bg-gray-100 p-4 text-sm text-gray-600">
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

                        {/* API */}
                        <section
                            id="api"
                            className="rounded-lg bg-white p-6 shadow-md"
                        >
                            <h2 className="mb-4 text-2xl font-semibold text-gray-800">
                                API Endpoints
                            </h2>
                            <div className="space-y-4">
                                <div className="border-l-4 border-[#72efdd] pl-4">
                                    <h3 className="text-lg font-medium text-gray-700">
                                        Tasks
                                    </h3>
                                    <ul className="mt-2 space-y-2 text-gray-600">
                                        <li>
                                            GET /api/tasks - Получить все задачи
                                        </li>
                                        <li>
                                            POST /api/tasks - Создать новую
                                            задачу
                                        </li>
                                        <li>
                                            PUT /api/tasks/:id - Обновить задачу
                                        </li>
                                        <li>
                                            DELETE /api/tasks/:id - Удалить
                                            задачу
                                        </li>
                                    </ul>
                                </div>
                                <div className="border-l-4 border-[#72efdd] pl-4">
                                    <h3 className="text-lg font-medium text-gray-700">
                                        Executors
                                    </h3>
                                    <ul className="mt-2 space-y-2 text-gray-600">
                                        <li>
                                            GET /api/executors - Получить всех
                                            исполнителей
                                        </li>
                                        <li>
                                            POST /api/executors - Добавить
                                            нового исполнителя
                                        </li>
                                        <li>
                                            PUT /api/executors/:id - Обновить
                                            данные исполнителя
                                        </li>
                                        <li>
                                            DELETE /api/executors/:id - Удалить
                                            исполнителя
                                        </li>
                                    </ul>
                                </div>
                            </div>
                        </section>

                        {/* Архитектура */}
                        <section
                            id="architecture"
                            className="rounded-lg bg-white p-6 shadow-md"
                        >
                            <h2 className="mb-4 text-2xl font-semibold text-gray-800">
                                Архитектура
                            </h2>
                            <div className="space-y-4 text-gray-600">
                                <p>
                                    Система построена на микросервисной
                                    архитектуре с четким разделением
                                    ответственности между компонентами. Основные
                                    компоненты:
                                </p>
                                <ul className="list-inside list-disc space-y-2">
                                    <li>
                                        Frontend - React приложение с
                                        компонентной архитектурой
                                    </li>
                                    <li>
                                        Backend API - RESTful сервис на Express
                                    </li>
                                    <li>
                                        База данных - MongoDB для хранения
                                        данных
                                    </li>
                                    <li>
                                        Сервис аутентификации - JWT-based
                                        авторизация
                                    </li>
                                </ul>
                            </div>
                        </section>

                        {/* Безопасность */}
                        <section
                            id="security"
                            className="rounded-lg bg-white p-6 shadow-md"
                        >
                            <h2 className="mb-4 text-2xl font-semibold text-gray-800">
                                Безопасность
                            </h2>
                            <div className="space-y-4 text-gray-600">
                                <ul className="list-inside list-disc space-y-2">
                                    <li>JWT аутентификация</li>
                                    <li>Защита от CSRF атак</li>
                                    <li>Валидация входных данных</li>
                                    <li>Шифрование чувствительных данных</li>
                                    <li>Rate limiting для API endpoints</li>
                                </ul>
                            </div>
                        </section>

                        {/* Развертывание */}
                        <section
                            id="deployment"
                            className="rounded-lg bg-white p-6 shadow-md"
                        >
                            <h2 className="mb-4 text-2xl font-semibold text-gray-800">
                                Развертывание
                            </h2>
                            <div className="space-y-4 text-gray-600">
                                <p>
                                    Для развертывания системы рекомендуется
                                    использовать Docker и Docker Compose:
                                </p>
                                <pre className="rounded-lg bg-gray-100 p-4 text-sm">
                                    <code>docker-compose up -d</code>
                                </pre>
                                <p>
                                    Система также может быть развернута на
                                    облачных платформах:
                                </p>
                                <ul className="list-inside list-disc space-y-2">
                                    <li>AWS</li>
                                    <li>Google Cloud Platform</li>
                                    <li>Microsoft Azure</li>
                                </ul>
                            </div>
                        </section>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default Docs
