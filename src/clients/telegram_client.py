"""Telegram notifier module.

Provides functionality to send messages and images via Telegram Bot API.
"""

import logging
from io import BytesIO
from typing import Optional

try:
    from telegram import Bot
    from telegram.error import TelegramError
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False


logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Client for sending notifications via Telegram Bot API.

    Attributes:
        bot_token: The Telegram bot token.
        chat_id: The target chat ID for sending messages.
        enabled: Whether notifications are enabled.
    """

    def __init__(self, bot_token: str, chat_id: str, enabled: bool = True):
        """Initialize the Telegram notifier.

        Args:
            bot_token: The Telegram bot token.
            chat_id: The target chat ID.
            enabled: Whether to enable notifications (default: True).
        """
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.enabled = enabled and TELEGRAM_AVAILABLE
        self._bot: Optional[Bot] = None

    def _get_bot(self) -> Bot:
        """Get or create the Telegram bot instance.

        Returns:
            The Telegram Bot object.

        Raises:
            ImportError: If python-telegram-bot is not installed.
            ValueError: If bot token or chat ID is not provided.
        """
        if self._bot is None:
            if not TELEGRAM_AVAILABLE:
                raise ImportError("python-telegram-bot not installed")
            if not self.bot_token or not self.chat_id:
                raise ValueError("Bot token and chat ID are required")
            self._bot = Bot(token=self.bot_token)
        return self._bot

    def send_image_with_caption(
        self,
        image_content: bytes,
        caption: str,
        mime_type: str = "image/jpeg"
    ) -> bool:
        """Send an image with a caption to Telegram.

        Args:
            image_content: The image content as bytes.
            caption: The caption text to include with the image.
            mime_type: The MIME type of the image (default: image/jpeg).

        Returns:
            True if the image was sent successfully, False otherwise.
        """
        if not self.enabled:
            logger.info("Telegram notifications disabled")
            return False

        try:
            bot = self._get_bot()

            image_file = BytesIO(image_content)
            image_file.name = "image.jpg"

            bot.send_photo(
                chat_id=self.chat_id,
                photo=image_file,
                caption=caption
            )

            logger.info(f"Sent image to Telegram ({len(image_content)} bytes, caption: {len(caption)} chars)")
            return True

        except TelegramError as e:
            logger.error(f"Failed to send image to Telegram: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending to Telegram: {e}")
            return False

    def send_error_notification(self, error_message: str, context: str = "") -> bool:
        """Send an error notification to Telegram.

        Args:
            error_message: The error message to send.
            context: Additional context about the error.

        Returns:
            True if the notification was sent successfully, False otherwise.
        """
        if not self.enabled:
            logger.info("Telegram notifications disabled")
            return False

        try:
            bot = self._get_bot()

            message = f"❌ *Instagram Agent Error*\n\n{error_message}"
            if context:
                message += f"\n\nContext: {context}"

            bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode="Markdown"
            )

            logger.info("Sent error notification to Telegram")
            return True

        except TelegramError as e:
            logger.error(f"Failed to send error notification: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending error notification: {e}")
            return False