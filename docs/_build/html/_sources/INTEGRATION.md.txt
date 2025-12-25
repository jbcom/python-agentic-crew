# External Integration Guide

> **For TypeScript/Node.js applications integrating with agentic-crew via CLI**

This guide documents how external tools (especially TypeScript/Node.js applications) should integrate with `agentic-crew` via subprocess calls. This follows the **clean language separation principle**:

- `agentic-crew` = Python only (PyPI)
- External consumers = Any language (invoke via CLI)

## Quick Start

```bash
# Install agentic-crew
pip install agentic-crew

# Install with a specific framework
pip install 'agentic-crew[crewai]'
pip install 'agentic-crew[langgraph]'
pip install 'agentic-crew[strands]'

# List available crews (JSON output)
agentic-crew list --json

# Run a crew
agentic-crew run <package> <crew> --input "..." --json
```

## CLI Contract (Stable API)

### Version Compatibility

The CLI contract is versioned and follows semantic versioning:
- **v0.x**: Current development version, JSON schemas may evolve
- **v1.0+**: Stable JSON schemas with backwards compatibility guarantees

### Commands

#### List Crews

```bash
agentic-crew list [package] --json
```

Lists all available crews or crews in a specific package.

**Options:**
- `package` (optional): Filter to a specific package
- `--framework`: Filter by framework (`crewai`, `langgraph`, `strands`)
- `--json`: Output as machine-parseable JSON

**Example:**
```bash
# List all crews
agentic-crew list --json

# List crews in a specific package
agentic-crew list otterfall --json
```

#### Get Crew Info

```bash
agentic-crew info <package> <crew> --json
```

Returns detailed information about a specific crew.

**Options:**
- `--json`: Output as machine-parseable JSON

**Example:**
```bash
agentic-crew info vendor-connectors connector_builder --json
```

#### Run a Crew

```bash
agentic-crew run <package> <crew> --input "..." --json
```

Executes a crew and returns the result.

**Options:**
- `--input`, `-i`: Input specification as string
- `--file`, `-f`: Read input from a file
- `--framework`: Force specific framework (`auto`, `crewai`, `langgraph`, `strands`)
- `--json`: Output as machine-parseable JSON (recommended for integrations)

**Examples:**
```bash
# Run with inline input
agentic-crew run otterfall game_builder --input "Create a QuestComponent" --json

# Run with input from file
agentic-crew run vendor-connectors connector_builder --file api_spec.md --json

# Force specific framework
agentic-crew run mypackage mycrew --input "..." --framework crewai --json
```

## JSON Output Schemas

### CrewListResult

Returned by `agentic-crew list --json`:

```json
{
  "crews": [
    {
      "package": "vendor-connectors",
      "name": "connector_builder",
      "description": "Build HTTP connectors from API documentation",
      "required_framework": null
    },
    {
      "package": "otterfall",
      "name": "game_builder",
      "description": "Build ECS components and game systems",
      "required_framework": "crewai"
    }
  ]
}
```

### CrewInfoResult

Returned by `agentic-crew info <package> <crew> --json`:

```json
{
  "package": "vendor-connectors",
  "name": "connector_builder",
  "description": "Build HTTP connectors from API documentation",
  "required_framework": null,
  "agents": [
    { "name": "api_analyst", "role": "API Documentation Analyst" },
    { "name": "connector_engineer", "role": "Senior Python Engineer" }
  ],
  "tasks": [
    { "name": "analyze_api", "description": "Analyze API documentation..." },
    { "name": "generate_connector", "description": "Generate connector code..." }
  ],
  "knowledge_paths": ["knowledge/api_patterns"]
}
```

### CrewRunResult

Returned by `agentic-crew run ... --json`:

**Success:**
```json
{
  "success": true,
  "output": "Generated connector code:\n\nclass MeshyConnector...",
  "framework_used": "crewai",
  "duration_ms": 45230
}
```

**Failure:**
```json
{
  "success": false,
  "error": "Package 'unknown' not found",
  "available_packages": ["vendor-connectors", "otterfall"],
  "duration_ms": 52
}
```

## TypeScript Types

Copy these types into your TypeScript project for type-safe integration:

