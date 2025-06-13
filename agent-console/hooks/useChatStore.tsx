"use client"

import type React from "react"

import { createContext, useContext, useReducer, type ReactNode } from "react"

export interface ChatMessage {
  id: string
  type: "text" | "code" | "image" | "prompt" | "approval"
  content: string
  timestamp: Date
  sender: "user" | "agent"
  language?: string
  options?: string[]
  planText?: string
  diagramUrl?: string
  filename?: string
}

interface ChatState {
  messages: ChatMessage[]
  isAwaitingApproval: boolean
  inputDisabled: boolean
}

type ChatAction =
  | { type: "ADD_MESSAGE"; payload: ChatMessage }
  | { type: "SET_AWAITING_APPROVAL"; payload: boolean }
  | { type: "SET_INPUT_DISABLED"; payload: boolean }

const initialState: ChatState = {
  messages: [
    {
      id: "1",
      type: "text",
      content: "Write me an agent that uses a custom tool to get the current weather.",
      timestamp: new Date(),
      sender: "user",
    },
    {
      id: "2",
      type: "text",
      content:
        "Thank you for your request. I have created a developer request and will now begin the analysis process.",
      timestamp: new Date(),
      sender: "agent",
    },
    {
      id: "3",
      type: "text",
      content:
        'I\'ve analyzed your request and categorized it as a "Code Generation" issue. I will now search our knowledge base and past tickets for relevant information.',
      timestamp: new Date(),
      sender: "agent",
    },
    {
      id: "4",
      type: "prompt",
      content:
        "My search is complete. I found several relevant documents and past tickets. I am now ready to formulate a solution. Shall I proceed?",
      timestamp: new Date(),
      sender: "agent",
      options: ["Yes, Proceed"],
    },
    {
      id: "5",
      type: "approval",
      content: "Architecture Approval",
      timestamp: new Date(),
      sender: "agent",
      planText:
        "Plan: I will build a simple agent with one custom tool, get_current_weather. This tool will call an external weather API to fetch current weather data for a specified location.",
      diagramUrl: "/placeholder.svg?height=200&width=300",
    },
    {
      id: "6",
      type: "code",
      content: "// code here",
      timestamp: new Date(),
      sender: "agent",
      filename: "weather_agent.py",
    },
    {
      id: "7",
      type: "text",
      content: "Here is the code for the agent.",
      timestamp: new Date(),
      sender: "agent",
    },
  ],
  isAwaitingApproval: true,
  inputDisabled: true,
}

function chatReducer(state: ChatState, action: ChatAction): ChatState {
  switch (action.type) {
    case "ADD_MESSAGE":
      return {
        ...state,
        messages: [...state.messages, action.payload],
      }
    case "SET_AWAITING_APPROVAL":
      return {
        ...state,
        isAwaitingApproval: action.payload,
      }
    case "SET_INPUT_DISABLED":
      return {
        ...state,
        inputDisabled: action.payload,
      }
    default:
      return state
  }
}

const ChatContext = createContext<{
  state: ChatState
  dispatch: React.Dispatch<ChatAction>
  addMessage: (message: Omit<ChatMessage, "id" | "timestamp">) => void
  handleApproval: (approved: boolean, feedback?: string) => void
} | null>(null)

export function ChatProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(chatReducer, initialState)

  const addMessage = (message: Omit<ChatMessage, "id" | "timestamp">) => {
    const newMessage: ChatMessage = {
      ...message,
      id: Date.now().toString(),
      timestamp: new Date(),
    }
    dispatch({ type: "ADD_MESSAGE", payload: newMessage })
  }

  const handleApproval = (approved: boolean, feedback?: string) => {
    const message = approved
      ? "Plan approved. Proceeding with implementation."
      : `Plan rejected. ${feedback || "Please revise the approach."}`

    addMessage({
      type: "text",
      content: message,
      sender: "user",
    })

    dispatch({ type: "SET_AWAITING_APPROVAL", payload: false })
    dispatch({ type: "SET_INPUT_DISABLED", payload: false })
  }

  return <ChatContext.Provider value={{ state, dispatch, addMessage, handleApproval }}>{children}</ChatContext.Provider>
}

export function useChatStore() {
  const context = useContext(ChatContext)
  if (!context) {
    throw new Error("useChatStore must be used within a ChatProvider")
  }
  return context
}
