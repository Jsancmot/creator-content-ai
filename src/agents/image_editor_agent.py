"""Image editor agent module.

Provides an AI agent for editing images using LiteLLM and Agno.
"""

import os
import logging
import time

try:
    from agno import Agent, Image
    AGNO_AVAILABLE = True
except ImportError:
    AGNO_AVAILABLE = False


logger = logging.getLogger(__name__)


class ImageEditorAgent:
    """AI agent for editing images using Agno and LiteLLM.

    Attributes:
        model: The model identifier to use for image editing.
        prompt_file: Path to the prompt file for image editing.
        max_retries: Maximum number of retry attempts on failure.
        retry_delay: Delay in seconds between retry attempts.
    """

    def __init__(
        self,
        model: str = "qwen/qwen2-vl-7b-instruct",
        prompt_file: str = "config/prompts/image_editor.md",
        max_retries: int = 3,
        retry_delay: int = 5
    ):
        """Initialize the image editor agent.

        Args:
            model: The model identifier for image editing.
            prompt_file: Path to the prompt file.
            max_retries: Maximum retry attempts on failure.
            retry_delay: Seconds to wait between retries.
        """
        self.model = model
        self.prompt_file = prompt_file
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._agent = None
        self._prompt = None
        self._load_prompt()

    def _load_prompt(self) -> None:
        """Load the image editing prompt from file."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, 'r', encoding='utf-8') as f:
                self._prompt = f.read()
            logger.info(f"Loaded image editor prompt from {self.prompt_file}")
        else:
            logger.warning(f"Prompt file not found: {self.prompt_file}")
            self._prompt = "Edit this image to make it look professional and ready for Instagram."

    def _get_agent(self) -> Agent:
        """Get or create the Agno agent instance.

        Returns:
            The Agno Agent object.

        Raises:
            ImportError: If agno is not installed.
        """
        if self._agent is None:
            if not AGNO_AVAILABLE:
                raise ImportError("Agno library not installed. Install with: pip install agno")

            self._agent = Agent(
                model=self.model,
                markdown=False,
                debug_mode=False
            )
        return self._agent

    def edit_image(self, image_content: bytes) -> bytes:
        """Edit an image using the AI agent.

        Args:
            image_content: The image content as bytes.

        Returns:
            The edited image content as bytes.

        Raises:
            ImportError: If agno is not installed.
            Exception: If all retry attempts fail.
        """
        if not AGNO_AVAILABLE:
            raise ImportError("Agno library not installed. Install with: pip install agno")

        agent = self._get_agent()

        image = Image(content=image_content)

        last_error = None
        for attempt in range(self.max_retries):
            try:
                agent.run(
                    prompt=self._prompt,
                    images=[image]
                )

                logger.info("Image edited successfully")
                return image_content

            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)

        logger.error(f"Failed to edit image after {self.max_retries} attempts: {last_error}")
        raise last_error


def load_prompt(prompt_file: str) -> str:
    """Load a prompt from a file.

    Args:
        prompt_file: Path to the prompt file.

    Returns:
        The prompt content as string, or empty string if file not found.
    """
    if os.path.exists(prompt_file):
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    logger.warning(f"Prompt file not found: {prompt_file}")
    return ""