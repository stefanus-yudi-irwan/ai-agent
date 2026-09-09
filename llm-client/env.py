"""helper functions"""
import os

class EnvironmentVariableError(Exception):
    """raise when environment variable is invalid"""

def load_optional_env_variable(env_key: str) -> str | None:
    """function to load optional environement variable
    Args:
        env_key (str): environment variable key
    Returns:
        str | None: environment variable value
    """
    env_variable: str | None = os.getenv(env_key)
    return env_variable

def load_required_env_variable(env_key: str) -> str:
    """function to load mandatory environement variable
    Args:
        env_key (str): environment variable key
    Returns:
        str | None: environment variable value
    """
    env_value: str | None = os.getenv(env_key)
    if env_value is None or not env_value.strip():
        raise EnvironmentVariableError(
            f"missing required environment variable: {env_key}"
        )
    return env_value
