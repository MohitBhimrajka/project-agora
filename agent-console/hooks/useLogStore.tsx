"use client"

import type React from "react"

import { createContext, useContext, useReducer, type ReactNode } from "react"

export interface LogEntry {
  id: string
  icon: "brain" | "book" | "database" | "wrench" | "lightbulb" | "target"
  title: string
  status: "in_progress" | "completed" | "error"
  timestamp: Date
  details?: {
    input?: any
    output?: any
  }
}

interface LogState {
  entries: LogEntry[]
}

type LogAction =
  | { type: "ADD_ENTRY"; payload: LogEntry }
  | { type: "UPDATE_ENTRY"; payload: { id: string; updates: Partial<LogEntry> } }

const initialEntries: LogEntry[] = [
  {
    id: "1",
    icon: "target",
    title: "Tool: create_ticket",
    status: "in_progress",
    timestamp: new Date(Date.now() - 5000),
  },
  {
    id: "2",
    icon: "brain",
    title: "Agent: ticket_analysis_agent",
    status: "completed",
    timestamp: new Date(Date.now() - 10000),
  },
  {
    id: "3",
    icon: "lightbulb",
    title: "Agent: knowledge_retrieval_agent",
    status: "in_progress",
    timestamp: new Date(Date.now() - 8000),
  },
  {
    id: "4",
    icon: "database",
    title: "Agent: db_retrieval_agent",
    status: "completed",
    timestamp: new Date(Date.now() - 12000),
  },
  {
    id: "5",
    icon: "target",
    title: "Agent: code_generator_agent (Phase 1: Plan)",
    status: "completed",
    timestamp: new Date(Date.now() - 15000),
  },
  {
    id: "6",
    icon: "wrench",
    title: "Tool: generate_diagram_from_mermaid",
    status: "completed",
    timestamp: new Date(Date.now() - 18000),
  },
  {
    id: "7",
    icon: "target",
    title: "Tool: generate_diagram_from_mermaid",
    status: "completed",
    timestamp: new Date(Date.now() - 20000),
  },
]

const initialState: LogState = {
  entries: initialEntries,
}

function logReducer(state: LogState, action: LogAction): LogState {
  switch (action.type) {
    case "ADD_ENTRY":
      return {
        ...state,
        entries: [action.payload, ...state.entries],
      }
    case "UPDATE_ENTRY":
      return {
        ...state,
        entries: state.entries.map((entry) =>
          entry.id === action.payload.id ? { ...entry, ...action.payload.updates } : entry,
        ),
      }
    default:
      return state
  }
}

const LogContext = createContext<{
  state: LogState
  dispatch: React.Dispatch<LogAction>
  addEntry: (entry: Omit<LogEntry, "id" | "timestamp">) => void
  updateEntry: (id: string, updates: Partial<LogEntry>) => void
} | null>(null)

export function LogProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(logReducer, initialState)

  const addEntry = (entry: Omit<LogEntry, "id" | "timestamp">) => {
    const newEntry: LogEntry = {
      ...entry,
      id: Date.now().toString(),
      timestamp: new Date(),
    }
    dispatch({ type: "ADD_ENTRY", payload: newEntry })
  }

  const updateEntry = (id: string, updates: Partial<LogEntry>) => {
    dispatch({ type: "UPDATE_ENTRY", payload: { id, updates } })
  }

  return <LogContext.Provider value={{ state, dispatch, addEntry, updateEntry }}>{children}</LogContext.Provider>
}

export function useLogStore() {
  const context = useContext(LogContext)
  if (!context) {
    throw new Error("useLogStore must be used within a LogProvider")
  }
  return context
}
