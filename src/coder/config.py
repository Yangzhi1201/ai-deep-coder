"""Configuration loading for AI Deep Coder."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

DEFAULT_MODEL = "anthropic:claude-sonnet-4-20250514"

PROVIDER_KEY_MAP = {
    "anthropic": "ANTHROPIC_API_KEY",
    "openai": "OPENAI_API_KEY",
}


@dataclass
class AppConfig:
    """Application configuration resolved from environment."""

    model: str = DEFAULT_MODEL
    workspace: Path = field(default_factory=Path.cwd)


def _extract_provider(model: str) -> str:
    """Extract the provider name from a 'provider:model' string."""
    if ":" in model:
        return model.split(":")[0]
    return "anthropic"


def validate_api_keys(model: str) -> None:
    """Check that the required API key exists for the given model spec."""
    provider = _extract_provider(model)
    env_var = PROVIDER_KEY_MAP.get(provider)

    if env_var and not os.environ.get(env_var):
        print(
            f"Error: {env_var} is not set.\n"
            f"The selected model '{model}' requires a {provider.title()} API key.\n"
            f"Set it in your .env file or as an environment variable."
        )
        sys.exit(1)


def load_config() -> AppConfig:
    """Load configuration from environment variables and .env file."""
    load_dotenv()

    model = os.environ.get("AI_DEEP_CODER_MODEL", DEFAULT_MODEL)
    workspace_str = os.environ.get("AI_DEEP_CODER_WORKSPACE")
    workspace = Path(workspace_str) if workspace_str else Path.cwd()

    validate_api_keys(model)

    return AppConfig(model=model, workspace=workspace)
