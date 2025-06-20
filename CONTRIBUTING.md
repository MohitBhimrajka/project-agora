# Contributing to Project Agora

Thank you for your interest in contributing to Project Agora! This guide will help you get started with contributing to this Agent Development Kit framework.

## 🚀 Getting Started

### Prerequisites

- Python 3.11 or higher
- Poetry for dependency management
- Google Cloud SDK (`gcloud`)
- A Google Cloud Project with billing enabled

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/project-agora.git
cd project-agora
   ```

2. **Install Dependencies**
   ```bash
   make install
   # or manually:
   poetry install
   ```

3. **Set Up Environment**
   ```bash
   make setup
   # or manually:
   ./setup_environment.sh
   ```

## 📋 How to Contribute

### Reporting Bugs

When reporting bugs, please include:

- **Clear description** of what went wrong
- **Steps to reproduce** the issue
- **Environment details** (OS, Python version, etc.)
- **Error messages** if any

**Simple Bug Report Template:**
```markdown
**What happened:**
Brief description of the bug

**How to reproduce:**
1. Run this command...
2. Do this action...
3. See this error...

**Environment:**
- OS: [e.g., macOS, Ubuntu]
- Python: [e.g., 3.11.5]

**Error (if any):**
[Paste error message here]
```

### Suggesting Features

For feature requests:
- **Describe the feature** clearly
- **Explain why it would be useful**
- **Suggest how it might work** (if you have ideas)

### Making Code Changes

#### Simple Workflow

1. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make Your Changes**
   - Follow the existing code style
   - Keep changes focused and small
   - Add comments for complex logic

3. **Test Locally**
   ```bash
   make run
   # Try out your changes to make sure they work
   ```

4. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add new feature: brief description"
   git push origin feature/your-feature-name
   ```

5. **Create Pull Request**
   - Use a clear title
   - Describe what you changed and why

## 📝 Code Style Guidelines

### Keep It Simple
- Use clear, descriptive variable names
- Add comments for complex logic
- Follow the existing code patterns you see in the project
- Maximum line length: 127 characters

### Good Example
```python
def create_new_agent(agent_name: str, tools: list[str]) -> Agent:
    """Creates a new agent with the specified tools."""
    if not agent_name:
        raise ValueError("Agent name cannot be empty")
    
    # Create the agent with default settings
    agent = Agent(name=agent_name, tools=tools)
    return agent
```

### Commit Messages
Keep them simple and clear:
- `Add new code generation feature`
- `Fix BigQuery connection issue`
- `Update documentation for setup`

## 🏗️ Project Structure

When adding new components:

**For new agents:**
```
project_agora/sub_agents/your_agent/
├── __init__.py
├── agent.py          # Main agent definition
└── README.md         # What this agent does
```

**For new tools:**
```
project_agora/tools/
├── _your_tools.py     # Your new tools
└── tools.py           # Add imports here
```

## 🎯 Areas Where We Need Help

### Easy Contributions
- **Documentation**: Improve README sections, add examples
- **Bug Fixes**: Fix small issues you encounter
- **New Tools**: Add integrations with other services
- **Examples**: Create usage examples for different scenarios

### Medium Difficulty
- **New Agents**: Create specialized agents for specific tasks
- **UI Improvements**: Enhance the web interface
- **Error Handling**: Make error messages more helpful

### Advanced
- **Performance**: Optimize slow operations
- **Cloud Integration**: Add support for other cloud providers
- **Architecture**: Improve the overall system design

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **GitHub Discussions**: For questions and ideas
- **Look at existing code**: Often the best way to understand how things work

## 🏆 Recognition

Contributors are recognized in:
- The project's contributor list
- Release notes for significant contributions

## 📝 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Don't worry about making everything perfect!** Small improvements are welcome, and we're happy to help you refine your contributions through the pull request process. 