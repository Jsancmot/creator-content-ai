"""Image tracker module.

Tracks processed images to avoid re-processing the same image.
"""

import json
import os
import logging
from typing import List

logger = logging.getLogger(__name__)


class ImageTracker:
    """Tracks processed images using a JSON file.

    Attributes:
        file_path: Path to the JSON tracking file.
    """

    def __init__(self, file_path: str = "processed_images.json"):
        """Initialize the image tracker.

        Args:
            file_path: Path to the JSON file for tracking processed images.
        """
        self.file_path = file_path
        self._processed: List[str] = []
        self._load()

    def _load(self) -> None:
        """Load processed image IDs from the tracking file."""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._processed = data.get('processed', [])
                logger.info(f"Loaded {len(self._processed)} processed images from {self.file_path}")
            except Exception as e:
                logger.error(f"Error loading tracking file: {e}")
                self._processed = []
        else:
            logger.info(f"Tracking file does not exist, starting fresh")

    def _save(self) -> None:
        """Save the current list of processed image IDs to file."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump({'processed': self._processed}, f, indent=2)
            logger.debug(f"Saved tracking file with {len(self._processed)} entries")
        except Exception as e:
            logger.error(f"Error saving tracking file: {e}")

    def mark_processed(self, file_id: str) -> None:
        """Mark an image as processed.

        Args:
            file_id: The Google Drive file ID to mark as processed.
        """
        if file_id not in self._processed:
            self._processed.append(file_id)
            self._save()
            logger.info(f"Marked image {file_id} as processed")

    def is_processed(self, file_id: str) -> bool:
        """Check if an image has been processed.

        Args:
            file_id: The Google Drive file ID to check.

        Returns:
            True if the image has been processed, False otherwise.
        """
        return file_id in self._processed

    def get_processed_count(self) -> int:
        """Get the number of processed images.

        Returns:
            Number of images in the processed list.
        """
        return len(self._processed)

    def reset(self) -> None:
        """Reset the tracking file, clearing all processed image IDs."""
        self._processed = []
        self._save()
        logger.info("Tracking file reset")