"""Instagram workflow module.

Provides functions for orchestrating the image processing workflow.
"""

import logging
from typing import Any


logger = logging.getLogger(__name__)


class ImageProcessingError(Exception):
    """Error raised when image processing fails."""
    pass


def process_single_image(
    file: dict,
    drive_client: Any,
    image_editor: Any,
    caption_agent: Any,
    telegram_notifier: Any,
    image_tracker: Any
) -> bool:
    """Process a single image through the complete workflow.

    The workflow includes:
    1. Download image from Google Drive
    2. Edit image using AI agent
    3. Generate caption using AI agent
    4. Upload edited image to output folder
    5. Send notification to Telegram
    6. Mark image as processed

    Args:
        file: Dictionary containing file metadata (id, name, etc.).
        drive_client: The Drive client instance.
        image_editor: The image editor agent instance.
        caption_agent: The caption agent instance.
        telegram_notifier: The Telegram notifier instance.
        image_tracker: The image tracker instance.

    Returns:
        True if processed successfully, False otherwise.
    """
    file_id = file['id']
    file_name = file['name']

    logger.info(f"Processing image: {file_name}")

    try:
        image_content = drive_client.download_image(file_id)

        edited_image = image_editor.edit_image(image_content)

        caption = caption_agent.generate_caption(edited_image)

        output_file_name = f"processed_{file_name}"
        drive_client.upload_image(
            drive_client.output_folder_id,
            output_file_name,
            edited_image
        )

        telegram_notifier.send_image_with_caption(edited_image, caption)

        image_tracker.mark_processed(file_id)

        logger.info(f"Successfully processed image: {file_name}")
        return True

    except Exception as e:
        logger.error(f"Error processing image {file_name}: {e}")
        telegram_notifier.send_error_notification(
            f"Error processing {file_name}: {str(e)}"
        )
        return False


def get_pending_images(drive_client: Any, image_tracker: Any) -> list[dict]:
    """Get all images that have not been processed yet.

    Args:
        drive_client: The Drive client instance.
        image_tracker: The image tracker instance.

    Returns:
        List of image metadata dictionaries for unprocessed images.
    """
    all_images = drive_client.list_images(drive_client.input_folder_id)

    pending = []
    for image in all_images:
        if not image_tracker.is_processed(image['id']):
            pending.append(image)
        else:
            logger.debug(f"Skipping already processed: {image['name']}")

    return pending


def get_processed_count(pending_images: list[dict]) -> int:
    """Get the count of processed images.

    Args:
        pending_images: List of image metadata dictionaries.

    Returns:
        Number of images in the list.
    """
    return len(pending_images)