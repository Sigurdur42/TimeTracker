from TimeTracker import *
from TimeTracker.domain import *
import unittest


class TimeTrackerTests(unittest.TestCase):
    def test_init_single_argument(self):
        target = TimeRecord(datetime(2023, 4, 23))
        self.assertEquals(0, target.duration, "duration should be 0 after init")
        self.assertEquals(0, target.end, "start should be 0 after init")
        self.assertEquals(0, target.pause, "pause should be 0 after init")

    def test_updateDuration_standard_case(self):
        target = TimeRecord(datetime(2023, 4, 23, 8, 0), datetime(
            2023, 4, 23, 17, 0), timedelta(minutes=30))
        self.assertEquals(0, target.duration,"duration should be 0 after init")

        target.updateDuration()
        self.assertEquals(timedelta(hours=8, minutes=30),target.duration, "duration after calculation")


if __name__ == '__main__':
    unittest.main()
