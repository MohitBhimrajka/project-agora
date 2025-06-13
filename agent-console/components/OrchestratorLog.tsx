"use client"

import { Info } from "lucide-react"
import LogEntry from "./LogEntry"
import Tooltip from "./Tooltip"
import type { useChatStream } from "@/hooks/useChatStream"

interface OrchestratorLogProps {
  streamData: ReturnType<typeof useChatStream>
}

export default function OrchestratorLog({ streamData }: OrchestratorLogProps) {
  const { logEntries } = streamData

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header */}
      <div
        className="p-4 border-b"
        style={{ backgroundColor: "var(--google-grey-100)", borderColor: "var(--google-grey-200)" }}
      >
        <div className="flex items-center gap-2">
          <h1 className="text-lg font-medium" style={{ color: "var(--google-grey-800)" }}>
            Live "Orchestrator's Log"
          </h1>
          <Tooltip content="This log shows the real-time execution of the ADK orchestrator and its specialized sub-agents.">
            <Info className="w-4 h-4 cursor-help" style={{ color: "var(--google-grey-500)" }} />
          </Tooltip>
        </div>
      </div>

      {/* Log Entries */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3">
        {logEntries.length === 0 ? (
          <div className="text-center text-gray-500 mt-8">
            <p className="text-sm">Agent activity will appear here...</p>
          </div>
        ) : (
          logEntries.map((entry) => <LogEntry key={entry.id} entry={entry} />)
        )}
      </div>
    </div>
  )
}
