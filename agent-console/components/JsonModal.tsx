"use client"

import { useEffect } from "react"
import { Button } from "@/components/ui/button"
import { X } from "lucide-react"

interface JsonModalProps {
  isOpen: boolean
  onClose: () => void
  title: string
  data: any
}

export default function JsonModal({ isOpen, onClose, title, data }: JsonModalProps) {
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose()
      }
    }

    if (isOpen) {
      document.addEventListener("keydown", handleEscape)
      document.body.style.overflow = "hidden"
    }

    return () => {
      document.removeEventListener("keydown", handleEscape)
      document.body.style.overflow = "unset"
    }
  }, [isOpen, onClose])

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg google-shadow-lg max-w-4xl w-full max-h-[80vh] flex flex-col">
        <div
          className="flex items-center justify-between p-6 border-b"
          style={{ borderColor: "var(--google-grey-200)" }}
        >
          <h2 className="text-xl font-medium" style={{ color: "var(--google-grey-800)" }}>
            {title}
          </h2>
          <Button onClick={onClose} variant="ghost" size="sm" className="text-gray-500 hover:text-gray-700">
            <X className="w-4 h-4" />
          </Button>
        </div>

        <div className="flex-1 overflow-auto p-6">
          <pre className="bg-gray-900 text-green-400 p-4 rounded-lg text-sm overflow-x-auto font-mono">
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      </div>
    </div>
  )
}
