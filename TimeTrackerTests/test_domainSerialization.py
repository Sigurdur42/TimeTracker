import unittest
from datetime import datetime

from TimeTracker.domainModels import TimeRecord
from TimeTracker.domainSerialization import DomainSerializer

class TimeTrackerTests(unittest.TestCase):
    def test_serialization(self):
        data = [
            TimeRecord(start=datetime(2023,8,3,8,0), end=datetime(2023,8,3,8,0)),
            TimeRecord(start=datetime(2023, 8, 2, 8, 0), end=datetime(2023, 8, 2, 8, 0)),
        ]

        ser = DomainSerializer()
        ser.serialize(data)