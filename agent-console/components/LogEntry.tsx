"use client"

import { useState } from "react"
import { Brain, Book, Database, Wrench, Lightbulb, Target, Eye, CheckCircle2, Clock, XCircle } from "lucide-react"
import { Button } from "@/components/ui/button"
import type { StreamLogEntry } from "@/hooks/useChatStream"
import JsonModal from "./JsonModal"

interface LogEntryProps {
  entry: StreamLogEntry
}

const iconMap = {
  brain: Brain,
  book: Book,
  database: Database,
  wrench: Wrench,
  lightbulb: Lightbulb,
  target: Target,
}

const statusConfig = {
  in_progress: {
    color: "var(--google-yellow)",
    bgColor: "#FEF7E0",
    label: "In Progress",
    icon: Clock,
  },
  completed: {
    color: "var(--google-green)",
    bgColor: "#E8F5E8",
    label: "Completed",
    icon: CheckCircle2,
  },
  error: {
    color: "var(--google-red)",
    bgColor: "#FCE8E6",
    label: "Error",
    icon: XCircle,
  },
}

export default function LogEntry({ entry }: LogEntryProps) {
  const [showModal, setShowModal] = useState(false)

  const IconComponent = iconMap[entry.icon] || Wrench
  const statusStyle = statusConfig[entry.status]
  const StatusIcon = statusStyle.icon

  const hasDetails = entry.input || entry.output

  return (
    <>
      <div className="bg-white rounded-lg p-4 google-shadow" style={{ border: "1px solid var(--google-grey-200)" }}>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div
              className="p-2 rounded-full flex items-center justify-center"
              style={{ backgroundColor: statusStyle.bgColor }}
            >
              <IconComponent className="w-5 h-5" style={{ color: statusStyle.color }} />
            </div>

            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <span
                  className="inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium"
                  style={{
                    backgroundColor: statusStyle.bgColor,
                    color: statusStyle.color,
                  }}
                >
                  <StatusIcon className="w-3 h-3" />[{statusStyle.label}]
                </span>
                <span className="text-sm font-medium" style={{ color: "var(--google-grey-800)" }}>
                  {entry.title}
                </span>
              </div>
              <div className="text-xs" style={{ color: "var(--google-grey-600)" }}>
                {entry.timestamp.toLocaleTimeString()}
              </div>
            </div>
          </div>

          {hasDetails && (
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowModal(true)}
              className="hover:bg-gray-100"
              style={{ color: "var(--google-blue)" }}
            >
              <Eye className="w-4 h-4 mr-1" />
              Details
            </Button>
          )}
        </div>
      </div>

      <JsonModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        title={`${entry.title} - Details`}
        data={{ input: entry.input, output: entry.output }}
      />
    </>
  )
}
