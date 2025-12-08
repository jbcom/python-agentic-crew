# agentic-crew

**Framework-agnostic AI crew orchestration** - declare once, run on CrewAI, LangGraph, Strands, or single-agent CLI tools.

## Why agentic-crew?

The AI agent ecosystem is fragmented:
- **Multi-agent frameworks** (CrewAI, LangGraph, Strands) - Different APIs for the same concepts
- **Single-agent CLI tools** (aider, claude-code, ollama) - Each with different invocation patterns

agentic-crew solves this with:
1. **Universal multi-agent format** - Define once, run on any framework
2. **Universal CLI runner** - Single interface for all coding CLI tools
3. **Smart orchestration** - Use the right tool for the job automatically

## Installation

```bash
# Core (no framework - auto-detects at runtime)
pip install agentic-crew

# With specific framework
pip install agentic-crew[crewai]      # CrewAI (recommended)
pip install agentic-crew[langgraph]   # LangGraph
pip install agentic-crew[strands]     # AWS Strands

# All frameworks
pip install agentic-crew[ai]
```

## Quick Start

### 1. Define a Crew (YAML)

```yaml
# .crewai/manifest.yaml
name: my-package
version: "1.0"

crews:
  analyzer:
    description: Analyze codebases
    agents: crews/analyzer/agents.yaml
    tasks: crews/analyzer/tasks.yaml
```

```yaml
# crews/analyzer/agents.yaml
code_reviewer:
  role: Senior Code Reviewer
  goal: Find bugs and improvements
  backstory: Expert at code analysis
```

```yaml
# crews/analyzer/tasks.yaml
review_code:
  description: Review the provided code for issues
  expected_output: List of findings with severity
  agent: code_reviewer
```

### 2. Run It

```python
from agentic_crew import run_crew

# Auto-detects best framework
result = run_crew("my-package", "analyzer", inputs={"code": "..."})
```

Or from CLI:

```bash
agentic-crew run my-package analyzer --input "Review this code: ..."
```

## Single-Agent CLI Runners

For simpler tasks that don't need multi-agent collaboration, agentic-crew supports direct execution via CLI-based coding tools:

### Available Runners

```bash
# List available single-agent runners
agentic-crew list-runners

# Shows:
# ✅ aider: AI pair programming in your terminal
# ✅ claude-code: Anthropic's AI coding agent
# ✅ codex: OpenAI's local coding agent
# ✅ ollama: Free local LLM execution (no API key needed!)
# ✅ kiro: AWS AI-assisted development CLI
# ✅ goose: Block's extensible AI coding agent
```

### Usage Examples

```bash
# Quick code fixes with Aider
agentic-crew run --runner aider --input "Add error handling to auth.py"

# Code generation with Claude Code
agentic-crew run --runner claude-code --input "Refactor the database module"

# Free local execution with Ollama
agentic-crew run --runner ollama --input "Fix the bug in utils.py" --model deepseek-coder

# With specific model
agentic-crew run --runner aider --input "Add tests" --model gpt-4o
```

### When to Use Single-Agent vs Multi-Agent

| Use Case | Best Choice |
|----------|-------------|
| Complex task with multiple steps requiring collaboration | Multi-agent crew (CrewAI/LangGraph/Strands) |
| Sequential coding tasks, quick edits | Single-agent CLI (aider, claude-code) |
| Simple file generation or code fixes | Single-agent CLI |
| Local development and testing | Single-agent CLI (especially ollama - free!) |
| Tasks requiring planning and delegation | Multi-agent crew |

### Custom CLI Runners

Define your own CLI tool in a config:

```yaml
# my-custom-runner.yaml
command: "my-coding-assistant"
task_flag: "--task"
auth_env:
  - "MY_API_KEY"
auto_approve: "--yes"
structured_output: "--json"
timeout: 600
```

Then use it:

```python
import yaml
from agentic_crew.core.decomposer import get_cli_runner

# Load your custom config from YAML
with open("my-custom-runner.yaml") as f:
    custom_config = yaml.safe_load(f)

runner = get_cli_runner(custom_config)
result = runner.run("Fix the bug")
```

## Framework Decomposition

The magic happens in `core/decomposer.py`:

```python
from agentic_crew.core.decomposer import detect_framework, get_runner

# See what's available
framework = detect_framework()  # "crewai", "langgraph", or "strands"

# Get a runner
runner = get_runner()  # Auto-selects best
runner = get_runner("langgraph")  # Force specific

# Build and run
crew = runner.build_crew(config)
result = runner.run(crew, inputs)
```

### Framework Priority

1. **CrewAI** (if installed) - Most features, best for complex crews
2. **LangGraph** (if CrewAI unavailable) - Good for flow-based logic
3. **Strands** (fallback) - Lightweight, minimal deps

## Package Integration

Any package can define crews in a `.crewai/` directory:

```
my-package/
├── .crewai/
│   ├── manifest.yaml
│   ├── knowledge/
│   │   └── domain_docs/
│   └── crews/
│       └── my_crew/
│           ├── agents.yaml
│           └── tasks.yaml
└── src/
```

Then run:

```bash
agentic-crew run my-package my_crew --input "..."
```

## Use Cases

### 1. Connector Builder (vendor-connectors)

A crew that scrapes API docs and generates HTTP connectors:

```bash
agentic-crew run vendor-connectors connector_builder \
  --input '{"api_docs_url": "https://docs.meshy.ai/en", "vendor_name": "meshy"}'
```

See [vendor-connectors Integration Guide](docs/VENDOR_CONNECTORS_INTEGRATION.md) for details.

### 2. Code Generation (any project)

Define crews for your specific domain and run them on any framework.

## Development

```bash
# Install with dev deps
uv sync --extra dev --extra tests --extra crewai

# Run tests
uv run pytest tests/ -v

# Lint
uvx ruff check src/ tests/ --fix
```

## Related Projects

- [vendor-connectors](https://github.com/jbcom/vendor-connectors) - HTTP connector library (uses agentic-crew for development)
- [CrewAI](https://github.com/crewAIInc/crewAI) - Original crew framework
- [LangGraph](https://github.com/langchain-ai/langgraph) - Graph-based agents
- [Strands](https://github.com/strands-agents/strands-agents-python) - AWS agent framework

## Documentation

- [Quick Start](docs/QUICKSTART.md) - Get started quickly
- [Architecture](docs/ARCHITECTURE.md) - Technical architecture
- [vendor-connectors Integration](docs/VENDOR_CONNECTORS_INTEGRATION.md) - Integration guide for vendor-connectors

## License

MIT
