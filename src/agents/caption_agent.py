"""Caption agent module.

Provides an AI agent for generating Instagram captions using LiteLLM and Agno.
"""

import os
import logging
import time
from typing import Optional

try:
    from agno import Agent
    AGNO_AVAILABLE = True
except ImportError:
    AGNO_AVAILABLE = False


logger = logging.getLogger(__name__)


class CaptionAgent:
    """AI agent for generating Instagram captions using Agno and LiteLLM.

    Attributes:
        model: The model identifier to use for caption generation.
        prompt_file: Path to the prompt file for caption generation.
        max_retries: Maximum number of retry attempts on failure.
        retry_delay: Delay in seconds between retry attempts.
        fallback_caption: Caption to use when generation fails.
    """

    def __init__(
        self,
        model: str = "groq/llama-3.3-70b-versatile",
        prompt_file: str = "config/prompts/caption.md",
        max_retries: int = 3,
        retry_delay: int = 2,
        fallback_caption: str = "✨ New photo posted"
    ):
        """Initialize the caption agent.

        Args:
            model: The model identifier for caption generation.
            prompt_file: Path to the prompt file.
            max_retries: Maximum retry attempts on failure.
            retry_delay: Seconds to wait between retries.
            fallback_caption: Caption to use on failure.
        """
        self.model = model
        self.prompt_file = prompt_file
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.fallback_caption = fallback_caption
        self._agent = None
        self._prompt = None
        self._load_prompt()

    def _load_prompt(self) -> None:
        """Load the caption generation prompt from file."""
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, 'r', encoding='utf-8') as f:
                self._prompt = f.read()
            logger.info(f"Loaded caption prompt from {self.prompt_file}")
        else:
            logger.warning(f"Prompt file not found: {self.prompt_file}")
            self._prompt = "Generate a short, engaging Instagram caption for this image with relevant hashtags."

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

    def generate_caption(self, image_content: Optional[bytes] = None) -> str:
        """Generate an Instagram caption using the AI agent.

        Args:
            image_content: Optional image content for context.

        Returns:
            The generated caption string, or fallback caption on failure.

        Raises:
            ImportError: If agno is not installed.
        """
        if not AGNO_AVAILABLE:
            raise ImportError("Agno library not installed. Install with: pip install agno")

        agent = self._get_agent()

        prompt = self._prompt
        if image_content:
            prompt = f"{prompt}\n\nPlease analyze this image and generate an Instagram caption."

        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = agent.run(prompt=prompt)

                caption = response.content.strip()
                logger.info(f"Caption generated successfully ({len(caption)} chars)")
                return caption

            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)

        logger.error(f"Failed to generate caption after {self.max_retries} attempts: {last_error}")
        return self.fallback_caption


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