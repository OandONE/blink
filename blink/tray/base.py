"""Abstract system tray backend."""

from abc import ABC, abstractmethod
from typing import Callable


class Tray(ABC):
    """Platform-specific system tray backend."""

    @abstractmethod
    def set_on_toggle(self, callback: Callable[[], None]) -> None: ...

    @abstractmethod
    def set_on_settings(self, callback: Callable[[], None]) -> None: ...

    @abstractmethod
    def set_on_quit(self, callback: Callable[[], None]) -> None: ...

    @abstractmethod
    def set_toggle_label(self, label: str) -> None: ...

    @abstractmethod
    def show(self) -> None: ...
