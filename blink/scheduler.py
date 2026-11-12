"""Pure-Python reminder scheduler for Blink

Zero GUI dependencies — can be tested in isolation and reused by future
backends (Windows, macOS, etc.)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Event(Enum):
    """Reminder events emitted by the scheduler"""

    BLINK = "blink"
    LOOK_AWAY = "look_away"
    REST = "rest"


class _Phase(Enum):
    """Internal scheduler phase."""

    ACTIVE = "active"
    LOOKING_AWAY = "looking_away"


@dataclass
class Scheduler:
    """Counts down time and emits reminders via :meth:`tick`

    Call :meth:`tick` once per second. Each call returns a (possibly empty)
    list of :class:`Event` values that should be surfaced to the user
    """

    blink_interval: int = 30
    look_away_interval: int = 1200
    look_away_duration: int = 20
    rest_duration: int = 20
    enabled: bool = True

    _blink_counter: int = field(default=0, init=False, repr=False)
    _look_counter: int = field(default=0, init=False, repr=False)
    _rest_counter: int = field(default=0, init=False, repr=False)
    _phase: _Phase = field(default=_Phase.ACTIVE, init=False, repr=False)

    def tick(self) -> list[Event]:
        """Advance the internal clock by one second and return events"""
        if not self.enabled:
            return []

        if self._phase is _Phase.LOOKING_AWAY:
            return self._tick_looking_away()
        return self._tick_active()

    def _tick_active(self) -> list[Event]:
        events: list[Event] = []
        self._blink_counter += 1
        self._look_counter += 1

        if self._blink_counter >= self.blink_interval:
            self._blink_counter = 0
            events.append(Event.BLINK)

        if self._look_counter >= self.look_away_interval:
            self._look_counter = 0
            self._rest_counter = 0
            self._phase = _Phase.LOOKING_AWAY
            events.append(Event.LOOK_AWAY)

        return events

    def _tick_looking_away(self) -> list[Event]:
        self._rest_counter += 1
        if self._rest_counter < self.look_away_duration:
            return []

        self._rest_counter = 0
        self._phase = _Phase.ACTIVE
        return [Event.REST]

    def pause(self) -> None:
        self.enabled = False

    def resume(self) -> None:
        self.enabled = True
        self.reset()

    def reset(self) -> None:
        """Reset all counters and return to ACTIVE phase"""
        self._blink_counter = 0
        self._look_counter = 0
        self._rest_counter = 0
        self._phase = _Phase.ACTIVE
