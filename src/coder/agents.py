"""Agent factory: builds the orchestrator with specialized subagents."""

from __future__ import annotations

from deepagents import SubAgent, create_deep_agent
from deepagents.backends import LocalShellBackend
from langgraph.graph.state import CompiledStateGraph

from coder.config import AppConfig
from coder.prompts import (
    BUG_FIXER_PROMPT,
    CODE_EXPLAINER_PROMPT,
    CODE_GENERATOR_PROMPT,
    CODE_REVIEWER_PROMPT,
    ORCHESTRATOR_PROMPT,
)
from coder.tools import get_custom_tools


def build_subagents(model: str) -> list[SubAgent]:
    """Create the four specialized subagent specifications.

    Each subagent inherits the parent's filesystem and execute tools
    automatically. We only specify name, description, system_prompt,
    and model.
    """
    return [
        SubAgent(
            name="code-generator",
            description=(
                "Generates new code: functions, classes, modules, and full files. "
                "Use for any request to write or create new code."
            ),
            system_prompt=CODE_GENERATOR_PROMPT,
            model=model,
        ),
        SubAgent(
            name="code-reviewer",
            description=(
                "Reviews existing code for bugs, style issues, performance, "
                "and security. Use when user asks for code review or audit."
            ),
            system_prompt=CODE_REVIEWER_PROMPT,
            model=model,
        ),
        SubAgent(
            name="code-explainer",
            description=(
                "Reads and explains code in detail. Use when user asks "
                "'what does this do' or 'explain this code'."
            ),
            system_prompt=CODE_EXPLAINER_PROMPT,
            model=model,
        ),
        SubAgent(
            name="bug-fixer",
            description=(
                "Diagnoses and fixes bugs using a reproduce-diagnose-fix-verify cycle. "
                "Use when user reports a bug, test failure, or error."
            ),
            system_prompt=BUG_FIXER_PROMPT,
            model=model,
        ),
    ]


def create_coding_agent(config: AppConfig) -> CompiledStateGraph:
    """Create the main AI Deep Coder orchestrator agent.

    The returned agent has built-in tools (filesystem, execute, planning,
    subagent delegation) plus any custom tools from tools.py.
    """
    backend = LocalShellBackend(
        root_dir=config.workspace,
    )
    subagents = build_subagents(config.model)
    custom_tools = get_custom_tools()

    return create_deep_agent(
        model=config.model,
        system_prompt=ORCHESTRATOR_PROMPT,
        subagents=subagents,
        backend=backend,
        tools=custom_tools if custom_tools else None,
        name="ai-deep-coder",
    )
