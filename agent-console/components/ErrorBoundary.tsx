"use client"

import { AlertTriangle, RefreshCw } from "lucide-react"
import { Button } from "@/components/ui/button"

interface ErrorDisplayProps {
  error: string
  onRetry?: () => void
  onClear?: () => void
}

export default function ErrorDisplay({ error, onRetry, onClear }: ErrorDisplayProps) {
  return (
    <div className="p-4 bg-red-50 border border-red-200 rounded-lg mx-4 mb-4">
      <div className="flex items-start gap-3">
        <AlertTriangle className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" />
        <div className="flex-1">
          <h3 className="text-sm font-medium text-red-800 mb-1">Connection Error</h3>
          <p className="text-sm text-red-700 mb-3">{error}</p>
          <div className="flex gap-2">
            {onRetry && (
              <Button size="sm" onClick={onRetry} className="bg-red-600 hover:bg-red-700 text-white">
                <RefreshCw className="w-3 h-3 mr-1" />
                Retry
              </Button>
            )}
            {onClear && (
              <Button size="sm" variant="outline" onClick={onClear} className="border-red-300 text-red-700">
                Clear
              </Button>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
