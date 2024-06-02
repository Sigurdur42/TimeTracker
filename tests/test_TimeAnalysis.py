import unittest

from timetracking.TimeAnalysis import TimeAnalysis
from timetracking.serializers import TimeRecordSerializer


class TimeAnalysisTests(unittest.TestCase):

    def test_verify_summarized_day(self):
        data_csv = [
                    # 1.1. is public Holiday -> 7.5h overtime
                    '01.01.2023;08:00;12:00',
                    '01.01.2023;12:30;16:00',

                    # normal workday -> -4.5h overtime
                    '02.01.2023;12:30;16:00',

                    # normal workday -> -4h overtime
                    '03.01.2023;12:00;16:00',

                    # normal workday -> -4h overtime
                    '03.02.2023;12:00;16:00',

                    # normal workday -> 1h overtime
                    '03.03.2023;07:00;12:00',
                    '03.03.2023;13:00;17:00',

                    # normal weekday, but marked as all overtime
                    '06.04.2024;13:00;17:00;True',]
        serializer = TimeRecordSerializer()
        data = serializer.read_csv_from_lines(data_csv)

        target = TimeAnalysis(data)
        self.__verify_data(target.data_by_day, "%d.%m.%Y", '01.01.2023', 7.5 * 60 * 60, 7.5 * 60 * 60)
        self.__verify_data(target.data_by_day, "%d.%m.%Y", '02.01.2023', 3.5 * 60 * 60, -(4.5 * 60 * 60))
        self.__verify_data(target.data_by_day, "%d.%m.%Y", '03.03.2023', 9 * 60 * 60, 1 * 60 * 60)
        self.__verify_data(target.data_by_day, "%d.%m.%Y", '06.04.2024', 4 * 60 * 60, 4 * 60 * 60)

        self.__verify_data(target.data_by_month, "%m.%Y", '01.2023', 15 * 60 * 60, -1 * 60 * 60)
        self.__verify_data(target.data_by_month, "%m.%Y", '02.2023', 4 * 60 * 60, -4 * 60 * 60)
        self.__verify_data(target.data_by_month, "%m.%Y", '03.2023', 9 * 60 * 60, 1 * 60 * 60)

        self.__verify_data(target.data_by_year, "%Y", '2023', 28 * 60 * 60, -4 * 60 * 60)
        self.__verify_data(target.data_by_year, "%Y", '2024', 4 * 60 * 60, 4 * 60 * 60)

    def test_summarize_by_topic(self):
        data_csv = [
                    # 1.1. is public Holiday -> 7.5h overtime
                    '01.01.2023;08:00;12:00;;misc;',
                    '01.01.2023;12:00;12:30;;Pause;',
                    '01.01.2023;12:30;16:00;;misc;',
                    ]
        serializer = TimeRecordSerializer()
        data = serializer.read_csv_from_lines(data_csv)
        target = TimeAnalysis(data)
        
        days = [_ for _ in target.data_by_day_by_topic if _.scope.strftime('01.01.2023') == '01.01.2023']
        for day in days:
            if day.comment == "misc":
                self.assertEqual(7.5, day.working_hours())
        
    def __verify_data(
            self,
            days,
            day_filter: str,
            day: str,
            expected_seconds: int,
            expected_overtime_seconds: int):
        wanted_day = [_ for _ in days if _.scope.strftime(day_filter) == day][0]
        self.assertEqual(expected_seconds, wanted_day.working_seconds, f'Wrong working duration on {day}')
        self.assertEqual(expected_overtime_seconds, wanted_day.overtime_seconds, f'Wrong overtime duration on {day}')
