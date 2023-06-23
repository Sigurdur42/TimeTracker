import unittest

from src.TimeAnalysis import TimeAnalysis
from src.models import SingleDaySummary
from src.serializers import TimeRecordSerializer


class TimeAnalysisTests(unittest.TestCase):

    def test_verify_summarized_day(self):
        data_csv = ['01.01.2023;08:00;12:00',
                    '01.01.2023;12:30;16:00',
                    '02.01.2023;12:30;16:00',
                    '03.01.2023;12:00;16:00',
                    '03.02.2023;12:00;16:00']
        serializer = TimeRecordSerializer()
        data = serializer.read_csv_from_lines(data_csv)

        target = TimeAnalysis(data)
        self.__verify_data(target.data_by_day, "%d.%m.%Y", '01.01.2023', 7.5 * 60 * 60)
        self.__verify_data(target.data_by_month, "%m.%Y", '01.2023', 15 * 60 * 60)
        self.__verify_data(target.data_by_month, "%m.%Y", '02.2023', 4 * 60 * 60)
        self.__verify_data(target.data_by_year, "%Y", '2023', 19 * 60 * 60)

    def __verify_data(
            self,
            days,
            day_filter: str,
            day: str,
            expected_seconds: int):
        wanted_day = [_ for _ in days if _.scope.strftime(day_filter) == day][0]
        self.assertEqual(expected_seconds, wanted_day.working_seconds, f'Wrong working duration on {day}')
