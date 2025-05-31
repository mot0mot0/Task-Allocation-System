import { useNavigate } from "react-router-dom"
import { Button } from "primereact/button"

const Home = () => {
    const navigate = useNavigate()

    return (
        <div className="flex min-h-screen flex-col items-center justify-center bg-[#f8fafc] pt-12">
            <div className="text-center">
                <h1 className="mb-4 text-6xl font-bold text-[#72efdd]">
                    Project Manager Assistant
                </h1>
                <p className="mb-8 text-xl text-[#64748b]">
                    Оптимизируйте процессы управления проектами с помощью
                    AI-ассистента
                </p>
                <Button
                    label="View Demo"
                    icon="pi pi-play"
                    size="large"
                    onClick={() => navigate("/demo")}
                    className="border-none bg-[#72efdd] px-6 py-3 text-lg text-[#334155] transition-all duration-300 hover:bg-[#80ffdb]"
                />
            </div>
        </div>
    )
}

export default Home
