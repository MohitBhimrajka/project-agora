"use client"
import ChatWindow from "@/components/ChatWindow"
import OrchestratorLog from "@/components/OrchestratorLog"
import Header from "@/components/Header"
import Footer from "@/components/Footer"
import { useChatStream } from "@/hooks/useChatStream"

export default function MainConsole() {
  const streamData = useChatStream()
  const apiUrl = process.env.NEXT_PUBLIC_API_URL

  return (
    <div className="min-h-screen flex flex-col" style={{ backgroundColor: "var(--google-grey-50)" }}>
      <Header isConnected={!streamData.error} apiUrl={apiUrl} />

      <div className="flex flex-1">
        {/* Left Pane - Chat Window */}
        <div className="flex-1" style={{ borderRight: "1px solid var(--google-grey-200)" }}>
          <ChatWindow streamData={streamData} />
        </div>

        {/* Right Pane - Orchestrator Log */}
        <div className="flex-1">
          <OrchestratorLog streamData={streamData} />
        </div>
      </div>

      <Footer />
    </div>
  )
}
