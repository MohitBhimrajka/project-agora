# Bidi-streaming(live) in ADK - Agent Development Kit

**Source URL:** https://google.github.io/adk-docs/streaming/

---

# Bidi-streaming(live) in ADK[¶](#bidi-streaminglive-in-adk "Permanent link")

Info

This is an experimental feature. Currrently available in Python.

Info

This is different from server-side streaming or token-leven streaming. This section is for bidi-streaming(live).

Bidi-streaming(live) in ADK adds the low-latency bidirectional voice and video interaction
capability of [Gemini Live API](https://ai.google.dev/gemini-api/docs/live) to
AI agents.

With bidi-streaming(live) mode, you can provide end users with the experience of natural,
human-like voice conversations, including the ability for the user to interrupt
the agent's responses with voice commands. Agents with streaming can process
text, audio, and video inputs, and they can provide text and audio output.

* **Quickstart (Streaming)**

  ---

  In this quickstart, you'll build a simple agent and use streaming in ADK to
  implement low-latency and bidirectional voice and video communication.

  [More information](../get-started/streaming/quickstart-streaming/)
* **Streaming Tools**

  ---

  Streaming tools allows tools (functions) to stream intermediate results back to agents and agents can respond to those intermediate results. For example, we can use streaming tools to monitor the changes of the stock price and have the agent react to it. Another example is we can have the agent monitor the video stream, and when there is changes in video stream, the agent can report the changes.

  [More information](streaming-tools/)
* **Custom Audio Streaming app sample**

  ---

  This article overviews the server and client code for a custom asynchronous web app built with ADK Streaming and FastAPI, enabling real-time, bidirectional audio and text communication with both Server Sent Events (SSE) and WebSockets.

  [More information (SSE)](custom-streaming/) and
   [(WebSockets)](custom-streaming-ws/)
* **Blog post: Google ADK + Vertex AI Live API**

  ---

  This article shows how to use Bidi-streaming (live) in ADK for real-time audio/video streaming. It offers a Python server example using LiveRequestQueue to build custom, interactive AI agents.

  [More information](https://medium.com/google-cloud/google-adk-vertex-ai-live-api-125238982d5e)
* **Shopper's Concierge demo**

  ---

  Learn how streaming in ADK can be used to build a personal shopping
  concierge that understands your personal style and offers tailored
  recommendations.

  [More information](https://youtu.be/LwHPYyw7u6U)
* **Streaming Configurations**

  ---

  There are some configurations you can set for live(streaming) agents.

  [More information](configuration/)