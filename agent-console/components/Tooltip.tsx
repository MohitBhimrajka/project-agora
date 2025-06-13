"use client"

import { useState, type ReactNode } from "react"

interface TooltipProps {
  content: string
  children: ReactNode
}

export default function Tooltip({ content, children }: TooltipProps) {
  const [isVisible, setIsVisible] = useState(false)

  return (
    <div className="relative inline-block">
      <div onMouseEnter={() => setIsVisible(true)} onMouseLeave={() => setIsVisible(false)}>
        {children}
      </div>
      {isVisible && (
        <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 text-sm text-white bg-gray-900 rounded-lg shadow-lg whitespace-nowrap z-50">
          {content}
          <div className="absolute top-full left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-900"></div>
        </div>
      )}
    </div>
  )
}
