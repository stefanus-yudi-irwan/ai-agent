"""configuration loader"""
import os
import re
from pathlib import Path
from typing import Any
import yaml
from .model import AppConfig

_ENV_PATTERN = re.compile(r"\$\{([^}]+)\}")

def _resolve_env_variables(value: Any) -> Any:
    """Recursively resolve ${ENV_VAR} references."""

    if isinstance(value, dict):
        return {
            key: _resolve_env_variables(item)
            for key, item in value.items()
        }

    if isinstance(value, list):
        return [
            _resolve_env_variables(item)
            for item in value
        ]

    if isinstance(value, str):
        def replace(match: re.Match[str]) -> str:
            env_name = match.group(1)
            env_value = os.getenv(env_name)

            if env_value is None:
                raise RuntimeError(
                    f"Environment variable '{env_name}' is not set"
                )

            return env_value

        return _ENV_PATTERN.sub(replace, value)

    return value

def load_config(path: str | Path) -> AppConfig:
    """Load YAML configuration and resolve environment variables."""
    path = Path(path)
    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)
    resolved_config = _resolve_env_variables(config)
    return AppConfig.model_validate(resolved_config)