# AI Deep Coder

AI programming assistant built on the [LangChain Deep Agents](https://github.com/langchain-ai/deepagents) framework.

## Architecture

```
User <-> CLI (rich) <-> Orchestrator Agent
                          |-- code-generator subagent
                          |-- code-reviewer subagent
                          |-- code-explainer subagent
                          +-- bug-fixer subagent

All agents share: LocalShellBackend (filesystem + shell)
Built-in tools: ls, read_file, write_file, edit_file, glob, grep, execute, write_todos, task
```

The orchestrator delegates tasks to specialized subagents:

- **code-generator** - Writes new code (functions, classes, modules, files)
- **code-reviewer** - Reviews code for bugs, style, performance, security
- **code-explainer** - Explains how code works step by step
- **bug-fixer** - Diagnoses and fixes bugs with reproduce-diagnose-fix-verify cycle

## Prerequisites

- Python 3.11+
- An API key for [Anthropic](https://console.anthropic.com/) or [OpenAI](https://platform.openai.com/)

## Installation

```bash
git clone https://github.com/Yangzhi1201/ai-deep-coder.git
cd ai-deep-coder
pip install -e .
```

## Configuration

Copy the example environment file and add your API key:

```bash
cp .env.example .env
```

Edit `.env` and set at least one API key:

```
ANTHROPIC_API_KEY=sk-ant-...
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `ANTHROPIC_API_KEY` | - | Anthropic API key (required for Claude models) |
| `OPENAI_API_KEY` | - | OpenAI API key (required for GPT models) |
| `AI_DEEP_CODER_MODEL` | `anthropic:claude-sonnet-4-20250514` | Model in `provider:model` format |
| `AI_DEEP_CODER_WORKSPACE` | Current directory | Working directory for file operations |

## Usage

```bash
# Run with the CLI entry point
ai-deep-coder

# Or run as a Python module
python -m coder
```

### CLI Commands

| Command | Description |
|---|---|
| `/help` | Show help message |
| `/model` | Show current model |
| `/workspace` | Show current workspace |
| `/clear` | Clear conversation history |
| `/quit` | Exit the application |

### Example Prompts

```
You > Write a Python function that implements binary search
You > Review the code in src/main.py
You > Explain how the authentication middleware works
You > This test is failing with KeyError, can you fix it?
```

## Extending

Add custom tools in `src/coder/tools.py`. They are merged with the built-in Deep Agents tools (filesystem, execute, planning, subagents).

To change models, set `AI_DEEP_CODER_MODEL` in your `.env`:

```
# Use OpenAI
AI_DEEP_CODER_MODEL=openai:gpt-4o

# Use Claude
AI_DEEP_CODER_MODEL=anthropic:claude-sonnet-4-20250514
```

## License

MIT
