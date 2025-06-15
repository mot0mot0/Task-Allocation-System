import { useState } from "react"
import { Button } from "primereact/button"
import { Tooltip } from "primereact/tooltip"

interface CodeBlockProps {
    code: string
}

export const CodeBlock = ({ code }: CodeBlockProps) => {
    const [copied, setCopied] = useState(false)

    const copyToClipboard = () => {
        navigator.clipboard.writeText(code)
        setCopied(true)
        setTimeout(() => setCopied(false), 2000)
    }

    return (
        <div className="relative">
            <pre className="rounded-lg bg-[#3a3a3a] p-4 text-sm">
                <code>{code}</code>
            </pre>
            <Tooltip target=".copy-button" />
            <Button
                icon={copied ? "pi pi-check" : "pi pi-copy"}
                className="copy-button absolute right-2 top-2 !h-8 !w-8 !p-0"
                onClick={copyToClipboard}
                tooltip={copied ? "Скопировано!" : "Копировать"}
                tooltipOptions={{ position: "left" }}
            />
        </div>
    )
} 