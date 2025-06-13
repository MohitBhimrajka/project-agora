"use client"

import { useState } from "react"
import { Copy, Check, FileText } from "lucide-react"
import { Button } from "@/components/ui/button"
import type { StreamMessage } from "@/hooks/useChatStream"

interface ChatMessageProps {
  message: StreamMessage
}

export default function ChatMessage({ message }: ChatMessageProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async (text: string) => {
    await navigator.clipboard.writeText(text)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const isUser = message.sender === "user"

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[80%] rounded-lg p-4 google-shadow ${isUser ? "text-white" : "bg-white"}`}
        style={{
          backgroundColor: isUser ? "var(--google-blue)" : "white",
          color: isUser ? "white" : "var(--google-grey-800)",
        }}
      >
        {message.type === "code" ? (
          <div className="relative">
            {/* Enhanced code header with filename */}
            <div
              className="flex items-center justify-between px-4 py-2 rounded-t-lg border-b"
              style={{
                backgroundColor: "var(--google-grey-800)",
                borderColor: "var(--google-grey-600)",
              }}
            >
              <div className="flex items-center gap-2">
                <FileText className="text-green-400 w-4 h-4" />
                <span className="text-green-400 text-sm font-mono">
                  {message.filename ? `==== FILE: ${message.filename} ====` : message.language || "code"}
                </span>
              </div>
              <Button
                size="sm"
                variant="ghost"
                onClick={() => handleCopy(message.text)}
                className="text-green-400 hover:text-green-300 hover:bg-gray-700 h-8 px-2"
              >
                {copied ? <Check className="w-4 h-4 mr-1" /> : <Copy className="w-4 h-4 mr-1" />}
                <span className="text-xs">{copied ? "Copied!" : "Copy Code"}</span>
              </Button>
            </div>
            <pre
              className="p-4 rounded-b-lg text-sm overflow-x-auto font-mono"
              style={{ backgroundColor: "var(--google-grey-900)", color: "#00ff00" }}
            >
              <code>{message.text}</code>
            </pre>
          </div>
        ) : (
          <p className="whitespace-pre-wrap">{message.text}</p>
        )}

        <div className="text-xs opacity-70 mt-2">{message.timestamp.toLocaleTimeString()}</div>
      </div>
    </div>
  )
}
