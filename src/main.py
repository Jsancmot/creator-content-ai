import os
import sys
import logging
import yaml

from src.clients.drive_client import DriveClient
from src.clients.telegram_client import TelegramNotifier
from src.agents.image_editor_agent import ImageEditorAgent
from src.agents.caption_agent import CaptionAgent
from src.agents.instagram_workflow import InstagramWorkflow
from src.utils.image_tracker import ImageTracker
from src.scheduler.polling_scheduler import PollingScheduler


def load_config(config_file: str = "config/settings.yaml"):
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


def setup_logging(log_level: str = "INFO"):
    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )


def main():
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    setup_logging(log_level)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Instagram Agent...")
    
    config = load_config()
    app_config = config.get('app', {})
    drive_config = config.get('drive', {})
    image_config = config.get('image_editor', {})
    caption_config = config.get('caption', {})
    telegram_config = config.get('telegram', {})
    tracking_config = config.get('tracking', {})
    
    input_folder = os.getenv('GOOGLE_DRIVE_INPUT_FOLDER_ID', drive_config.get('input_folder_id', ''))
    output_folder = os.getenv('GOOGLE_DRIVE_OUTPUT_FOLDER_ID', drive_config.get('output_folder_id', ''))
    
    if not input_folder or not output_folder:
        logger.error("GOOGLE_DRIVE_INPUT_FOLDER_ID and GOOGLE_DRIVE_OUTPUT_FOLDER_ID are required")
        sys.exit(1)
    
    service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON', '')
    credentials_path = None
    if not service_account_json:
        credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')
    
    drive_client = DriveClient(
        service_account_json=service_account_json,
        credentials_path=credentials_path
    )
    drive_client.input_folder_id = input_folder
    drive_client.output_folder_id = output_folder
    
    telegram_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
    telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID', telegram_config.get('chat_id', ''))
    telegram_enabled = telegram_config.get('enabled', True) and telegram_token and telegram_chat_id
    
    telegram_notifier = TelegramNotifier(
        bot_token=telegram_token,
        chat_id=telegram_chat_id,
        enabled=telegram_enabled
    )
    
    image_editor = ImageEditorAgent(
        model=os.getenv('IMAGE_MODEL', image_config.get('model', 'qwen/qwen2-vl-7b-instruct')),
        prompt_file=image_config.get('prompt_file', 'config/prompts/image_editor.md'),
        max_retries=image_config.get('max_retries', 3),
        retry_delay=image_config.get('retry_delay_seconds', 5)
    )
    
    caption_agent = CaptionAgent(
        model=os.getenv('CAPTION_MODEL', caption_config.get('model', 'groq/llama-3.3-70b-versatile')),
        prompt_file=caption_config.get('prompt_file', 'config/prompts/caption.md'),
        max_retries=caption_config.get('max_retries', 3),
        retry_delay=caption_config.get('retry_delay_seconds', 2),
        fallback_caption=caption_config.get('fallback_caption', '✨ Nueva foto publicada')
    )
    
    tracker = ImageTracker(tracking_config.get('file', 'processed_images.json'))
    
    workflow = InstagramWorkflow(
        image_editor_agent=image_editor,
        caption_agent=caption_agent,
        drive_client=drive_client,
        telegram_notifier=telegram_notifier,
        image_tracker=tracker
    )
    
    def poll():
        logger.info("Running poll cycle...")
        try:
            count = workflow.process_new_images()
            if count > 0:
                logger.info(f"Processed {count} new image(s)")
            else:
                logger.info("No new images to process")
        except Exception as e:
            logger.error(f"Error in poll cycle: {e}")
            telegram_notifier.send_error_notification(f"Error in poll cycle: {str(e)}")
    
    interval = int(os.getenv('POLLING_INTERVAL_MINUTES', app_config.get('polling_interval_minutes', 5)))
    
    scheduler = PollingScheduler(interval_minutes=interval, on_poll=poll)
    scheduler.start()


if __name__ == "__main__":
    main()