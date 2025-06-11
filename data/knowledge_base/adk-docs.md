# Agent Development Kit

**Source URL:** https://google.github.io/adk-docs/

---

Google I/O'25 - ADK updates

Big news!

* Introducing **[Java ADK v0.1.0](https://github.com/google/adk-java/)**, extending agent capabilities to the Java ecosystem.
* **[Python ADK](https://github.com/google/adk-python/)** is officially v1.0.0 offering stability for production-ready agents.

![Agent Development Kit Logo](assets/agent-development-kit.png)

# Agent Development Kit

## What is Agent Development Kit?[¶](#what-is-agent-development-kit "Permanent link")

Agent Development Kit (ADK) is a flexible and modular framework for **developing
and deploying AI agents**. While optimized for Gemini and the Google ecosystem,
ADK is **model-agnostic**, **deployment-agnostic**, and is built for
**compatibility with other frameworks**. ADK was designed to make agent
development feel more like software development, to make it easier for
developers to create, deploy, and orchestrate agentic architectures that range
from simple tasks to complex workflows.

Get started:

PythonJava

`pip install google-adk`

pom.xml

```
<dependency>
    <groupId>com.google.adk</groupId>
    <artifactId>google-adk</artifactId>
    <version>0.1.0</version>
</dependency>

```

build.gradle

```
dependencies {
    implementation 'com.google.adk:google-adk:0.1.0'
}

```

[Quickstart](get-started/quickstart/)
[Tutorials](tutorials/)
[Sample Agents](http://github.com/google/adk-samples)
[API Reference](api-reference/)
[Contribute ❤️](contributing-guide/)

---

## Learn more[¶](#learn-more "Permanent link")

[Watch "Introducing Agent Development Kit"!](https://www.youtube.com/watch?v=zgrOwow_uTQ target= "_blank\" rel=\"noopener noreferrer")

* **Flexible Orchestration**

  ---

  Define workflows using workflow agents (`Sequential`, `Parallel`, `Loop`)
  for predictable pipelines, or leverage LLM-driven dynamic routing
  (`LlmAgent` transfer) for adaptive behavior.

  [**Learn about agents**](agents/)
* **Multi-Agent Architecture**

  ---

  Build modular and scalable applications by composing multiple specialized
  agents in a hierarchy. Enable complex coordination and delegation.

  [**Explore multi-agent systems**](agents/multi-agents/)
* **Rich Tool Ecosystem**

  ---

  Equip agents with diverse capabilities: use pre-built tools (Search, Code
  Exec), create custom functions, integrate 3rd-party libraries (LangChain,
  CrewAI), or even use other agents as tools.

  [**Browse tools**](tools/)
* **Deployment Ready**

  ---

  Containerize and deploy your agents anywhere – run locally, scale with
  Vertex AI Agent Engine, or integrate into custom infrastructure using Cloud
  Run or Docker.

  [**Deploy agents**](deploy/)
* **Built-in Evaluation**

  ---

  Systematically assess agent performance by evaluating both the final
  response quality and the step-by-step execution trajectory against
  predefined test cases.

  [**Evaluate agents**](evaluate/)
* **Building Safe and Secure Agents**

  ---

  Learn how to building powerful and trustworthy agents by implementing
  security and safety patterns and best practices into your agent's design.

  [**Safety and Security**](safety/)