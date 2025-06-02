import { useNavigate } from "react-router-dom"
import { Button } from "primereact/button"

const HomePage = () => {
    const navigate = useNavigate()

    return (
        <div className="flex min-h-screen flex-col items-center justify-center bg-transparent pt-12">
            <div className="text-center">
                <h1 className="text-shadow-text-shadow-[0_35px_35px_rgb(0_0_0_/_0.25)] mb-4 text-6xl font-bold text-(--primary-app-color)">
                    Project Manager Assistant
                </h1>
                <p className="mb-8 text-xl text-(--text-color-primary)">
                    Оптимизируйте процессы управления проектами с помощью
                    AI-ассистента
                </p>
                <Button
                    label="View Demo"
                    icon="pi pi-play"
                    size="large"
                    onClick={() => navigate("/demo")}
                    className="border-none px-6 py-3 text-lg transition-all duration-300 hover:bg-[#80ffdb]"
                />
            </div>
        </div>
    )
}

export default HomePage
