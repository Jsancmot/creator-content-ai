import os
import sys
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def check_env_vars():
    required = [
        'GOOGLE_DRIVE_INPUT_FOLDER_ID',
        'GOOGLE_DRIVE_OUTPUT_FOLDER_ID'
    ]
    
    optional = [
        'GOOGLE_SERVICE_ACCOUNT_JSON',
        'GOOGLE_CREDENTIALS_PATH',
        'LITELLM_API_KEY',
        'TELEGRAM_BOT_TOKEN',
        'TELEGRAM_CHAT_ID'
    ]
    
    logger.info("Checking environment variables...")
    
    missing_required = []
    for var in required:
        value = os.getenv(var)
        if value:
            logger.info(f"  ✓ {var} is set")
        else:
            logger.warning(f"  ✗ {var} is NOT set")
            missing_required.append(var)
    
    for var in optional:
        value = os.getenv(var)
        if value:
            logger.info(f"  ✓ {var} is set")
        else:
            logger.info(f"  ○ {var} is not set (optional)")
    
    if missing_required:
        logger.error(f"\nMissing required variables: {', '.join(missing_required)}")
        return False
    
    return True


def test_drive_client():
    logger.info("\nTesting Google Drive client...")
    
    try:
        from src.clients.drive_client import DriveClient
        
        service_account_json = os.getenv('GOOGLE_SERVICE_ACCOUNT_JSON', '')
        credentials_path = os.getenv('GOOGLE_CREDENTIALS_PATH')
        
        client = DriveClient(
            service_account_json=service_account_json,
            credentials_path=credentials_path
        )
        
        input_folder = os.getenv('GOOGLE_DRIVE_INPUT_FOLDER_ID')
        if input_folder:
            files = client.list_images(input_folder)
            logger.info(f"  ✓ Successfully listed images in Drive folder: {len(files)} files found")
        else:
            logger.warning("  Skipped: GOOGLE_DRIVE_INPUT_FOLDER_ID not set")
        
        return True
        
    except Exception as e:
        logger.error(f"  ✗ Failed: {e}")
        return False


def test_telegram_client():
    logger.info("\nTesting Telegram client...")
    
    try:
        from src.clients.telegram_client import TelegramNotifier
        
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if token and chat_id:
            notifier = TelegramNotifier(token, chat_id, enabled=True)
            logger.info("  ✓ Telegram client initialized")
        else:
            logger.warning("  Skipped: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set")
        
        return True
        
    except Exception as e:
        logger.error(f"  ✗ Failed: {e}")
        return False


def test_agents():
    logger.info("\nTesting agent imports...")
    
    try:
        from src.agents.image_editor_agent import ImageEditorAgent
        from src.agents.caption_agent import CaptionAgent
        
        logger.info("  ✓ Agent modules imported successfully")
        return True
        
    except ImportError as e:
        logger.warning(f"  ○ Some dependencies not available: {e}")
        logger.info("  This is expected if agno is not installed")
        return True
    except Exception as e:
        logger.error(f"  ✗ Failed: {e}")
        return False


def main():
    logger.info("=" * 50)
    logger.info("Instagram Agent - Credential Verification")
    logger.info("=" * 50)
    
    all_passed = True
    
    if not check_env_vars():
        all_passed = False
    
    if not test_drive_client():
        all_passed = False
    
    if not test_telegram_client():
        all_passed = False
    
    test_agents()
    
    logger.info("\n" + "=" * 50)
    if all_passed:
        logger.info("All checks passed!")
        sys.exit(0)
    else:
        logger.error("Some checks failed. Please review the output above.")
        sys.exit(1)


if __name__ == "__main__":
    main()