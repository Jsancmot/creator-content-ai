import logging
from typing import Optional

try:
    from agno import Workflow, Agent
    AGNO_AVAILABLE = True
except ImportError:
    AGNO_AVAILABLE = False

logger = logging.getLogger(__name__)


class InstagramWorkflow:
    def __init__(
        self,
        image_editor_agent,
        caption_agent,
        drive_client,
        telegram_notifier,
        image_tracker
    ):
        self.image_editor = image_editor_agent
        self.caption_agent = caption_agent
        self.drive_client = drive_client
        self.telegram = telegram_notifier
        self.tracker = image_tracker

    def process_new_images(self) -> int:
        processed_count = 0
        
        input_folder = self.drive_client.list_images(
            self.drive_client.input_folder_id
        )
        
        for file in input_folder:
            file_id = file['id']
            file_name = file['name']
            
            if self.tracker.is_processed(file_id):
                logger.info(f"Skipping already processed image: {file_name}")
                continue
            
            logger.info(f"Processing new image: {file_name}")
            
            try:
                image_content = self.drive_client.download_image(file_id)
                
                edited_image = self.image_editor.edit_image(image_content)
                
                caption = self.caption_agent.generate_caption(edited_image)
                
                output_file_name = f"processed_{file_name}"
                self.drive_client.upload_image(
                    self.drive_client.output_folder_id,
                    output_file_name,
                    edited_image
                )
                
                self.telegram.send_image_with_caption(edited_image, caption)
                
                self.tracker.mark_processed(file_id)
                
                processed_count += 1
                logger.info(f"Successfully processed image: {file_name}")
                
            except Exception as e:
                logger.error(f"Error processing image {file_name}: {e}")
                self.telegram.send_error_notification(
                    f"Error processing {file_name}: {str(e)}"
                )
        
        return processed_count