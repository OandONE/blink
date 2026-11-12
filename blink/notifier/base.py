"""Abstract notification backend"""

from abc import ABC, abstractmethod


class Notifier(ABC):
    """Platform-specific notification backend"""

    @abstractmethod
    def notify(self, title: str, message: str) -> None:
        """Show a notification to the user"""

    def close(self) -> None:
        """Release any resources. Optional to override"""
