import json
import os
import logging
from typing import List, Optional

logger = logging.getLogger(__name__)


class ImageTracker:
    def __init__(self, file_path: str = "processed_images.json"):
        self.file_path = file_path
        self._processed: List[str] = []
        self._load()

    def _load(self):
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

    def _save(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump({'processed': self._processed}, f, indent=2)
            logger.debug(f"Saved tracking file with {len(self._processed)} entries")
        except Exception as e:
            logger.error(f"Error saving tracking file: {e}")

    def mark_processed(self, file_id: str) -> None:
        if file_id not in self._processed:
            self._processed.append(file_id)
            self._save()
            logger.info(f"Marked image {file_id} as processed")

    def is_processed(self, file_id: str) -> bool:
        return file_id in self._processed

    def get_processed_count(self) -> int:
        return len(self._processed)

    def reset(self):
        self._processed = []
        self._save()
        logger.info("Tracking file reset")