"use client"

import { Cloud, Wifi } from "lucide-react"

interface HeaderProps {
  isConnected?: boolean
  apiUrl?: string
}

export default function Header({ isConnected = true, apiUrl }: HeaderProps) {
  const isDemoMode = !apiUrl || apiUrl.includes("your-adk-copilot-service")

  return (
    <header className="bg-white google-shadow-lg px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          {/* Google Cloud Logo */}
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-green-500 rounded-sm flex items-center justify-center">
              <Cloud className="text-white w-5 h-5" />
            </div>
            <div className="text-xl font-medium" style={{ color: "var(--google-grey-700)" }}>
              <span style={{ color: "var(--google-blue)" }}>Google Cloud</span>
              <span className="mx-2" style={{ color: "var(--google-grey-400)" }}>
                |
              </span>
              <span>ADK Copilot</span>
            </div>
          </div>
        </div>

        {/* Connection Status */}
        <div className="flex items-center gap-2">
          {isDemoMode ? (
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-yellow-100">
              <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
              <span className="text-xs font-medium text-yellow-700">Demo Mode</span>
            </div>
          ) : (
            <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-green-100">
              <Wifi className="w-3 h-3 text-green-600" />
              <span className="text-xs font-medium text-green-700">Connected</span>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
