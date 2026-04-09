import sys
import logging

from src.config import (
    setup_logging,
    get_app_config,
    get_drive_config,
    get_image_editor_config,
    get_caption_config,
    get_telegram_config,
    get_tracking_config,
    get_value,
    load_config
)
from src.clients.drive_client import DriveClient
from src.clients.telegram_client import TelegramNotifier
from src.agents.image_editor_agent import ImageEditorAgent
from src.agents.caption_agent import CaptionAgent
from src.agents.instagram_workflow import InstagramWorkflow
from src.utils.image_tracker import ImageTracker
from src.scheduler.polling_scheduler import PollingScheduler


def main():
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Instagram Agent...")
    
    load_config()
    
    app_config = get_app_config()
    drive_config = get_drive_config()
    image_config = get_image_editor_config()
    caption_config = get_caption_config()
    telegram_config = get_telegram_config()
    tracking_config = get_tracking_config()
    
    input_folder = get_value('GOOGLE_DRIVE_INPUT_FOLDER_ID', drive_config.get('input_folder_id', ''), 'GOOGLE_DRIVE_INPUT_FOLDER_ID')
    output_folder = get_value('GOOGLE_DRIVE_OUTPUT_FOLDER_ID', drive_config.get('output_folder_id', ''), 'GOOGLE_DRIVE_OUTPUT_FOLDER_ID')
    
    if not input_folder or not output_folder:
        logger.error("GOOGLE_DRIVE_INPUT_FOLDER_ID and GOOGLE_DRIVE_OUTPUT_FOLDER_ID are required")
        sys.exit(1)
    
    service_account_json = get_value('GOOGLE_SERVICE_ACCOUNT_JSON', '', 'GOOGLE_SERVICE_ACCOUNT_JSON')
    credentials_path = None
    if not service_account_json:
        credentials_path = get_value('GOOGLE_CREDENTIALS_PATH', 'credentials.json', 'GOOGLE_CREDENTIALS_PATH')
    
    drive_client = DriveClient(
        service_account_json=service_account_json,
        credentials_path=credentials_path
    )
    drive_client.input_folder_id = input_folder
    drive_client.output_folder_id = output_folder
    
    telegram_token = get_value('TELEGRAM_BOT_TOKEN', '', 'TELEGRAM_BOT_TOKEN')
    telegram_chat_id = get_value('TELEGRAM_CHAT_ID', telegram_config.get('chat_id', ''), 'TELEGRAM_CHAT_ID')
    telegram_enabled = telegram_config.get('enabled', True) and telegram_token and telegram_chat_id
    
    telegram_notifier = TelegramNotifier(
        bot_token=telegram_token,
        chat_id=telegram_chat_id,
        enabled=telegram_enabled
    )
    
    image_editor = ImageEditorAgent(
        model=get_value('IMAGE_MODEL', image_config.get('model', 'qwen/qwen2-vl-7b-instruct'), 'IMAGE_MODEL'),
        prompt_file=image_config.get('prompt_file', 'config/prompts/image_editor.md'),
        max_retries=image_config.get('max_retries', 3),
        retry_delay=image_config.get('retry_delay_seconds', 5)
    )
    
    caption_agent = CaptionAgent(
        model=get_value('CAPTION_MODEL', caption_config.get('model', 'groq/llama-3.3-70b-versatile'), 'CAPTION_MODEL'),
        prompt_file=caption_config.get('prompt_file', 'config/prompts/caption.md'),
        max_retries=caption_config.get('max_retries', 3),
        retry_delay=caption_config.get('retry_delay_seconds', 2),
        fallback_caption=caption_config.get('fallback_caption', '✨ New photo posted')
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
    
    interval = int(get_value('POLLING_INTERVAL_MINUTES', app_config.get('polling_interval_minutes', 5), 'POLLING_INTERVAL_MINUTES'))
    
    scheduler = PollingScheduler(interval_minutes=interval, on_poll=poll)
    scheduler.start()


if __name__ == "__main__":
    main()