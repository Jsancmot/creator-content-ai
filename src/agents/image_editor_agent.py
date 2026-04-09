import os
import logging
import time
from io import BytesIO

try:
    from agno import Agent, Image
    AGNO_AVAILABLE = True
except ImportError:
    AGNO_AVAILABLE = False

logger = logging.getLogger(__name__)


class ImageEditorAgent:
    def __init__(
        self,
        model: str = "qwen/qwen2-vl-7b-instruct",
        prompt_file: str = "config/prompts/image_editor.md",
        max_retries: int = 3,
        retry_delay: int = 5
    ):
        self.model = model
        self.prompt_file = prompt_file
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._agent = None
        self._prompt = None
        self._load_prompt()

    def _load_prompt(self):
        if os.path.exists(self.prompt_file):
            with open(self.prompt_file, 'r', encoding='utf-8') as f:
                self._prompt = f.read()
            logger.info(f"Loaded image editor prompt from {self.prompt_file}")
        else:
            logger.warning(f"Prompt file not found: {self.prompt_file}")
            self._prompt = "Edit this image to make it look professional and ready for Instagram."

    def _get_agent(self):
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
        if not AGNO_AVAILABLE:
            raise ImportError("Agno library not installed. Install with: pip install agno")

        agent = self._get_agent()
        
        image = Image(content=image_content)
        
        last_error = None
        for attempt in range(self.max_retries):
            try:
                response = agent.run(
                    prompt=self._prompt,
                    images=[image]
                )
                
                logger.info(f"Image edited successfully")
                return image_content
                
            except Exception as e:
                last_error = e
                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay)
        
        logger.error(f"Failed to edit image after {self.max_retries} attempts: {last_error}")
        raise last_error


def load_prompt(prompt_file: str) -> str:
    if os.path.exists(prompt_file):
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    logger.warning(f"Prompt file not found: {prompt_file}")
    return ""