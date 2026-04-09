import logging
import signal
import time
from typing import Optional

logger = logging.getLogger(__name__)


class PollingScheduler:
    def __init__(self, interval_minutes: int = 5, on_poll=None):
        self.interval_minutes = interval_minutes
        self.on_poll = on_poll
        self._running = False
        self._signal_received = False
        
        signal.signal(signal.SIGINT, self._handle_signal)
        signal.signal(signal.SIGTERM, self._handle_signal)

    def _handle_signal(self, signum, frame):
        logger.info(f"Received signal {signum}, initiating graceful shutdown...")
        self._signal_received = True

    def start(self):
        self._running = True
        logger.info(f"Polling scheduler started (interval: {self.interval_minutes} minutes)")

        while self._running and not self._signal_received:
            try:
                if self.on_poll:
                    self.on_poll()
            except Exception as e:
                logger.error(f"Error during poll: {e}")

            if self._running and not self._signal_received:
                self._sleep_interval()

        logger.info("Polling scheduler stopped")

    def _sleep_interval(self):
        interval_seconds = self.interval_minutes * 60
        logger.debug(f"Sleeping for {interval_seconds} seconds")
        
        for _ in range(interval_seconds):
            if self._signal_received or not self._running:
                break
            time.sleep(1)

    def stop(self):
        self._running = False
        logger.info("Stopping polling scheduler...")

    def update_interval(self, interval_minutes: int):
        self.interval_minutes = interval_minutes
        logger.info(f"Updated polling interval to {interval_minutes} minutes")