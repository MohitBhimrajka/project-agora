"use client"

import { useState, useCallback, useRef } from "react"

// Replace this with your actual Cloud Run service URL
const API_URL = process.env.NEXT_PUBLIC_API_URL || "https://your-adk-copilot-service-xxxxxxxx-uc.a.run.app/run_sse"

export interface StreamMessage {
  id: string
  sender: "user" | "agent"
  text: string
  type?: "text" | "code" | "approval"
  timestamp: Date
  filename?: string
  language?: string
  planText?: string
  diagramUrl?: string
}

export interface StreamLogEntry {
  id: string
  type: string
  status: "in_progress" | "completed" | "error"
  tool_name?: string
  agent_name?: string
  input?: any
  output?: any
  timestamp: Date
  title: string
  icon: "brain" | "book" | "database" | "wrench" | "lightbulb" | "target"
}

export const useChatStream = () => {
  const [messages, setMessages] = useState<StreamMessage[]>([])
  const [logEntries, setLogEntries] = useState<StreamLogEntry[]>([])
  const [ticketState, setTicketState] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [isAwaitingApproval, setIsAwaitingApproval] = useState(false)
  const eventSourceRef = useRef<EventSource | null>(null)

  const getIconForEntry = (data: any): StreamLogEntry["icon"] => {
    const title = data.tool_name || data.agent_name || data.type || ""

    if (title.includes("ticket_analysis")) return "lightbulb"
    if (title.includes("knowledge_retrieval")) return "book"
    if (title.includes("db_retrieval")) return "database"
    if (title.includes("code_generator")) return "target"
    if (title.includes("llm") || title.includes("thinking")) return "brain"

    return "wrench"
  }

  const sendMessage = useCallback(
    async (userMessage: string) => {
      setIsLoading(true)
      setError(null)

      // Add user message to the chat immediately
      const userMsg: StreamMessage = {
        id: Date.now().toString(),
        sender: "user",
        text: userMessage,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, userMsg])

      try {
        // Close any existing connection
        if (eventSourceRef.current) {
          eventSourceRef.current.close()
        }

        // For development/testing, we'll simulate the API response
        if (API_URL.includes("your-adk-copilot-service")) {
          // Simulate API response for demo purposes
          simulateApiResponse(userMessage)
          return
        }

        // Create a POST request to initiate the SSE stream
        const response = await fetch(API_URL, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "text/event-stream",
            "Cache-Control": "no-cache",
          },
          body: JSON.stringify({
            app_name: "adk_copilot",
            request: { text: userMessage },
            session: {
              state: {
                ticket: ticketState, // Send the state from the previous turn
              },
            },
          }),
        })

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`)
        }

        // Handle the streaming response
        const reader = response.body?.getReader()
        const decoder = new TextDecoder()

        if (!reader) {
          throw new Error("No response body reader available")
        }

        let buffer = ""

        while (true) {
          const { done, value } = await reader.read()

          if (done) {
            setIsLoading(false)
            break
          }

          buffer += decoder.decode(value, { stream: true })
          const lines = buffer.split("\n")
          buffer = lines.pop() || "" // Keep incomplete line in buffer

          for (const line of lines) {
            if (line.startsWith("data: ")) {
              try {
                const eventData = line.slice(6).trim()
                if (eventData === "[DONE]") {
                  setIsLoading(false)
                  return
                }
                const data = JSON.parse(eventData)
                handleStreamEvent(data)
              } catch (parseError) {
                console.warn("Failed to parse SSE data:", parseError, line)
              }
            } else if (line.startsWith("event: ")) {
              // Handle event type if needed
              const eventType = line.slice(7).trim()
              if (eventType === "end") {
                setIsLoading(false)
                return
              }
            }
          }
        }
      } catch (err) {
        console.error("Stream error:", err)
        setError(`Connection failed: ${err instanceof Error ? err.message : "Unknown error"}`)
        setIsLoading(false)
      }
    },
    [ticketState],
  )

  // Simulate API response for demo/development
  const simulateApiResponse = (userMessage: string) => {
    // Simulate thinking
    const thinkingEntry: StreamLogEntry = {
      id: `llm-${Date.now()}`,
      type: "llm_request",
      status: "in_progress",
      timestamp: new Date(),
      title: "LLM: Processing request",
      icon: "brain",
    }
    setLogEntries((prev) => [thinkingEntry, ...prev])

    setTimeout(() => {
      // Complete thinking
      setLogEntries((prev) =>
        prev.map((entry) => (entry.id === thinkingEntry.id ? { ...entry, status: "completed" } : entry)),
      )

      // Add agent response
      const agentMessage: StreamMessage = {
        id: Date.now().toString(),
        sender: "agent",
        text: `I understand you want to: "${userMessage}". I'm analyzing your request and will provide a comprehensive solution using the ADK framework.`,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, agentMessage])

      // Simulate more agent activity
      setTimeout(() => {
        const analysisEntry: StreamLogEntry = {
          id: `analysis-${Date.now()}`,
          type: "agent_request",
          status: "in_progress",
          agent_name: "ticket_analysis_agent",
          timestamp: new Date(),
          title: "Agent: ticket_analysis_agent",
          icon: "lightbulb",
        }
        setLogEntries((prev) => [analysisEntry, ...prev])

        setTimeout(() => {
          setLogEntries((prev) =>
            prev.map((entry) => (entry.id === analysisEntry.id ? { ...entry, status: "completed" } : entry)),
          )

          // Show approval request
          const approvalMessage: StreamMessage = {
            id: Date.now().toString(),
            sender: "agent",
            text: "I've analyzed your request and prepared a solution plan. Shall I proceed with the implementation?",
            type: "approval",
            timestamp: new Date(),
            planText: `Plan: I will create a comprehensive solution for your request: "${userMessage}". This will involve setting up the necessary ADK components, configuring the agent architecture, and implementing the required functionality.`,
            diagramUrl: "/placeholder.svg?height=200&width=300",
          }
          setMessages((prev) => [...prev, approvalMessage])
          setIsAwaitingApproval(true)
          setIsLoading(false)
        }, 1500)
      }, 1000)
    }, 2000)
  }

  const handleStreamEvent = (data: any) => {
    console.log("Received event:", data.type, data)

    switch (data.type) {
      case "tool_request":
        const toolEntry: StreamLogEntry = {
          id: `tool-${Date.now()}-${Math.random()}`,
          type: "tool_request",
          status: "in_progress",
          tool_name: data.tool_request?.name,
          input: data.tool_request?.input,
          timestamp: new Date(),
          title: `Tool: ${data.tool_request?.name || "Unknown"}`,
          icon: getIconForEntry(data.tool_request),
        }
        setLogEntries((prev) => [toolEntry, ...prev])
        break

      case "tool_response":
        setLogEntries((prev) =>
          prev.map((entry) =>
            entry.tool_name === data.tool_response?.name && entry.status === "in_progress"
              ? { ...entry, status: "completed", output: data.tool_response?.output }
              : entry,
          ),
        )
        break

      case "agent_request":
        const agentEntry: StreamLogEntry = {
          id: `agent-${Date.now()}-${Math.random()}`,
          type: "agent_request",
          status: "in_progress",
          agent_name: data.agent_request?.name,
          input: data.agent_request?.input,
          timestamp: new Date(),
          title: `Agent: ${data.agent_request?.name || "Unknown"}`,
          icon: getIconForEntry(data.agent_request),
        }
        setLogEntries((prev) => [agentEntry, ...prev])
        break

      case "agent_response":
        setLogEntries((prev) =>
          prev.map((entry) =>
            entry.agent_name === data.agent_response?.name && entry.status === "in_progress"
              ? { ...entry, status: "completed", output: data.agent_response?.output }
              : entry,
          ),
        )
        break

      case "llm_request":
        const llmEntry: StreamLogEntry = {
          id: `llm-${Date.now()}-${Math.random()}`,
          type: "llm_request",
          status: "in_progress",
          timestamp: new Date(),
          title: "LLM: Processing request",
          icon: "brain",
        }
        setLogEntries((prev) => [llmEntry, ...prev])
        break

      case "llm_response":
        setLogEntries((prev) =>
          prev.map((entry, index) =>
            index === 0 && entry.type === "llm_request" && entry.status === "in_progress"
              ? { ...entry, status: "completed", output: data.llm_response }
              : entry,
          ),
        )
        break

      case "final_response":
        const agentMessage: StreamMessage = {
          id: Date.now().toString(),
          sender: "agent",
          text: data.final_response?.text || data.final_response?.content || "Response received",
          type: data.final_response?.type || "text",
          timestamp: new Date(),
          filename: data.final_response?.filename,
          language: data.final_response?.language,
        }

        // Check if this is an approval request
        if (data.final_response?.text?.includes("Shall I proceed") || data.final_response?.requires_approval) {
          setIsAwaitingApproval(true)
          agentMessage.type = "approval"
          agentMessage.planText = data.final_response?.plan_text
          agentMessage.diagramUrl = data.final_response?.diagram_url
        }

        setMessages((prev) => [...prev, agentMessage])
        break

      case "state":
        // CRITICAL: Store the updated state for the next request
        setTicketState(data.state?.ticket)
        break

      case "error":
        setError(data.error?.message || "An error occurred")
        setIsLoading(false)
        break

      case "end":
        console.log("Stream ended by server")
        setIsLoading(false)
        break

      default:
        console.log("Unhandled event type:", data.type, data)
        break
    }
  }

  const handleApproval = useCallback(
    (approved: boolean, feedback?: string) => {
      const approvalMessage = approved
        ? "Plan approved. Proceeding with implementation."
        : `Plan rejected. ${feedback || "Please revise the approach."}`

      setIsAwaitingApproval(false)
      sendMessage(approvalMessage)
    },
    [sendMessage],
  )

  const clearConversation = useCallback(() => {
    setMessages([])
    setLogEntries([])
    setTicketState(null)
    setIsAwaitingApproval(false)
    setError(null)
    setIsLoading(false)
    if (eventSourceRef.current) {
      eventSourceRef.current.close()
    }
  }, [])

  return {
    messages,
    logEntries,
    isLoading,
    error,
    isAwaitingApproval,
    ticketState,
    sendMessage,
    handleApproval,
    clearConversation,
  }
}
