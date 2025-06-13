"use client"

import ChatMessage from "./ChatMessage"
import MessageInput from "./MessageInput"
import ArchitectureApprovalCard from "./ArchitectureApprovalCard"
import ErrorDisplay from "./ErrorBoundary"
import type { useChatStream } from "@/hooks/useChatStream"
import { Loader2 } from "lucide-react"

interface ChatWindowProps {
  streamData: ReturnType<typeof useChatStream>
}

export default function ChatWindow({ streamData }: ChatWindowProps) {
  const { messages, isLoading, error, isAwaitingApproval, clearConversation } = streamData

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header */}
      <div
        className="p-4 border-b border-gray-200 bg-gray-50"
        style={{ backgroundColor: "var(--google-grey-100)", borderColor: "var(--google-grey-200)" }}
      >
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-semibold text-gray-900" style={{ color: "var(--google-grey-800)" }}>
            Smart Conversation Thread
          </h1>
          {isLoading && (
            <div className="flex items-center gap-2" style={{ color: "var(--google-blue)" }}>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span className="text-sm">Agent is thinking...</span>
            </div>
          )}
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <ErrorDisplay
          error={error}
          onClear={() => {
            clearConversation()
          }}
        />
      )}

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && !isLoading && !error && (
          <div className="text-center text-gray-500 mt-8">
            <div className="mb-4">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🤖</span>
              </div>
              <h2 className="text-lg font-medium mb-2" style={{ color: "var(--google-grey-800)" }}>
                Welcome to ADK Copilot!
              </h2>
              <p className="text-sm" style={{ color: "var(--google-grey-600)" }}>
                Ask me anything about building agents with the Google Agent Development Kit.
              </p>
            </div>
            <div className="text-xs" style={{ color: "var(--google-grey-500)" }}>
              Try asking: "Create a weather agent" or "Help me build a chatbot"
            </div>
          </div>
        )}

        {messages.map((message) => (
          <div key={message.id}>
            {message.type === "approval" ? (
              <ArchitectureApprovalCard
                planText={message.planText || message.text}
                diagramUrl={message.diagramUrl || ""}
                streamData={streamData}
              />
            ) : (
              <ChatMessage message={message} />
            )}
          </div>
        ))}
      </div>

      {/* Input */}
      <MessageInput disabled={isLoading || isAwaitingApproval} streamData={streamData} />
    </div>
  )
}
