"""Abstract system tray backend"""

from abc import ABC, abstractmethod
from typing import Callable


class Tray(ABC):
    """Platform-specific system tray backend

    Callbacks passed to ``set_on_*`` take no arguments; the backend is
    responsible for adapting its own signal signature
    """

    @abstractmethod
    def set_on_toggle(self, callback: Callable[[], None]) -> None: ...

    @abstractmethod
    def set_on_quit(self, callback: Callable[[], None]) -> None: ...

    @abstractmethod
    def set_toggle_label(self, label: str) -> None:
        """Update the Pause/Resume menu item text"""

    @abstractmethod
    def show(self) -> None:
        """Display the tray icon and menu"""
