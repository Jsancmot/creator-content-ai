"""Configuration module for Instagram Agent.

Provides functions to load and access configuration from YAML files
and environment variables.
"""

import os
import logging
from typing import Optional, Any

import yaml


logger = logging.getLogger(__name__)

_config: Optional[dict] = None


def load_config(config_file: str = "config/settings.yaml") -> dict:
    """Load configuration from YAML file.

    Args:
        config_file: Path to the configuration YAML file.

    Returns:
        Dictionary containing configuration values.

    Raises:
        FileNotFoundError: If the configuration file doesn't exist.
    """
    global _config
    if _config is None:
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                _config = yaml.safe_load(f) or {}
                logger.info(f"Loaded configuration from {config_file}")
        else:
            logger.warning(f"Configuration file not found: {config_file}")
            _config = {}
    return _config


def get_config() -> dict:
    """Get the loaded configuration dictionary.

    Returns:
        Dictionary containing configuration values.
    """
    if _config is None:
        load_config()
    return _config or {}


def get_value(key: str, default: Any = None, env_var: Optional[str] = None) -> Any:
    """Get a configuration value with environment variable override.

    Args:
        key: Configuration key in dot notation (e.g., 'app.name').
        default: Default value if key is not found.
        env_var: Environment variable name to check first.

    Returns:
        The configuration value or default.
    """
    if env_var:
        env_value = os.getenv(env_var)
        if env_value:
            return env_value

    config = get_config()
    keys = key.split('.')
    value = config
    for k in keys:
        if isinstance(value, dict):
            value = value.get(k)
        else:
            return default
        if value is None:
            return default

    return value


def get_app_config() -> dict:
    """Get application configuration section.

    Returns:
        Dictionary containing app configuration.
    """
    return get_value('app', {})


def get_drive_config() -> dict:
    """Get Google Drive configuration section.

    Returns:
        Dictionary containing drive configuration.
    """
    return get_value('drive', {})


def get_image_editor_config() -> dict:
    """Get image editor agent configuration section.

    Returns:
        Dictionary containing image editor configuration.
    """
    return get_value('image_editor', {})


def get_caption_config() -> dict:
    """Get caption agent configuration section.

    Returns:
        Dictionary containing caption configuration.
    """
    return get_value('caption', {})


def get_telegram_config() -> dict:
    """Get Telegram notifier configuration section.

    Returns:
        Dictionary containing telegram configuration.
    """
    return get_value('telegram', {})


def get_tracking_config() -> dict:
    """Get image tracking configuration section.

    Returns:
        Dictionary containing tracking configuration.
    """
    return get_value('tracking', {})


def setup_logging(log_level: Optional[str] = None) -> None:
    """Configure logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
                   Defaults to 'INFO' or config value.
    """
    if log_level is None:
        log_level = get_value('app.log_level', 'INFO')
        if log_level is None:
            log_level = 'INFO'

    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
    logger.info(f"Logging configured at {log_level} level")


def reload_config(config_file: str = "config/settings.yaml") -> dict:
    """Reload configuration from file, clearing cached values.

    Args:
        config_file: Path to the configuration YAML file.

    Returns:
        Dictionary containing reloaded configuration values.
    """
    global _config
    _config = None
    return load_config(config_file)