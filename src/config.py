import os
import logging
from typing import Optional, Any
import yaml


logger = logging.getLogger(__name__)

_config: Optional[dict] = None


def load_config(config_file: str = "config/settings.yaml") -> dict:
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
    if _config is None:
        load_config()
    return _config or {}


def get_value(key: str, default: Any = None, env_var: Optional[str] = None) -> Any:
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
    return get_value('app', {})


def get_drive_config() -> dict:
    return get_value('drive', {})


def get_image_editor_config() -> dict:
    return get_value('image_editor', {})


def get_caption_config() -> dict:
    return get_value('caption', {})


def get_telegram_config() -> dict:
    return get_value('telegram', {})


def get_tracking_config() -> dict:
    return get_value('tracking', {})


def setup_logging(log_level: Optional[str] = None) -> None:
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
    global _config
    _config = None
    return load_config(config_file)