"use client"

import type React from "react"

import { useState } from "react"
import { Send, RotateCcw } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import type { useChatStream } from "@/hooks/useChatStream"

interface MessageInputProps {
  disabled?: boolean
  streamData: ReturnType<typeof useChatStream>
}

export default function MessageInput({ disabled = false, streamData }: MessageInputProps) {
  const [message, setMessage] = useState("")
  const { sendMessage, clearConversation, isLoading } = streamData

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (message.trim() && !disabled && !isLoading) {
      sendMessage(message.trim())
      setMessage("")
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleClear = () => {
    clearConversation()
    setMessage("")
  }

  if (disabled) {
    return (
      <div
        className="p-4 border-t border-gray-200 bg-gray-50"
        style={{ backgroundColor: "var(--google-grey-100)", borderColor: "var(--google-grey-200)" }}
      >
        <div className="text-center text-gray-500 text-sm" style={{ color: "var(--google-grey-600)" }}>
          Input disabled - awaiting approval
        </div>
      </div>
    )
  }

  return (
    <div className="p-4 border-t border-gray-200" style={{ borderColor: "var(--google-grey-200)" }}>
      <form onSubmit={handleSubmit} className="flex gap-2">
        <Textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask me anything about building agents with ADK..."
          className="flex-1 min-h-[40px] max-h-[120px] resize-none"
          rows={1}
          disabled={isLoading}
        />
        <div className="flex flex-col gap-2">
          <Button
            type="submit"
            disabled={!message.trim() || isLoading}
            className="text-white"
            style={{ backgroundColor: "var(--google-blue)" }}
          >
            <Send className="h-4 w-4" />
          </Button>
          <Button
            type="button"
            onClick={handleClear}
            variant="outline"
            size="sm"
            className="text-gray-600 hover:text-gray-800"
            title="Clear conversation"
          >
            <RotateCcw className="h-3 w-3" />
          </Button>
        </div>
      </form>
    </div>
  )
}
