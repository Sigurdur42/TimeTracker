import logging
import unittest

from timetracking.TimeAnalysis import TimeAnalysis
from timetracking.serializers import TimeRecordSerializer


class TimeAnalysisWithRealDataTests(unittest.TestCase):
    def setUp(self) -> None:
        serializer = TimeRecordSerializer()
        self.loaded_data = serializer.read_from_csv_file("./tests/TestData/DataFile.csv")
        self.target = TimeAnalysis(self.loaded_data)

    def test_verify_day_calculations(self):
        data = [
            ("26.07.2023", 7 * 60 + 50, -10),
            ("03.04.2023", 5.5 * 60, -2.5 * 60),
            ("04.04.2023", 7.5 * 60, -0.5 * 60),
            ("05.04.2023", 9 * 60 + 20, 1 * 60 + 20),
            ("06.04.2023", 8 * 60, 0),
            ("07.04.2023", 8 * 60 + 50, 50),
            ("11.04.2023", 8 * 60 + 15, 15),
            ("13.04.2023", 9 * 60 + 30, 1 * 60 + 30),
            ("14.04.2023", 5 * 60 + 50, -(2 * 60 + 10)),
            ("17.04.2023", 8 * 60 + 50, 50),
            ("18.04.2023", 6 * 60 + 50, -(1 * 60 + 10)),
            ("19.04.2023", 8 * 60 + 20, 20),
            ("20.04.2023", 7 * 60 + 40, -20),
            ("21.04.2023", 7 * 60 + 25, -35),
            ("24.04.2023", 9 * 60 + 15, 1 * 60 + 15),
            ("25.04.2023", 8 * 60 + 30, 30),
            ("26.04.2023", 8 * 60 + 15, 15),
            ("27.04.2023", 7 * 60 + 15, -45),
            ("28.04.2023", 7 * 60 + 50, -10),
            ("02.05.2023", 8 * 60 + 25, 25),
            ("03.05.2023", 8 * 60 + 40, 40),
            ("04.05.2023", 8 * 60 + 10, 10),
            ("05.05.2023", 6 * 60 + 15, -(1 * 60 + 45)),
            ("08.05.2023", 8 * 60 + 45, 45),
            ("09.05.2023", 9 * 60 + 15, 1 * 60 + 15),
            ("10.05.2023", 9 * 60 + 30, 1 * 60 + 30),
            ("11.05.2023", 8 * 60, 0),
            ("12.05.2023", 7 * 60 + 15, -(0 * 60 + 45)),
            ("15.05.2023", 8 * 60 + 55, 55),
            ("16.05.2023", 7 * 60, -60),
            ("22.05.2023", 9 * 60, 60),
            ("23.05.2023", 9 * 60, 60),
            ("24.05.2023", 8 * 60, 0),
            ("25.05.2023", 7 * 60 + 40, -20),
            ("30.05.2023", 8 * 60, 0),
            ("31.05.2023", 9 * 60 + 40, 1 * 60 + 40),
            ("01.06.2023", 9 * 60, 1 * 60),
            ("02.06.2023", 8 * 60 + 55, 55),
            ("05.06.2023", 8 * 60 + 30, 30),
            ("06.06.2023", 8 * 60 + 50, 50),
            ("07.06.2023", 7 * 60 + 30, -30),
            ("08.06.2023", 7 * 60 + 5, -55),
            ("09.06.2023", 4 * 60 + 40, -(3 * 60 + 20)),
            ("12.06.2023", 8 * 60 + 35, 35),
            ("13.06.2023", 8 * 60 + 5, 5),
            ("14.06.2023", 7 * 60 + 45, -15),
            ("15.06.2023", 9 * 60 + 5, 65),
            ("16.06.2023", 4 * 60 + 55, -(3 * 60 + 5)),
            ("19.06.2023", 8 * 60 + 50, 50),
            ("20.06.2023", 8 * 60 + 20, 20),
            ("21.06.2023", 8 * 60 + 50, 50),
            ("22.06.2023", 7 * 60 + 50, -10),
            ("23.06.2023", 7 * 60 + 50, -10),
            ("26.06.2023", 8 * 60 + 40, 40),
            ("27.06.2023", 8 * 60, 0),
            ("28.06.2023", 7 * 60 + 50, -10),
        ]

        for row in data:
            self.__verify_day(row[0], row[1], row[2])

    def __verify_day(
        self, day: str, expected_minutes: int, expected_overtime_minutes: int
    ):
        found = [
            _ for _ in self.target.data_by_day if _.scope.strftime("%d.%m.%Y") == day
        ]
        if len(found) == 0:
            self.fail(f"Cannot find day {day} in \n{self.target.data_by_day}")

        wanted_day = found[0]
        self.assertEqual(
            expected_minutes,
            wanted_day.working_seconds / 60,
            f"Wrong working duration on {day}",
        )
        self.assertEqual(
            expected_overtime_minutes,
            wanted_day.overtime_seconds / 60,
            f"Wrong overtime duration on {day}",
        )
