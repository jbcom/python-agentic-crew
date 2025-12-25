# vendor-connectors Integration Guide

This guide explains how `agentic-crew` integrates with the [vendor-connectors](https://github.com/jbcom/vendor-connectors) repository to enable AI-powered connector generation and tool sharing.

## Overview

The integration between `agentic-crew` and `vendor-connectors` is bidirectional:

1. **vendor-connectors → agentic-crew**: Uses agentic-crew as a dev dependency to generate connectors via AI crews
2. **agentic-crew → vendor-connectors**: Can use connectors from vendor-connectors as tools in crews

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    vendor-connectors                             │
│                                                                  │
│  .crewai/                                                        │
│  ├── manifest.yaml          # Crew definitions                  │
│  ├── crews/                                                      │
│  │   └── connector_builder/ # Generates HTTP connectors         │
│  │       ├── agents.yaml                                        │
│  │       └── tasks.yaml                                         │
│  └── knowledge/                                                  │
│      └── api_patterns/      # API documentation patterns        │
│                                                                  │
│  src/vendor_connectors/                                          │
│  ├── meshy/                 # Generated Meshy connector         │
│  │   ├── client.py                                              │
│  │   └── tools.py           # CrewAI/LangGraph/Strands tools    │
│  └── ...                                                         │
└─────────────────────────────────────────────────────────────────┘
                              │
                              │ Uses as dev dependency
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    agentic-crew                                  │
│                                                                  │
│  Core framework-agnostic orchestration                           │
│  - Discovers .crewai/ directories                                │
│  - Loads crew configurations                                     │
│  - Runs on CrewAI/LangGraph/Strands                             │
│  - CLI with JSON output for integration                          │
└─────────────────────────────────────────────────────────────────┘
```

## Setup

### 1. Add agentic-crew to vendor-connectors

In `vendor-connectors/pyproject.toml`:

```toml
[project.optional-dependencies]
# Development dependencies for AI crews
crews = [
    "agentic-crew[crewai]>=0.1.0",  # Use CrewAI for crew execution
]
```

Install with:
```bash
cd vendor-connectors
uv sync --extra crews
```

### 2. Create .crewai/ Directory Structure

Create the crew configuration in vendor-connectors:

```
vendor-connectors/
├── .crewai/
│   ├── manifest.yaml
│   ├── crews/
│   │   └── connector_builder/
│   │       ├── agents.yaml
│   │       └── tasks.yaml
│   └── knowledge/
│       └── api_patterns/
│           ├── rest_api_patterns.md
│           └── authentication_patterns.md
└── ...
```

### 3. Configure manifest.yaml

```yaml
# vendor-connectors/.crewai/manifest.yaml
name: vendor-connectors
version: "1.0"
description: AI crews for vendor connector generation

llm:
  provider: anthropic
  model: claude-sonnet-4-20250514

crews:
  connector_builder:
    description: Generate HTTP connector from API documentation
    agents: crews/connector_builder/agents.yaml
    tasks: crews/connector_builder/tasks.yaml
    knowledge:
      - knowledge/api_patterns
```

## Usage Workflows

### Workflow 1: Generate a Connector

Use the `connector_builder` crew to generate a new connector from API docs:

```bash
# From vendor-connectors directory
agentic-crew run vendor-connectors connector_builder \
  --input '{"api_docs_url": "https://docs.meshy.ai/en", "vendor_name": "meshy"}'
```

**Output**: Generated connector code in `/tmp/connector-output/meshy/`

**Review and integrate**:
```bash
# 1. Review generated code
ls -la /tmp/connector-output/meshy/

# 2. Copy to vendor-connectors
cp -r /tmp/connector-output/meshy/ src/vendor_connectors/

# 3. Add tests
# 4. Submit PR
```

### Workflow 2: JSON Output for Programmatic Integration

Use the `--json` flag for integration with other tools:

```bash
agentic-crew run vendor-connectors connector_builder \
  --input '{"api_docs_url": "https://docs.example.com"}' \
  --json | jq '.'
```

**Output**:
```json
{
  "success": true,
  "output": "Generated connector code for Example API...",
  "framework_used": "crewai",
  "duration_ms": 45230
}
```

### Workflow 3: TypeScript Integration (via agentic-control)

If vendor-connectors has a TypeScript component, use agentic-control:

```typescript
import { CrewTool } from 'agentic-control';

const crewTool = new CrewTool();

const result = await crewTool.invokeCrew({
  package: 'vendor-connectors',
  crew: 'connector_builder',
  input: JSON.stringify({
    api_docs_url: 'https://docs.meshy.ai/en',
    vendor_name: 'meshy'
  }),
});

console.log('Generated connector:', result.output);
```

## Connector Builder Crew Example

### agents.yaml

```yaml
# vendor-connectors/.crewai/crews/connector_builder/agents.yaml
api_analyst:
  role: API Documentation Analyst
  goal: Extract API endpoints, parameters, and authentication from docs
  backstory: >
    Expert at reading API documentation and identifying patterns.
    You understand REST, GraphQL, and various authentication schemes.

connector_engineer:
  role: Senior Python Engineer
  goal: Generate clean, well-typed HTTP connector code
  backstory: >
    Expert Python developer with deep knowledge of httpx, pydantic,
    and type hints. You write production-quality connectors.

qa_engineer:
  role: Quality Assurance Engineer
  goal: Review connector code for correctness and completeness
  backstory: >
    Specialist in API client testing. You ensure connectors handle
    errors gracefully and follow best practices.
```

### tasks.yaml

```yaml
# vendor-connectors/.crewai/crews/connector_builder/tasks.yaml
analyze_api:
  description: >
    Analyze the API documentation at {api_docs_url}.
    Extract all endpoints, request/response schemas, and auth requirements.
  expected_output: >
    Structured JSON with endpoints, parameters, and schemas
  agent: api_analyst

generate_connector:
  description: >
    Generate Python connector code using httpx and pydantic.
    Include proper error handling and type hints.
    Output to /tmp/connector-output/{vendor_name}/
  expected_output: >
    Complete Python module with client.py and tools.py
  agent: connector_engineer

review_code:
  description: >
    Review the generated connector for:
    - Type safety
    - Error handling
    - Documentation
    - Test coverage gaps
  expected_output: >
    List of issues found and recommendations
  agent: qa_engineer
```

## Tool Sharing Pattern

vendor-connectors can export tools that agentic-crew crews can use.

### Export Tools from vendor-connectors

```python
# src/vendor_connectors/meshy/tools.py
from typing import Literal

def get_tools(framework: Literal["crewai", "langgraph", "strands"] = "crewai"):
    """Get Meshy tools in the specified framework format.
    
    Args:
        framework: Target framework for tools
        
    Returns:
        List of tools in framework-native format
    """
    if framework == "crewai":
        from crewai_tools import Tool
        
        return [
            Tool(
                name="meshy_text3d_generate",
                description="Generate 3D model from text prompt",
                func=lambda prompt: generate_3d_model(prompt),
            ),
            # ... more tools
        ]
    elif framework == "langgraph":
        from langchain_core.tools import StructuredTool
        
        return [
            StructuredTool.from_function(
                name="meshy_text3d_generate",
                description="Generate 3D model from text prompt",
                func=lambda prompt: generate_3d_model(prompt),
            ),
            # ... more tools
        ]
    # ... etc
```

### Use in agentic-crew Crews

```yaml
# In any agentic-crew manifest.yaml
crews:
  game_asset_generator:
    description: Generate 3D game assets
    agents: crews/game_asset_generator/agents.yaml
    tasks: crews/game_asset_generator/tasks.yaml
    tools:
      # Import tools from vendor-connectors
      - vendor_connectors.meshy.tools:get_tools
```

Or programmatically:

```python
from vendor_connectors.meshy.tools import get_tools
from agentic_crew.core.loader import create_agent_from_config

# Get tools for your framework
meshy_tools = get_tools(framework="crewai")

# Add to agent
agent = create_agent_from_config(
    "asset_generator",
    agent_config,
    tools=meshy_tools
)
```

## Advanced: Extending Crews

vendor-connectors can reference crews from agentic-crew:

```yaml
# vendor-connectors/.crewai/manifest.yaml
crews:
  enhanced_builder:
    description: Extended connector builder with validation
    extends: agentic-crew:connector_builder  # Reference base crew
    additional_tasks:
      - validate_openapi  # Add vendor-connectors specific tasks
```

## CLI Reference

### List Available Crews

```bash
# List all crews in vendor-connectors
agentic-crew list vendor-connectors

# JSON output
agentic-crew list vendor-connectors --json
```

### Show Crew Details

```bash
# Get detailed crew information
agentic-crew info vendor-connectors connector_builder

# JSON output for integration
agentic-crew info vendor-connectors connector_builder --json
```

### Run a Crew

```bash
# With input string
agentic-crew run vendor-connectors connector_builder \
  --input '{"api_docs_url": "https://docs.api.com"}'

# From input file
agentic-crew run vendor-connectors connector_builder \
  --file api_spec.yaml

# Force specific framework
agentic-crew run vendor-connectors connector_builder \
  --input '...' \
  --framework langgraph

# JSON output
agentic-crew run vendor-connectors connector_builder \
  --input '...' \
  --json
```

## Exit Codes

The CLI uses standard exit codes for integration:

- `0` - Success
- `1` - Crew execution failed
- `2` - Configuration error (package/crew not found)

Example in CI/CD:

```bash
if agentic-crew run vendor-connectors connector_builder --input '...' --json > result.json; then
  echo "Connector generated successfully"
  jq '.output' result.json
else
  echo "Generation failed"
  jq '.error' result.json
  exit 1
fi
```

## Environment Variables

Required environment variables:

```bash
# For Claude LLM (primary)
export ANTHROPIC_API_KEY="sk-ant-api03-..."

# Optional: OpenRouter fallback
export OPENROUTER_API_KEY="sk-or-v1-..."

# For vendor-specific tools (if using Meshy)
export MESHY_API_KEY="msy_..."
```

## Testing

### Test Connector Generation

```bash
# Test that connector_builder crew works
cd vendor-connectors
uv run pytest tests/test_connector_builder.py -v

# Test generated connector
cd /tmp/connector-output/meshy
uv run pytest tests/ -v
```

### Integration Test Example

```python
# vendor-connectors/tests/test_connector_builder.py
import json
import subprocess

def test_connector_builder_cli():
    """Test connector generation via CLI."""
    result = subprocess.run(
        [
            "agentic-crew", "run",
            "vendor-connectors", "connector_builder",
            "--input", '{"api_docs_url": "https://docs.meshy.ai/en"}',
            "--json"
        ],
        capture_output=True,
        text=True
    )
    
    assert result.returncode == 0
    output = json.loads(result.stdout)
    assert output["success"] is True
    assert "meshy" in output["output"].lower()
```

## Best Practices

### 1. Version Pinning

Pin agentic-crew versions for reproducibility:

```toml
crews = ["agentic-crew[crewai]==0.1.0"]
```

### 2. Knowledge Base Organization

Structure knowledge for reuse:

```
.crewai/knowledge/
├── api_patterns/
│   ├── rest_best_practices.md
│   ├── authentication_schemes.md
│   └── error_handling.md
├── code_patterns/
│   ├── httpx_usage.md
│   └── pydantic_models.md
└── vendor_specific/
    ├── meshy_api.md
    └── openai_api.md
```

### 3. Framework-Agnostic Tools

When exporting tools, support all frameworks:

```python
def get_tools(framework="crewai"):
    """Support crewai, langgraph, strands."""
    # ... implementation
```

### 4. Error Handling

Always handle crew failures gracefully:

```bash
if ! agentic-crew run vendor-connectors connector_builder --input '...' --json > result.json; then
  echo "Crew failed, check result.json for details"
  jq '.error' result.json
  exit 1
fi
```

## Troubleshooting

### Issue: Package not found

**Error**: `Package 'vendor-connectors' not found`

**Solution**: Ensure `.crewai/manifest.yaml` exists in vendor-connectors root:

```bash
ls -la vendor-connectors/.crewai/manifest.yaml
```

### Issue: Crew not found

**Error**: `Crew 'connector_builder' not found`

**Solution**: Check manifest.yaml has the crew defined:

```yaml
crews:
  connector_builder:  # Must match exactly
    description: ...
```

### Issue: Framework not available

**Error**: `No AI frameworks installed`

**Solution**: Install a framework:

```bash
uv sync --extra crews  # Installs crewai
# or
pip install 'agentic-crew[crewai]'
```

### Issue: Tool import fails

**Error**: `ModuleNotFoundError: No module named 'vendor_connectors'`

**Solution**: Install vendor-connectors:

```bash
pip install vendor-connectors[meshy]
```

## Related Documentation

- [agentic-crew README](../README.md) - Main documentation
- [Architecture](./ARCHITECTURE.md) - Technical architecture
- [Quick Start](./QUICKSTART.md) - Getting started guide
- [vendor-connectors](https://github.com/jbcom/vendor-connectors) - Connector library

## See Also

- Issue [#37](https://github.com/jbcom/agentic-crew/issues/37) - connector_builder crew implementation
- Issue [#17](https://github.com/jbcom/agentic-crew/issues/17) - Integration points
- Issue [#18](https://github.com/jbcom/agentic-crew/issues/18) - Tool sharing pattern
- Issue [#33](https://github.com/jbcom/agentic-crew/issues/33) - JSON CLI output