```typescript
// types/agentic-crew.ts

/** Result from `agentic-crew list --json` */
export interface CrewListResult {
  crews: CrewSummary[];
}

export interface CrewSummary {
  /** Package containing the crew */
  package: string;
  /** Crew name */
  name: string;
  /** Human-readable description */
  description: string;
  /** Required framework (null = any framework works) */
  required_framework: 'crewai' | 'langgraph' | 'strands' | null;
}

/** Result from `agentic-crew info <package> <crew> --json` */
export interface CrewInfoResult {
  package: string;
  name: string;
  description: string;
  required_framework: 'crewai' | 'langgraph' | 'strands' | null;
  agents: AgentInfo[];
  tasks: TaskInfo[];
  knowledge_paths: string[];
}

export interface AgentInfo {
  name: string;
  role: string;
}

export interface TaskInfo {
  name: string;
  description: string;
}

/** Result from `agentic-crew run ... --json` */
export interface CrewRunResult {
  success: boolean;
  /** Crew output (present when success=true) */
  output?: string;
  /** Error message (present when success=false) */
  error?: string;
  /** Framework that was used */
  framework_used?: 'crewai' | 'langgraph' | 'strands';
  /** Execution duration in milliseconds */
  duration_ms: number;
  /** Available packages (present on package not found error) */
  available_packages?: string[];
}

/** Exit codes from CLI */
export enum ExitCode {
  /** Crew executed successfully */
  Success = 0,
  /** Crew execution failed (runtime error) */
  ExecutionFailed = 1,
  /** Configuration error (package/crew not found) */
  ConfigurationError = 2,
  /** Framework not available */
  FrameworkNotAvailable = 3,
}
```

## Exit Codes

| Code | Name | Description |
|------|------|-------------|
| `0` | Success | Crew executed successfully |
| `1` | ExecutionFailed | Crew execution failed (runtime error) |
| `2` | ConfigurationError | Package or crew not found |
| `3` | FrameworkNotAvailable | Required framework is not installed |

**Example handling:**
```typescript
const result = spawnSync('agentic-crew', ['run', pkg, crew, '--json']);

switch (result.status) {
  case 0:
    const output = JSON.parse(result.stdout.toString()) as CrewRunResult;
    return output.output;
  case 1:
    throw new Error('Crew execution failed');
  case 2:
    throw new Error('Package or crew not found');
  case 3:
    throw new Error('Framework not installed');
  default:
    throw new Error(`Unknown error: exit code ${result.status}`);
}
```

## Installation

### Standard Installation

```bash
# Basic installation (no framework - will auto-detect at runtime)
pip install agentic-crew

# With CrewAI (recommended for most use cases)
pip install 'agentic-crew[crewai]'

# With LangGraph
pip install 'agentic-crew[langgraph]'

# With AWS Strands
pip install 'agentic-crew[strands]'

# With all frameworks
pip install 'agentic-crew[ai]'
```

### Docker Installation

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install with uv (recommended - faster)
RUN pip install uv
RUN uv pip install --system 'agentic-crew[crewai]'

# Or with pip
# RUN pip install 'agentic-crew[crewai]'

# Set environment variables
ENV ANTHROPIC_API_KEY=""

# Verify installation
RUN agentic-crew list
```

### Docker Compose Example

```yaml
# docker-compose.yml
version: '3.8'
services:
  agentic-crew:
    build: .
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    volumes:
      - ./packages:/workspace/packages:ro
```

## TypeScript Integration Examples

### Basic Integration (Node.js)

```typescript
// crews/crew-tool.ts
import { spawn, spawnSync } from 'child_process';
import type { CrewRunResult, CrewListResult } from './types/agentic-crew';

export class CrewTool {
  /**
   * List all available crews
   */
  async listCrews(): Promise<CrewListResult> {
    return new Promise((resolve, reject) => {
      const proc = spawn('agentic-crew', ['list', '--json']);
      let stdout = '';
      let stderr = '';

      proc.stdout.on('data', (data) => { stdout += data; });
      proc.stderr.on('data', (data) => { stderr += data; });

      proc.on('close', (code) => {
        if (code === 0) {
          resolve(JSON.parse(stdout));
        } else {
          reject(new Error(`Failed to list crews: ${stderr}`));
        }
      });
    });
  }

