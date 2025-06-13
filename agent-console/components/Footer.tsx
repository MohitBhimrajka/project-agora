"use client"

export default function Footer() {
  return (
    <footer className="bg-white border-t px-6 py-4" style={{ borderColor: "var(--google-grey-200)" }}>
      <div className="flex items-center justify-center gap-6 text-sm">
        <a href="#" className="hover:underline transition-colors" style={{ color: "var(--google-blue)" }}>
          Official ADK Docs
        </a>
        <span style={{ color: "var(--google-grey-400)" }}>|</span>
        <a href="#" className="hover:underline transition-colors" style={{ color: "var(--google-blue)" }}>
          Project on GitHub
        </a>
        <span style={{ color: "var(--google-grey-400)" }}>|</span>
        <span style={{ color: "var(--google-grey-600)" }}>Powered by Google ADK</span>
      </div>
    </footer>
  )
}
