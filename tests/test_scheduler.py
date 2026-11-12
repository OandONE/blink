"""Tests for the pure-Python scheduler. Run with: python3 -m unittest discover tests"""

import unittest

from blink.scheduler import Event, Scheduler


class SchedulerTest(unittest.TestCase):
    def test_blink_fires_at_interval(self):
        s = Scheduler(blink_interval=3, look_away_interval=100, look_away_duration=2)
        events = [s.tick() for _ in range(3)]
        self.assertEqual(events[0], [])
        self.assertEqual(events[1], [])
        self.assertEqual(events[2], [Event.BLINK])

    def test_look_away_then_rest(self):
        s = Scheduler(blink_interval=100, look_away_interval=3, look_away_duration=2)
        results = [s.tick() for _ in range(5)]
        self.assertEqual(results[2], [Event.LOOK_AWAY])
        self.assertEqual(results[3], [])
        self.assertEqual(results[4], [Event.REST])

    def test_no_rest_on_startup(self):
        """Regression: rest must not fire right after startup"""
        s = Scheduler(blink_interval=100, look_away_interval=100, look_away_duration=2)
        for _ in range(50):
            self.assertEqual(s.tick(), [])

    def test_paused_returns_nothing(self):
        s = Scheduler(blink_interval=1, enabled=False)
        for _ in range(5):
            self.assertEqual(s.tick(), [])

    def test_resume_resets_state(self):
        s = Scheduler(blink_interval=2, look_away_interval=100)
        s.tick()
        s.pause()
        s.tick()
        s.resume()
        self.assertEqual(s.tick(), [])
        self.assertEqual(s.tick(), [Event.BLINK])


if __name__ == "__main__":
    unittest.main()