  /**
   * Invoke a crew and return the result
   */
  async invokeCrew(params: {
    package: string;
    crew: string;
    input: string;
    framework?: 'auto' | 'crewai' | 'langgraph' | 'strands';
  }): Promise<CrewRunResult> {
    const args = [
      'run',
      params.package,
      params.crew,
      '--input', params.input,
      '--json',
    ];

    if (params.framework && params.framework !== 'auto') {
      args.push('--framework', params.framework);
    }

    return new Promise((resolve, reject) => {
      const proc = spawn('agentic-crew', args);
      let stdout = '';
      let stderr = '';

      proc.stdout.on('data', (data) => { stdout += data; });
      proc.stderr.on('data', (data) => { stderr += data; });

      proc.on('close', (code) => {
        try {
          const result = JSON.parse(stdout) as CrewRunResult;
          resolve(result);
        } catch {
          reject(new Error(`Failed to parse output: ${stdout || stderr}`));
        }
      });
    });
  }
}
```

### Vercel AI SDK Integration

The **Vercel AI SDK** provides excellent tool abstraction support, enabling seamless agent-to-crew communication. This is the recommended pattern for AI agent orchestrators.

```typescript
// tools/invoke-crew.ts
import { tool } from 'ai';
import { z } from 'zod';
import { CrewTool } from './crews/crew-tool.js';

const crewTool = new CrewTool();

/**
 * Define crew invocation as a Vercel AI tool
 */
export const invokeCrewTool = tool({
  description: 'Delegate a task to a specialized AI crew. Use this when a task ' +
    'requires specialized agents working together (e.g., code generation, ' +
    'analysis, content creation).',
  parameters: z.object({
    package: z.string().describe('Package containing the crew (e.g., "otterfall", "vendor-connectors")'),
    crew: z.string().describe('Crew name (e.g., "game_builder", "connector_builder")'),
    input: z.string().describe('Task specification for the crew - be detailed and specific'),
  }),
  execute: async ({ package: pkg, crew, input }) => {
    const result = await crewTool.invokeCrew({ package: pkg, crew, input });
    
    if (!result.success) {
      throw new Error(result.error || 'Crew execution failed');
    }
    
    return result.output;
  },
});

// Example: Using in an agent
import { generateText } from 'ai';
import { anthropic } from '@ai-sdk/anthropic';

const result = await generateText({
  model: anthropic('claude-sonnet-4-20250514'),
  tools: { invokeCrew: invokeCrewTool },
  maxSteps: 5,
  prompt: 'Design and implement a quest system for the game. ' +
    'Delegate the implementation to the appropriate crew.',
});

console.log(result.text);
```

### Agent-to-Agent Communication Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Your App (TypeScript/Node.js)                 │
│                         Vercel AI SDK                            │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │ Fleet Agent │    │Triage Agent │    │ Coordinator Agent   │  │
│  └──────┬──────┘    └──────┬──────┘    └──────────┬──────────┘  │
│         │                  │                      │              │
│         └──────────────────┴──────────────────────┘              │
│                            │                                     │
│                    ┌───────▼───────┐                             │
│                    │ invokeCrew()  │  ← Vercel AI Tool           │
│                    │    Tool       │                             │
│                    └───────┬───────┘                             │
└────────────────────────────┼────────────────────────────────────┘
                             │ subprocess: agentic-crew CLI
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                     agentic-crew (Python)                        │
│                    Framework Decomposition                       │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │   CrewAI    │    │  LangGraph  │    │      Strands        │  │
│  │   Runner    │    │   Runner    │    │      Runner         │  │
│  └──────┬──────┘    └──────┬──────┘    └──────────┬──────────┘  │
│         │                  │                      │              │
│         └──────────────────┴──────────────────────┘              │
│                            │                                     │
│                    ┌───────▼───────┐                             │
│                    │ Multi-Agent   │                             │
│                    │    Crews      │                             │
│                    └───────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
```

## Environment Variables

Set these environment variables for the Python process:

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | Yes* | Claude API access (primary LLM) |
| `OPENAI_API_KEY` | No | OpenAI API access (alternative) |
| `OPENROUTER_API_KEY` | No | OpenRouter fallback |
| `AWS_ACCESS_KEY_ID` | No | For Strands with AWS Bedrock |
| `AWS_SECRET_ACCESS_KEY` | No | For Strands with AWS Bedrock |
| `AWS_DEFAULT_REGION` | No | AWS region for Bedrock |

