import { useState, useRef } from "react"
import type { ChangeEvent } from "react"
import { Card } from "primereact/card"
import { InputText } from "primereact/inputtext"
import { Button } from "primereact/button"
import { Dialog } from "primereact/dialog"
import { Tag } from "primereact/tag"
import { ProgressSpinner } from "primereact/progressspinner"
import { InputTextarea } from "primereact/inputtextarea"
import { FileUpload } from "primereact/fileupload"
import type { FileUploadUploadEvent } from "primereact/fileupload"
import axios from "axios"

interface Executor {
    id: number
    name: string
    resume: string
}

interface Task {
    id: number
    title: string
    description: string
}

const Demo = () => {
    const [executors, setExecutors] = useState<Executor[]>([])
    const [tasks, setTasks] = useState<Task[]>([])
    const [showDialog, setShowDialog] = useState(false)
    const [isLoading, setIsLoading] = useState(false)
    const [projectContext, setProjectContext] = useState("")
    const [newTask, setNewTask] = useState({ title: "", description: "" })
    const [newExecutor, setNewExecutor] = useState({ name: "", resume: "" })
    const fileUploadRef = useRef<FileUpload>(null)

    const handleFileUpload = async (event: FileUploadUploadEvent) => {
        const file = event.files[0]
        if (file) {
            const text = await file.text()
            setNewExecutor((prev) => ({ ...prev, resume: text }))
        }
    }

    const handleAddExecutor = async () => {
        if (!newExecutor.name || !newExecutor.resume) return

        setIsLoading(true)
        try {
            // Здесь будет запрос к бэкенду
            const response = await axios.post("/api/executors", newExecutor)
            setExecutors([...executors, response.data])
            setNewExecutor({ name: "", resume: "" })
            setShowDialog(false)
        } catch (error) {
            console.error("Error adding executor:", error)
        } finally {
            setIsLoading(false)
        }
    }

    const handleAddTask = () => {
        if (!newTask.title || !newTask.description) return

        setTasks([
            ...tasks,
            {
                id: tasks.length + 1,
                title: newTask.title,
                description: newTask.description,
            },
        ])
        setNewTask({ title: "", description: "" })
    }

    return (
        <div className="min-h-screen bg-[#f8fafc] p-6 pt-24">
            {/* Блок исполнителей */}
            <Card className="mb-6 shadow-sm">
                <div className="mb-4 flex items-center justify-between">
                    <div className="flex flex-wrap gap-2">
                        {executors.map((executor) => (
                            <Tag
                                key={executor.id}
                                value={executor.name}
                                className="bg-[#72efdd] px-3 py-2 text-lg text-[#334155]"
                            />
                        ))}
                    </div>
                    <Button
                        label="Добавить исполнителя"
                        icon="pi pi-plus"
                        onClick={() => setShowDialog(true)}
                        disabled={isLoading}
                        className="!border-none !bg-[#72efdd] !text-[#334155] transition-all duration-300 hover:!bg-[#72efdd]/80"
                    />
                </div>
            </Card>

            {/* Диалог добавления исполнителя */}
            <Dialog
                visible={showDialog}
                onHide={() => !isLoading && setShowDialog(false)}
                header="Добавить исполнителя"
                className="w-2/3"
            >
                <div className="flex flex-col gap-4">
                    <div className="field">
                        <label
                            htmlFor="name"
                            className="mb-2 block text-[#334155]"
                        >
                            Имя исполнителя
                        </label>
                        <InputText
                            id="name"
                            value={newExecutor.name}
                            onChange={(e: ChangeEvent<HTMLInputElement>) =>
                                setNewExecutor({
                                    ...newExecutor,
                                    name: e.target.value,
                                })
                            }
                            className="w-full"
                            disabled={isLoading}
                        />
                    </div>
                    <div className="field">
                        <label
                            htmlFor="resume"
                            className="mb-2 block text-[#334155]"
                        >
                            Резюме
                        </label>
                        <InputTextarea
                            id="resume"
                            value={newExecutor.resume}
                            onChange={(e: ChangeEvent<HTMLTextAreaElement>) =>
                                setNewExecutor({
                                    ...newExecutor,
                                    resume: e.target.value,
                                })
                            }
                            rows={5}
                            className="w-full"
                            disabled={isLoading}
                        />
                    </div>
                    <div className="field">
                        <label className="mb-2 block text-[#334155]">
                            Или загрузите файл
                        </label>
                        <FileUpload
                            ref={fileUploadRef}
                            mode="basic"
                            name="resume"
                            accept=".txt,.doc,.docx,.pdf"
                            maxFileSize={1000000}
                            onUpload={handleFileUpload}
                            disabled={isLoading}
                            chooseLabel="Выбрать файл"
                        />
                    </div>
                    <div className="flex justify-end gap-2">
                        {isLoading && <ProgressSpinner />}
                        <Button
                            label="Обработать"
                            onClick={handleAddExecutor}
                            disabled={isLoading}
                            className="!border-none !bg-[#72efdd] !text-[#334155] transition-all duration-300 hover:!bg-[#72efdd]/80"
                        />
                    </div>
                </div>
            </Dialog>

            {/* Контекст проекта */}
            <Card className="mb-6 shadow-sm">
                <div className="field">
                    <label
                        htmlFor="context"
                        className="mb-2 block text-lg text-[#334155]"
                    >
                        Контекст проекта
                    </label>
                    <InputTextarea
                        id="context"
                        value={projectContext}
                        onChange={(e: ChangeEvent<HTMLTextAreaElement>) =>
                            setProjectContext(e.target.value)
                        }
                        rows={3}
                        className="w-full"
                    />
                </div>
            </Card>

            {/* Блок задач */}
            <Card className="shadow-sm">
                <div className="flex flex-col gap-4">
                    <div className="flex flex-wrap gap-2">
                        {tasks.map((task) => (
                            <Tag
                                key={task.id}
                                value={task.title}
                                className="bg-[#72efdd] px-3 py-2 text-lg text-[#334155]"
                            />
                        ))}
                    </div>
                    <div className="flex gap-4">
                        <div className="field flex-1">
                            <InputText
                                value={newTask.title}
                                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                                    setNewTask({
                                        ...newTask,
                                        title: e.target.value,
                                    })
                                }
                                placeholder="Название задачи"
                                className="w-full"
                            />
                        </div>
                        <div className="field flex-1">
                            <InputText
                                value={newTask.description}
                                onChange={(e: ChangeEvent<HTMLInputElement>) =>
                                    setNewTask({
                                        ...newTask,
                                        description: e.target.value,
                                    })
                                }
                                placeholder="Описание задачи"
                                className="w-full"
                            />
                        </div>
                        <Button
                            label="Добавить задачу"
                            icon="pi pi-plus"
                            onClick={handleAddTask}
                            className="!border-none !bg-[#72efdd] !text-[#334155] transition-all duration-300 hover:!bg-[#72efdd]/80"
                        />
                    </div>
                </div>
            </Card>
        </div>
    )
}

export default Demo
