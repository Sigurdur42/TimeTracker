from TimeTracker.domainModels import *
import unittest


class TimeTrackerTests(unittest.TestCase):
    def test_init_single_argument(self):
        target = TimeRecord(datetime(2023, 4, 23))
        self.assertEqual(0, target.duration, "duration should be 0 after init")
        self.assertEqual(0, target.end, "start should be 0 after init")
        self.assertEqual(0, target.pause, "pause should be 0 after init")

    def test_updateDuration_standard_case(self):
        target = TimeRecord(
            datetime(2023, 4, 23, 8, 0), 
            datetime(2023, 4, 23, 17, 0), 
            timedelta(minutes=30))
        self.assertEqual(0, target.duration, "duration should be 0 after init")

        target.update_duration()
        self.assertEqual(
            timedelta(hours=8, minutes=30),
            target.duration, "duration after calculation")
        
    def test_update_duration_no_break(self) :
        target = TimeRecord(
            datetime(2023, 4, 23, 8, 0), 
            datetime(2023, 4, 23, 17, 0), 
            timedelta(minutes=0))
        self.assertEqual(0, target.duration, "duration should be 0 after init")
        target.update_duration()
        self.assertEqual(
            timedelta(hours=9, minutes=00),
            target.duration, "duration after calculation")

    def test_update_duration_end_before_start(self) :
        target = TimeRecord(
            datetime(2023, 4, 23, 8, 0), 
            datetime(2022, 4, 23, 17, 0), 
            timedelta(minutes=0))
        self.assertEqual(0, target.duration, "duration should be 0 after init")
        target.update_duration()
        self.assertEqual(
            timedelta(hours=0, minutes=0),
            target.duration, "duration after calculation")


if __name__ == '__main__':
    unittest.main()