*At least one LLM provider API key is required.

**Example:**
```typescript
import { spawn } from 'child_process';

const proc = spawn('agentic-crew', args, {
  env: {
    ...process.env,
    ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY,
  },
});
```

## Error Handling

### Structured Error Responses

When `--json` flag is used, errors are returned as structured JSON:

```typescript
async function runCrewSafe(pkg: string, crew: string, input: string) {
  const result = await crewTool.invokeCrew({ package: pkg, crew, input });
  
  if (!result.success) {
    // Check for specific error types
    if (result.available_packages) {
      // Package not found - suggest alternatives
      console.error(`Package not found. Available: ${result.available_packages.join(', ')}`);
    } else if (result.error?.includes('framework')) {
      // Framework not installed
      console.error('Required framework not installed');
    } else {
      // General execution error
      console.error(`Crew failed: ${result.error}`);
    }
    return null;
  }
  
  return result.output;
}
```

### Timeout Handling

Crews can take significant time to execute. Configure appropriate timeouts:

```typescript
import { spawn } from 'child_process';

function invokeCrewWithTimeout(args: string[], timeoutMs = 300000) {
  return new Promise((resolve, reject) => {
    const proc = spawn('agentic-crew', args);
    
    const timeout = setTimeout(() => {
      proc.kill('SIGTERM');
      reject(new Error(`Crew execution timed out after ${timeoutMs}ms`));
    }, timeoutMs);
    
    let stdout = '';
    proc.stdout.on('data', (data) => { stdout += data; });
    
    proc.on('close', (code) => {
      clearTimeout(timeout);
      resolve({ code, stdout });
    });
  });
}
```

## Best Practices

### 1. Always Use `--json` Flag

For programmatic integration, always use the `--json` flag to get structured output:

```typescript
// Good
const args = ['run', pkg, crew, '--input', input, '--json'];

// Bad - output format may change
const args = ['run', pkg, crew, '--input', input];
```

### 2. Handle Long-Running Operations

Crews can take minutes to complete. Design your integration accordingly:

```typescript
// Stream progress to the user
const proc = spawn('agentic-crew', args);

proc.stderr.on('data', (data) => {
  // Log progress (stderr contains status messages in non-JSON mode)
  console.log(`Progress: ${data.toString()}`);
});
```

### 3. Cache Crew List

The list of available crews rarely changes. Cache it:

```typescript
let crewListCache: CrewListResult | null = null;
let cacheTime = 0;
const CACHE_TTL = 60000; // 1 minute

async function getCachedCrewList(): Promise<CrewListResult> {
  if (crewListCache && Date.now() - cacheTime < CACHE_TTL) {
    return crewListCache;
  }
  crewListCache = await crewTool.listCrews();
  cacheTime = Date.now();
  return crewListCache;
}
```

### 4. Validate Input Before Calling

Validate crew existence before expensive operations:

```typescript
async function safeInvokeCrew(pkg: string, crew: string, input: string) {
  const list = await getCachedCrewList();
  const exists = list.crews.some(c => c.package === pkg && c.name === crew);
  
  if (!exists) {
    throw new Error(`Crew ${pkg}/${crew} not found`);
  }
  
  return crewTool.invokeCrew({ package: pkg, crew, input });
}
```

## Troubleshooting

### Command Not Found

```bash
# Verify installation
which agentic-crew

# If not found, ensure Python bin is in PATH
export PATH="$PATH:$(python -m site --user-base)/bin"
```

### Framework Errors

```bash
# Check available frameworks
agentic-crew list --json 2>&1 | head -20

# Install missing framework
pip install 'agentic-crew[crewai]'
```

### API Key Issues

```bash
# Verify API key is set
echo $ANTHROPIC_API_KEY | head -c 10

# Test with a simple command
ANTHROPIC_API_KEY="your-key" agentic-crew list --json
```

## Related Resources

- [agentic-crew GitHub](https://github.com/jbcom/agentic-crew)
- [Vercel AI SDK Documentation](https://sdk.vercel.ai/docs)
- [CrewAI Documentation](https://docs.crewai.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
