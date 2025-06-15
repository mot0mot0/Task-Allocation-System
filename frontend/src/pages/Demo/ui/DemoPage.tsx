import { useState, useRef, useEffect } from "react"
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
import { Tooltip } from "primereact/tooltip"
import { InputSwitch } from "primereact/inputswitch"
import axios from "axios"
import { BACKEND_URL } from "../../../constants"

interface Executor {
    id: string
    name: string
    resume: string
    color: string
    isLoading?: boolean
    hasError?: boolean
    analyzed_data?: AnalysisData
}

interface Task {
    id: string
    title: string
    description: string
    start_date: string
    end_date: string
    analyzed_data?: AnalysisData
    color: string
    isLoading?: boolean
    hasError?: boolean
}

interface AnalysisData {
    soft?: Record<string, number>
    hard?: Record<string, number>
}

interface Skill {
    name: string
    level: number
}

interface TaskSkills {
    id: string
    start_date: string
    end_date: string
    soft_skills: Skill[]
    hard_skills: Skill[]
}

interface ExecutorSkills {
    id: string
    soft_skills: Skill[]
    hard_skills: Skill[]
}

interface AllocationRequest {
    tasks: TaskSkills[]
    executors: ExecutorSkills[]
}

interface AllocationResponse {
    allocation: Record<string, string>
}

