"""
Configuration management for TMA Framework.
"""

# Python imports
from os import getenv
from pathlib import Path
from typing import Optional, TypeVar, Callable
from msgspec import Struct
from yaml import load, SafeLoader

T = TypeVar("T", int, float)


def _convert_env_var(
    env_var_name: str,
    value: Optional[str],
    converter: Callable[[str], T],
    default: Optional[T] = None,
) -> T:
    """
    Convert environment variable value with error handling.

    Args:
        env_var_name: Name of the environment variable for error messages
        value: String value from environment variable
        converter: Function to convert string to target type (int or float)
        default: Default value if value is None

    Returns:
        Converted value

    Raises:
        ValueError: If conversion fails, with descriptive message
    """
    if value is None:
        if default is None:
            raise ValueError(f"{env_var_name} environment variable is required")
        return default

    try:
        return converter(value)
    except (ValueError, TypeError) as e:
        raise ValueError(
            f"Invalid {converter.__name__} value for {env_var_name}: '{value}'"
        ) from e


class Config(Struct, frozen=True):
    """Configuration for TMA Framework MTProto client."""

    api_id: int
    api_hash: str
    session_string: Optional[str] = None
    session_file: Optional[str] = None
    mini_app_url: Optional[str] = None
    mini_app_start_param: Optional[str] = None
    timeout: int = 30
    retry_count: int = 3
    retry_delay: float = 1.0
    log_level: str = "INFO"
    bot_token: Optional[str] = None
    language_code: str = "ru"

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        if not self.api_id or self.api_id < 1 or self.api_id > 999999999:
            raise ValueError(
                f"api_id must be between 1 and 999999999, got {self.api_id}"
            )
        if not self.api_hash or len(self.api_hash) != 32:
            raise ValueError(
                f"api_hash must be exactly 32 characters long, got {len(self.api_hash) if self.api_hash else 0}"
            )
        if self.timeout < 1 or self.timeout > 300:
            raise ValueError(
                f"timeout must be between 1 and 300 seconds, got {self.timeout}"
            )
        if self.retry_count < 0 or self.retry_count > 10:
            raise ValueError(
                f"retry_count must be between 0 and 10, got {self.retry_count}"
            )
        if self.retry_delay < 0.1 or self.retry_delay > 10.0:
            raise ValueError(
                f"retry_delay must be between 0.1 and 10.0 seconds, got {self.retry_delay}"
            )
        if self.session_string is not None and self.session_file is not None:
            raise ValueError(
                "Cannot provide both session_string and session_file. Please provide only one session source."
            )
        if self.session_string is not None and not self.session_string.strip():
            raise ValueError(
                "session_string cannot be empty or contain only whitespace. Provide a valid session string or use session_file instead."
            )
        if self.session_file is not None and not self.session_file.strip():
            raise ValueError(
                "session_file cannot be empty or contain only whitespace. Provide a valid file path or use session_string instead."
            )
        if self.session_string is None and self.session_file is None:
            raise ValueError(
                "Session required. Provide one of: session_string (for saved session) or session_file (for file session). You need to authenticate manually first to get a session."
            )
        if self.log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            raise ValueError(
                f"Invalid log level: {self.log_level}. Must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"
            )

    @classmethod
    def from_env(cls) -> "Config":
        """Create config from environment variables."""
        api_id = _convert_env_var("TMA_API_ID", getenv("TMA_API_ID"), int)
        api_hash = getenv("TMA_API_HASH")
        if not api_hash:
            raise ValueError("TMA_API_HASH environment variable is required")
        timeout = _convert_env_var(
            "TMA_TIMEOUT", getenv("TMA_TIMEOUT"), int, default=30
        )
        retry_count = _convert_env_var(
            "TMA_RETRY_COUNT", getenv("TMA_RETRY_COUNT"), int, default=3
        )
        retry_delay = _convert_env_var(
            "TMA_RETRY_DELAY", getenv("TMA_RETRY_DELAY"), float, default=1.0
        )

        return cls(
            api_id=api_id,
            api_hash=api_hash,
            session_string=getenv("TMA_SESSION_STRING"),
            session_file=getenv("TMA_SESSION_FILE"),
            mini_app_url=getenv("TMA_MINI_APP_URL"),
            mini_app_start_param=getenv("TMA_MINI_APP_START_PARAM"),
            timeout=timeout,
            retry_count=retry_count,
            retry_delay=retry_delay,
            log_level=getenv("TMA_LOG_LEVEL", "INFO"),
            bot_token=getenv("TELEGRAM_BOT_TOKEN"),
            language_code=getenv("TMA_LANGUAGE_CODE", "ru"),
        )

    @classmethod
    def from_yaml(cls, yaml_path: str) -> "Config":
        """
        Create config from YAML file.

        Sensitive fields (api_hash, session_string, session_file) can be overridden
        by environment variables if they are set:
        - TMA_API_HASH overrides api_hash
        - TMA_SESSION_STRING overrides session_string
        - TMA_SESSION_FILE overrides session_file

        Args:
            yaml_path: Path to YAML configuration file

        Returns:
            Config instance loaded from YAML with optional env var overrides
        """
        try:
            with Path(yaml_path).open("r") as file:
                config_data = load(file, Loader=SafeLoader)

            # Override sensitive fields with environment variables if present
            if getenv("TMA_API_HASH"):
                config_data["api_hash"] = getenv("TMA_API_HASH")
            if getenv("TMA_SESSION_STRING"):
                config_data["session_string"] = getenv("TMA_SESSION_STRING")
                # Remove session_file if session_string is provided via env
                config_data.pop("session_file", None)
            elif getenv("TMA_SESSION_FILE"):
                config_data["session_file"] = getenv("TMA_SESSION_FILE")
                # Remove session_string if session_file is provided via env
                config_data.pop("session_string", None)

            return cls(**config_data)
        except FileNotFoundError:
            raise ValueError(f"Configuration file not found: {yaml_path}")
        except Exception as e:
            raise ValueError(
                f"Failed to load configuration from {yaml_path}: {e}"
            ) from e