const DemoPage = () => {
    const [executors, setExecutors] = useState<Executor[]>([])
    const [tasks, setTasks] = useState<Task[]>([])
    const [showExecutorDialog, setShowExecutorDialog] = useState(false)
    const [projectContext, setProjectContext] = useState("")
    const [isProjectContextFocused, setIsProjectContextFocused] =
        useState(false)
    const [newTask, setNewTask] = useState({ 
        title: "", 
        description: "", 
        start_date: "", 
        end_date: ""
    })
    const [newExecutor, setNewExecutor] = useState({ name: "", resume: "" })
    const fileUploadRef = useRef<FileUpload>(null)
    const contextTextareaRef = useRef<HTMLTextAreaElement>(null)
    const [showAllocationDialog, setShowAllocationDialog] = useState(false)
    const [isAllocating, setIsAllocating] = useState(false)
    const [allocation, setAllocation] = useState<Record<string, string>>({})
    const [isGanttView, setIsGanttView] = useState(false)

    const tagColors = [
        "!bg-[#3b82f6]",
        "!bg-[#22c55e]",
        "!bg-[#f59e0b]",
        "!bg-[#8b5cf6]",
        "!bg-[#ec4899]",
        "!bg-[#ef4444]",
        "!bg-[#10b981]",
        "!bg-[#6366f1]",
        "!bg-[#f97316]",
        "!bg-[#14b8a6]",
        "!bg-[#a855f7]",
        "!bg-[#06b6d4]",
        "!bg-[#f43f5e]",
        "!bg-[#84cc16]",
        "!bg-[#0ea5e9]",
    ]

    const getRandomColorClass = () => {
        const randomIndex = Math.floor(Math.random() * tagColors.length)
        return tagColors[randomIndex]
    }

    const formatAnalysisData = (item: Task | Executor) => {
        if (item.isLoading) {
            return "В обработке..."
        }
        if (item.hasError) {
            return "Ошибка при анализе. Нажмите на кнопку обновления для повторной попытки."
        }

        let result = ""
        
        if ('start_date' in item && 'end_date' in item) {
            const startDate = new Date(item.start_date).toLocaleDateString('ru-RU')
            const endDate = new Date(item.end_date).toLocaleDateString('ru-RU')
            result += `Сроки: ${startDate} - ${endDate}\n`
        }

        const data = item.analyzed_data
        if (!data) return result || "Нет данных для анализа"

        const softSkills = data.soft
            ? Object.entries(data.soft)
                  .map(
                      ([skill, value]) =>
                          `ㅤ${skill}: ${(Number(value) * 10).toFixed(0)}/10`
                  )
                  .join("\n")
            : ""

        const hardSkills = data.hard
            ? Object.entries(data.hard)
                  .map(
                      ([skill, value]) =>
                          `ㅤ${skill}: ${(Number(value) * 10).toFixed(0)}/10`
                  )
                  .join("\n")
            : ""

        return [
            result,
            softSkills && "Soft Skills:",
            softSkills,
            hardSkills && "Hard Skills:",
            hardSkills,
        ]
            .filter(Boolean)
            .join("\n")
    }

    const handleFileUpload = async (event: FileUploadUploadEvent) => {
        const file = event.files[0]
        if (file) {
            const text = await file.text()
            setNewExecutor((prev) => ({ ...prev, resume: text }))
        }
    }

    const handleAddExecutor = async () => {
        if (!newExecutor.name || !newExecutor.resume) return

        const executorId = Date.now().toString()
        const executorToAdd = {
            id: executorId,
            name: newExecutor.name,
            resume: newExecutor.resume,
            color: getRandomColorClass(),
            isLoading: true,
            hasError: false,
            analyzed_data: undefined,
        }

        setExecutors((prevExecutors) => [...prevExecutors, executorToAdd])
        setNewExecutor({ name: "", resume: "" })
        setShowExecutorDialog(false)

        try {
            const response = await axios.post(
                `${BACKEND_URL}/analyze/executor`,
                {
                    id: executorId,
                    name: newExecutor.name,
                    resume: newExecutor.resume,
                }
            )
            setExecutors((prevExecutors) =>
                prevExecutors.map((executor) =>
                    executor.id === executorId
                        ? {
                              ...executor,
                              analyzed_data: response.data,
                              isLoading: false,
                              hasError: false,
                          }
                        : executor
                )
            )
        } catch (error) {
            console.error("Error adding executor:", error)
            setExecutors((prevExecutors) =>
                prevExecutors.map((executor) =>
                    executor.id === executorId
                        ? { ...executor, isLoading: false, hasError: true }
                        : executor
                )
            )
        }
    }

    const handleRetryExecutor = async (executorToRetry: Executor) => {
        setExecutors((prevExecutors) =>
            prevExecutors.map((executor) =>
                executor.id === executorToRetry.id
                    ? { ...executor, isLoading: true, hasError: false }
                    : executor
            )
        )
        try {
            const response = await axios.post(
                `${BACKEND_URL}/analyze/executor`,
                {
                    id: executorToRetry.id,
                    name: executorToRetry.name,
                    resume: executorToRetry.resume,
                }
            )
            setExecutors((prevExecutors) =>
                prevExecutors.map((executor) =>
                    executor.id === executorToRetry.id
                        ? {
                              ...executor,
                              analyzed_data: response.data,
                              isLoading: false,
                              hasError: false,
                          }
                        : executor
                )
            )
        } catch (error) {
            console.error("Error analyzing executor on retry:", error)
            setExecutors((prevExecutors) =>
                prevExecutors.map((executor) =>
                    executor.id === executorToRetry.id
                        ? { ...executor, isLoading: false, hasError: true }
                        : executor
                )
            )
        }
    }

    const handleAddTask = async () => {
        if (!newTask.title || !newTask.description || !newTask.start_date || !newTask.end_date) return

        const taskId = Date.now().toString()
        const taskToAdd = {
            id: taskId,
            title: newTask.title,
            description: newTask.description,
            start_date: newTask.start_date,
            end_date: newTask.end_date,
            color: getRandomColorClass(),
            isLoading: true,
            hasError: false,
            analyzed_data: undefined,
        }

        setTasks((prevTasks) => [...prevTasks, taskToAdd])
        setNewTask({ title: "", description: "", start_date: "", end_date: "" })

        try {
            const response = await axios.post(`${BACKEND_URL}/analyze/task`, {
                id: taskId,
                title: taskToAdd.title,
                description: taskToAdd.description,
                start_date: taskToAdd.start_date,
                end_date: taskToAdd.end_date,
                project_description: projectContext,
            })
            setTasks((prevTasks) =>
                prevTasks.map((task) =>
                    task.id === taskId
                        ? {
                              ...task,
                              analyzed_data: response.data.assessment,
                              isLoading: false,
                              hasError: false,
                          }
                        : task
                )
            )
        } catch (error) {
            console.error("Error analyzing task:", error)
            setTasks((prevTasks) =>
                prevTasks.map((task) =>
                    task.id === taskId
                        ? { ...task, isLoading: false, hasError: true }
                        : task
                )
            )
        }
    }

    const handleRetryTask = async (taskToRetry: Task) => {
        setTasks((prevTasks) =>
            prevTasks.map((task) =>
                task.id === taskToRetry.id
                    ? { ...task, isLoading: true, hasError: false }
                    : task
            )
        )
        try {
            const response = await axios.post(`${BACKEND_URL}/analyze/task`, {
                id: taskToRetry.id,
                title: taskToRetry.title,
                description: taskToRetry.description,
                project_description: projectContext,
            })

            setTasks((prevTasks) =>
                prevTasks.map((task) =>
                    task.id === taskToRetry.id
                        ? {
                              ...task,
                              analyzed_data: response.data.assessment,
                              isLoading: false,
                              hasError: false,
                          }
                        : task
                )
            )
        } catch (error) {
            console.error("Error analyzing task on retry:", error)
            setTasks((prevTasks) =>
                prevTasks.map((task) =>
                    task.id === taskToRetry.id
                        ? { ...task, isLoading: false, hasError: true }
                        : task
                )
            )
        }
    }

    const getTooltipContent = (item: Task | Executor) => {
        if (item.isLoading) {
            return "В обработке..."
        }
        if (item.hasError) {
            return "Ошибка при анализе. Нажмите на кнопку обновления для повторной попытки."
        }
        return formatAnalysisData(item) || "Нет данных для анализа"
    }

    const prepareAllocationData = (): AllocationRequest => {
        const tasksData: TaskSkills[] = tasks.map((task) => {
            const assessment = task.analyzed_data
                ? task.analyzed_data
                : { soft: {}, hard: {} }
            return {
                id: task.id,
                title: task.title,
                description: task.description,
                start_date: task.start_date,
                end_date: task.end_date,
                soft_skills: Object.entries(assessment.soft || {}).map(
                    ([name, level]) => ({
                        name,
                        level: Math.round(Number(level) * 10),
                    })
                ),
                hard_skills: Object.entries(assessment.hard || {}).map(
                    ([name, level]) => ({
                        name,
                        level: Math.round(Number(level) * 10),
                    })
                ),
            }
        })

        const executorsData: ExecutorSkills[] = executors.map((executor) => {
            const assessment = executor.analyzed_data
                ? executor.analyzed_data
                : { soft: {}, hard: {} }
            return {
                id: executor.id,
                name: executor.name,
                soft_skills: Object.entries(assessment.soft || {}).map(
                    ([name, level]) => ({
                        name,
                        level: Math.round(Number(level) * 10),
                    })
                ),
                hard_skills: Object.entries(assessment.hard || {}).map(
                    ([name, level]) => ({
                        name,
                        level: Math.round(Number(level) * 10),
                    })
                ),
            }
        })

        return {
            tasks: tasksData,
            executors: executorsData,
        }
    }

    const handleAllocate = async () => {
        setShowAllocationDialog(true)
        setIsAllocating(true)
        setAllocation({})

        try {
            const data = prepareAllocationData()
            await axios.post<AllocationResponse>(
                `${BACKEND_URL}/match/allocate`,
                data
            ).then((response) => {
            setAllocation(response.data.allocation)
            })
        } catch (error) {
            console.error("Error allocating tasks:", error)
        } finally {
            setIsAllocating(false)
        }
    }

    const handleDeleteTask = (taskId: string) => {
        setTasks((prevTasks) => prevTasks.filter((task) => task.id !== taskId));
        // Remove task from allocation if it exists
        setAllocation((prevAllocation) => {
            const newAllocation = { ...prevAllocation };
            delete newAllocation[taskId];
            return newAllocation;
        });
    };

    const handleDeleteExecutor = (executorId: string) => {
        setExecutors((prevExecutors) => prevExecutors.filter((executor) => executor.id !== executorId));

        setAllocation((prevAllocation) => {
            const newAllocation = { ...prevAllocation };
            Object.entries(newAllocation).forEach(([taskId, assignedExecutorId]) => {
                if (assignedExecutorId === executorId) {
                    delete newAllocation[taskId];
                }
            });
            return newAllocation;
        });
    };

    useEffect(() => {
        const taskTags = document.querySelectorAll(".task-tag")
        const executorTags = document.querySelectorAll(".executor-tag")

        taskTags.forEach((tag) => {
            const taskId = tag.getAttribute("data-task-id")
            const task = tasks.find((t) => t.id === taskId)
            if (task) {
                tag.setAttribute("data-pr-tooltip", getTooltipContent(task))
            }
        })

        executorTags.forEach((tag) => {
            const executorId = tag.getAttribute("data-executor-id")
            const executor = executors.find(
                (e) => e.id.toString() === executorId
            )
            if (executor) {
                tag.setAttribute("data-pr-tooltip", getTooltipContent(executor))
            }
        })
    }, [tasks, executors])

    return (
        <div className="flex min-h-screen w-full max-w-[1064px] flex-col gap-y-8 bg-transparent px-5 pt-22 pb-8">
            <style>
                {`
                    .p-tooltip {
                        max-height: 80vh;
                    }
                    .p-tooltip-text {
                        white-space: pre-line;
                        max-height: 80vh;
                        overflow-y: auto;
                    }
                `}
            </style>
            <Card className="bg-transparent p-0 shadow-sm">
                <div className="field flex flex-col gap-3 py-3">
                    {isProjectContextFocused ? (
                        <InputTextarea
                            id="context"
                            ref={contextTextareaRef}
                            value={projectContext}
                            onChange={(e: ChangeEvent<HTMLTextAreaElement>) =>
                                setProjectContext(e.target.value)
                            }
                            onBlur={() => setIsProjectContextFocused(false)}
                            rows={1}
                            className="w-full"
                            autoResize={true}
                            placeholder="Описание проекта"
                        />
                    ) : (
                        <div
                            id="context"
                            className={`flex h-[50px] w-full cursor-text items-center overflow-hidden rounded-md border border-[#424242] bg-[#3030309c] px-3 py-2 text-ellipsis whitespace-nowrap transition duration-200 hover:!border-(--primary-app-color) ${projectContext.length > 0 ? "text-[var(--text-color-primary)]" : ""}`}
                            onClick={() => setIsProjectContextFocused(true)}
                            aria-hidden="true"
                        >
                            {projectContext.length > 0
                                ? projectContext
                                : "Описание проекта"}
                        </div>
                    )}

                    <small id="context-help">
                        Опишите контекст вашего проекта как можно подробнее для
                        более эффективного анализа
                    </small>
                </div>
            </Card>

            <div className="flex flex-1 flex-row gap-8">
                <Card className="w-full flex-1 shadow-sm">
                    <div className="flex h-full flex-col gap-4 py-3">
                        {tasks.length > 0 && (
                            <div className="flex flex-wrap items-center gap-2">
                                {tasks.map((task) => (
                                    <div
                                        key={task.id}
                                        className="flex items-center gap-1"
                                    >
                                        <Tooltip
                                            target={`#task-${task.id}`}
                                            content={getTooltipContent(task)}
                                            showDelay={150}
                                            hideDelay={300}
                                            position="bottom"
                                            autoHide={false}
                                            className="max-h-[80vh] overflow-y-auto"
                                        />
                                        <Tag
                                            id={`task-${task.id}`}
                                            value={
                                                <div className="flex items-center gap-2">
                                                    <span>{task.title}</span>
                                                    <i 
                                                        className="pi pi-times text-[#ef4444] text-sm cursor-pointer hover:text-[#dc2626] p-1 rounded-full hover:bg-[#ffffff75] transition-colors"
                                                        style={{ fontSize: '0.8rem' }}
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            handleDeleteTask(task.id);
                                                        }}
                                                    />
                                                </div>
                                            }
                                            className={`task-tag ${task.color} cursor-default overflow-hidden px-3 py-2 text-left text-lg text-ellipsis whitespace-nowrap text-[#f8f8f8]`}
                                        />
                                        {task.isLoading && (
                                            <ProgressSpinner
                                                style={{
                                                    width: "20px",
                                                    height: "20px",
                                                }}
                                                strokeWidth="8"
                                                fill="transparent"
                                                animationDuration=".5s"
                                            />
                                        )}
                                        {task.hasError && !task.isLoading && (
                                            <Button
                                                icon="pi pi-refresh"
                                                className="p-button-rounded p-button-danger p-button-text !h-[26px] !w-[26px]"
                                                onClick={() => handleRetryTask(task)}
                                            />
                                        )}
                                    </div>
                                ))}
                            </div>
                        )}
                        <div className="flex flex-1 flex-col gap-4">
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
                                <Button
                                    label="Добавить"
                                    icon="pi pi-plus"
                                    onClick={handleAddTask}
                                    className="!border-none !bg-(--primary-app-color) !text-[#334155] transition-all duration-300 hover:!bg-(--primary-app-color)/80"
                                />
                            </div>
                            <div className="flex gap-4">
                                <div className="field flex-1">
                                    <InputText
                                        type="date"
                                        value={newTask.start_date}
                                        onChange={(e: ChangeEvent<HTMLInputElement>) =>
                                            setNewTask({
                                                ...newTask,
                                                start_date: e.target.value,
                                            })
                                        }
                                        placeholder="Дата начала"
                                        className="w-full"
                                    />
                                </div>
                                <div className="field flex-1">
                                    <InputText
                                        type="date"
                                        value={newTask.end_date}
                                        onChange={(e: ChangeEvent<HTMLInputElement>) =>
                                            setNewTask({
                                                ...newTask,
                                                end_date: e.target.value,
                                            })
                                        }
                                        placeholder="Дата окончания"
                                        className="w-full"
                                    />
                                </div>
                            </div>
                            <div className="field flex-1">
                                <InputTextarea
                                    value={newTask.description}
                                    onChange={(e: ChangeEvent<HTMLTextAreaElement>) =>
                                        setNewTask({
                                            ...newTask,
                                            description: e.target.value,
                                        })
                                    }
                                    autoResize={true}
                                    placeholder="Описание задачи"
                                    className="!h-full w-full"
                                />
                            </div>
                        </div>
                    </div>
                </Card>

                <div className="flex flex-col gap-8 max-w-[350px]">
                    <Card className="flex-1 shadow-sm">
                        <div className="flex flex-col justify-between gap-4 py-3">
                            <Button
                                label="Добавить"
                                icon="pi pi-plus"
                                onClick={() => setShowExecutorDialog(true)}
                                className="!border-none !bg-(--primary-app-color) !text-[#334155] transition-all duration-300 hover:!bg-(--primary-app-color)/80"
                            />

                            <div className="flex flex-wrap items-center gap-2">
                                {executors.map((executor) => (
                                    <div
                                        key={executor.id}
                                        className="flex items-center gap-1"
                                    >
                                        <Tooltip
                                            target={`#executor-${executor.id}`}
                                            content={getTooltipContent(
                                                executor
                                            )}
                                            showDelay={150}
                                            hideDelay={300}
                                            mouseTrackTop={0}
                                            position="left"
                                            autoHide={false}
                                        />
                                        <Tag
                                            id={`executor-${executor.id}`}
                                            value={
                                                <div className="flex items-center gap-2">
                                                    <span>{executor.name.trim().split(" ")[0]}</span>
                                                    <i 
                                                        className="pi pi-times text-[#ef4444] text-sm cursor-pointer hover:text-[#dc2626] p-1 rounded-full hover:bg-[#ffffff75] transition-colors"
                                                        style={{ fontSize: '0.8rem' }}
                                                        onClick={(e) => {
                                                            e.stopPropagation();
                                                            handleDeleteExecutor(executor.id);
                                                        }}
                                                    />
                                                </div>
                                            }
                                            className={`executor-tag cursor-default ${executor.color} px-3 py-2 text-lg text-[#334155]`}
                                        />
                                        {executor.isLoading && (
                                            <ProgressSpinner
                                                style={{
                                                    width: "20px",
                                                    height: "20px",
                                                }}
                                                strokeWidth="8"
                                                fill="transparent"
                                                animationDuration=".5s"
                                            />
                                        )}
                                        {executor.hasError && !executor.isLoading && (
                                            <Button
                                                icon="pi pi-refresh"
                                                className="p-button-rounded p-button-danger p-button-text !h-[20px] !w-[20px]"
                                                onClick={() => handleRetryExecutor(executor)}
                                            />
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>
                    </Card>

                    <Button
                        label="Распределить"
                        onClick={handleAllocate}
                        disabled={tasks.length === 0 || executors.length === 0}
                        className={`!border-none !text-[#334155] transition-all duration-300 ${
                            tasks.length === 0 || executors.length === 0
                                ? "cursor-not-allowed !bg-gray-400"
                                : "!bg-(--primary-app-color) hover:!bg-(--primary-app-color)/80"
                        }`}
                    />
                </div>
            </div>

            <Dialog
                visible={showExecutorDialog}
                onHide={() => setShowExecutorDialog(false)}
                header="Добавить исполнителя"
                className="w-2/3"
            >
                <div className="flex flex-col gap-4">
                    <div className="field">
                        <label
                            htmlFor="name"
                            className="mb-2 block text-(--text-color-secondary)"
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
                        />
                    </div>
                    <div className="field">
                        <label
                            htmlFor="resume"
                            className="mb-2 block text-(--text-color-secondary)"
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
                            rows={4}
                            className="min-h-[50px] w-full"
                            autoResize={true}
                        />
                    </div>
                    <div className="flex justify-between">
                        <div className="flex items-end gap-4">
                            <FileUpload
                                ref={fileUploadRef}
                                mode="basic"
                                name="resume"
                                accept=".txt,.doc,.docx,.pdf"
                                maxFileSize={1000000}
                                onUpload={handleFileUpload}
                                chooseLabel="Выбрать файл"
                            />
                            <label className="block h-fit text-(--text-color-secondary)">
                                Прикрепить файл (.txt, .doc, .docx, .pdf)
                            </label>
                        </div>
                        <div className="flex items-end justify-end gap-2 rounded-md transition duration-200">
                            <Button
                                label="Обработать"
                                onClick={handleAddExecutor}
                                className="h-[48px] !border-none !bg-[#72efdd] !text-[#334155] transition-all duration-300 hover:!bg-[#72efddcc]"
                            />
                        </div>
                    </div>
                </div>
            </Dialog>

            <Dialog
                visible={showAllocationDialog}
                onHide={() => setShowAllocationDialog(false)}
                header="Распределение задач"
                className="w-4/5"
                style={{ maxWidth: "1200px" }}
            >
                {isAllocating ? (
                    <div className="flex flex-col items-center justify-center gap-4 py-12">
                        <ProgressSpinner
                            style={{ width: "50px", height: "50px" }}
                        />
                        <span className="text-lg text-(--text-color-secondary)">
                            Ожидание обработки данных...
                        </span>
                    </div>
                ) : (
                    <div className="flex flex-col gap-2">
                        {isGanttView ? (
                            <div className="flex flex-col gap-4 p-4">
                                <div className="flex flex-col gap-4">
                                    {executors.map((executor) => (
                                        <div key={executor.id} className="flex flex-col gap-2">
                                            <div className="flex items-center gap-2">
                                                <Tooltip
                                                    target={`#gantt-executor-${executor.id}`}
                                                    content={getTooltipContent(executor)}
                                                    showDelay={150}
                                                    hideDelay={300}
                                                    mouseTrackTop={0}
                                                    position="bottom"
                                                    autoHide={false}
                                                />
                                                <label id={`gantt-executor-${executor.id}`} className="text-md font-medium text-(--text-color-secondary) cursor-default">
                                                    {executor.name}
                                                </label>
                                            </div>
                                            <div className="flex flex-col gap-2">
                                                <div className="relative h-6 w-full border-b border-[#424242]">
                                                    {(() => {
                                                        const minDate = new Date(Math.min(...tasks.map(t => new Date(t.start_date).getTime())));
                                                        const maxDate = new Date(Math.max(...tasks.map(t => new Date(t.end_date).getTime())));
                                                        const totalDays = (maxDate.getTime() - minDate.getTime()) / (1000 * 60 * 60 * 24);
                                                        const months = [];
                                                        let currentDate = new Date(minDate);
                                                        
                                                        while (currentDate <= maxDate) {
                                                            const monthStart = new Date(currentDate.getFullYear(), currentDate.getMonth(), 1);
                                                            const monthEnd = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 0);
                                                            const monthStartOffset = ((monthStart.getTime() - minDate.getTime()) / (1000 * 60 * 60 * 24) / totalDays) * 100;
                                                            const monthWidth = ((monthEnd.getTime() - monthStart.getTime()) / (1000 * 60 * 60 * 24) / totalDays) * 100;
                                                            
                                                            months.push(
                                                                <div
                                                                    key={monthStart.toISOString()}
                                                                    className="absolute h-full border-r border-[#424242]"
                                                                    style={{
                                                                        left: `${monthStartOffset}%`,
                                                                        width: `${monthWidth}%`,
                                                                    }}
                                                                >
                                                                    <span className="absolute -top-6 left-2 text-xs text-(--text-color-secondary)">
                                                                        {monthStart.toLocaleString('ru-RU', { month: 'short', year: 'numeric' })}
                                                                    </span>
                                                                </div>
                                                            );
                                                            
                                                            currentDate = new Date(currentDate.getFullYear(), currentDate.getMonth() + 1, 1);
                                                        }
                                                        
                                                        return months;
                                                    })()}
                                                </div>
                                                {tasks
                                                    .filter((task) => allocation[task.id] === executor.id)
                                                    .map((task) => {
                                                        const startDate = new Date(task.start_date);
                                                        const endDate = new Date(task.end_date);
                                                        const minDate = new Date(Math.min(...tasks.map(t => new Date(t.start_date).getTime())));
                                                        const maxDate = new Date(Math.max(...tasks.map(t => new Date(t.end_date).getTime())));
                                                        const totalDays = (maxDate.getTime() - minDate.getTime()) / (1000 * 60 * 60 * 24);
                                                        const startOffset = ((startDate.getTime() - minDate.getTime()) / (1000 * 60 * 60 * 24) / totalDays) * 100;
                                                        const width = ((endDate.getTime() - startDate.getTime()) / (1000 * 60 * 60 * 24) / totalDays) * 100;
                                                        
                                                        return (
                                                            <div key={task.id} className="relative h-8 w-full">
                                                                <div className="absolute inset-0 grid grid-cols-[repeat(52,1fr)] gap-px">
                                                                    {Array.from({ length: 52 }).map((_, i) => (
                                                                        <div key={i} className="h-full border-r border-[#424242]/30" />
                                                                    ))}
                                                                </div>
                                                                <Tooltip
                                                                    target={`#gantt-task-${task.id}`}
                                                                    content={getTooltipContent(task)}
                                                                    position="top"
                                                                    autoHide={false}
                                                                />
                                                                <div
                                                                    id={`gantt-task-${task.id}`}
                                                                    className={`absolute h-full overflow-hidden rounded-md ${task.color} cursor-default`}
                                                                    style={{
                                                                        left: `${startOffset}%`,
                                                                        width: `${width}%`,
                                                                    }}
                                                                >
                                                                    <span className="px-2 py-1 text-sm text-[#f8f8f8] truncate">
                                                                        {task.title}
                                                                    </span>
                                                                </div>
                                                            </div>
                                                        );
                                                    })}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        ) : (
                            <div className="overflow-x-auto">
                                <div className="flex min-w-max gap-4 p-4">
                                    {executors.map((executor) => (
                                        <div key={executor.id} className="flex flex-1 min-w-[300px] flex-col gap-4">
                                            <div className="flex items-center justify-center rounded-md bg-[#72efdd] px-4 py-2">
                                                <Tooltip
                                                    target={`#executor-${executor.id}`}
                                                    content={getTooltipContent(
                                                        executor
                                                    )}
                                                    showDelay={150}
                                                    hideDelay={300}
                                                    mouseTrackTop={0}
                                                    position="bottom"
                                                    autoHide={false}
                                                />
                                                <label id={`executor-${executor.id}`} className="w-full text-center text-md font-medium text-[#334155] cursor-default">
                                                    {executor.name}
                                                </label>
                                            </div>
                                            <div className="flex min-h-[300px] flex-col gap-2 rounded-md border border-[#424242] bg-[#3030309c] p-4">
                                                {tasks
                                                    .filter((task) => allocation[task.id] === executor.id)
                                                    .map((task) => (
                                                        <div key={task.id} className="flex flex-col gap-1">
                                                            <Tooltip
                                                                target={`#allocation-task-${task.id}`}
                                                                content={getTooltipContent(task)}
                                                                position="bottom"
                                                                autoHide={false}
                                                            />
                                                            <Tag
                                                                id={`allocation-task-${task.id}`}
                                                                value={task.title}
                                                                className={`task-tag ${task.color} cursor-default overflow-hidden px-3 py-2 text-left text-lg text-ellipsis whitespace-nowrap text-[#f8f8f8]`}
                                                            />
                                                        </div>
                                                    ))}
                                                {tasks.filter((task) => allocation[task.id] === executor.id).length === 0 && (
                                                    <div className="flex h-full items-center justify-center rounded-md border border-dashed border-[#424242] px-4 py-8">
                                                        <span className="text-(--text-color-secondary)">Нет назначенных задач</span>
                                                    </div>
                                                )}
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                        <div className="flex justify-between px-4 gap-4">
                                <div className="flex items-center gap-2">
                                    <span className="text-(--text-color-secondary)">Список</span>
                                    <InputSwitch checked={isGanttView} onChange={(e) => setIsGanttView(e.value)} />
                                    <span className="text-(--text-color-secondary)">Диаграмма Ганта</span>
                                </div>
                                <div className="relative">
                                    <Tooltip
                                        target="#unassigned-tasks-button"
                                        content="Показать нераспределенные задачи"
                                        position="left"
                                    />
                                    <Button
                                        id="unassigned-tasks-button"
                                        icon="pi pi-list"
                                        className={`menu-button p-button-rounded p-button-text !h-[48px] !w-[48px] ${
                                            tasks.some((task) => allocation[task.id] === "unassigned")
                                                ? "!text-[#ef4444] hover:!bg-[#ef4444]/10"
                                                : "!text-[#424242] cursor-not-allowed"
                                        }`}
                                        onClick={() => {
                                            if (tasks.some((task) => allocation[task.id] === "unassigned")) {
                                                const popup = document.getElementById("unassigned-tasks-popup");
                                                if (popup) {
                                                    popup.style.display = popup.style.display === "none" ? "block" : "none";
                                                }
                                            }
                                        }}
                                    />
                                    {tasks.some((task) => allocation[task.id] === "unassigned") && (
                                        <div
                                            id="unassigned-tasks-popup"
                                            className="absolute bottom-full right-1/2 mb-2 hidden  transform"
                                            style={{ minWidth: "300px" }}
                                        >
                                            <div className="flex flex-col gap-2 rounded-md border border-[#424242] bg-[#3030309c] p-4 shadow-lg">
                                                <div className="flex flex-col gap-2">
                                                    {tasks
                                                        .filter((task) => allocation[task.id] === "unassigned")
                                                        .map((task) => (
                                                            <div key={task.id} className="flex flex-col gap-1">
                                                                <Tooltip
                                                                    target={`#allocation-task-${task.id}`}
                                                                    content={getTooltipContent(task)}
                                                                    position="left"
                                                                    autoHide={false}
                                                                />
                                                                <Tag
                                                                    id={`allocation-task-${task.id}`}
                                                                    value={task.title}
                                                                    className={`task-tag ${task.color} cursor-default overflow-hidden px-3 py-2 text-left text-lg text-ellipsis whitespace-nowrap text-[#f8f8f8]`}
                                                                />
                                                            </div>
                                                        ))}
                                                </div>
                                            </div>
                                        </div>
                                    )}
                                </div>
                        </div>
                    </div>
                )}
            </Dialog>
        </div>
    )
}

export default DemoPage
