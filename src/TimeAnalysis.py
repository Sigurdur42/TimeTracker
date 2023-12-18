import logging
import itertools
from datetime import timedelta

from .models import TimeRecord
from .models import ScopeSummary
from typing import List


class TimeAnalysis:
    def __init__(self, data: List[TimeRecord]):
        self.data_by_day = list[ScopeSummary]()
        self.data_by_month = list[ScopeSummary]()
        self.data_by_year = list[ScopeSummary]()
        self.data_by_day_by_topic = list[ScopeSummary]()
        self.raw_data = sorted(data, key=lambda row: row.start)
        self.analyse_raw_data()

    def analyse_raw_data(self):
        self.__analyse_raw_data_by_day()
        self.__analyse_data_by_month()
        self.__analyse_data_by_year()

    def __analyse_raw_data_by_day(self):
        def by_day(_: TimeRecord):
            return _.start.date()

        def by_comment(_: TimeRecord):
            return _.comment

        grouped = {
            key: list(group) for key, group in itertools.groupby(self.raw_data, by_day)
        }

        self.data_by_day.clear()
        self.data_by_day_by_topic.clear()
        for single_day in grouped.values():
            self.data_by_day.append(self.__summarize_single_day(single_day))

            sorted_by_comment = sorted(single_day, key=by_comment)
            days = itertools.groupby(sorted_by_comment, by_comment)

            for comment, values in days:
                list_values = list(values)
                r = self.__summarize_single_day(list_values)
                r.comment = comment
                self.data_by_day_by_topic.append(r)

    def __analyse_data_by_month(self):
        def by_month(_: ScopeSummary):
            return _.scope.strftime("%m.%Y")

        grouped = {
            key: list(group)
            for key, group in itertools.groupby(self.data_by_day, by_month)
        }

        self.data_by_month.clear()
        for month in grouped.values():
            month_time_spend = 0
            month_overtime = 0
            for record in month:
                month_time_spend += record.working_seconds
                month_overtime += record.overtime_seconds

            by_month = ScopeSummary(month[0].scope, month_time_spend, month_overtime)
            self.data_by_month.append(by_month)

    def __analyse_data_by_year(self):
        def by_year(_: ScopeSummary):
            return _.scope.strftime("%Y")

        grouped = {
            key: list(group)
            for key, group in itertools.groupby(self.data_by_month, by_year)
        }

        self.data_by_year.clear()
        for year in grouped.values():
            year_time_spend = 0
            year_overtime = 0
            for record in year:
                year_time_spend += record.working_seconds
                year_overtime += record.overtime_seconds

            by_year = ScopeSummary(year[0].scope, year_time_spend, year_overtime)
            self.data_by_year.append(by_year)

    @staticmethod
    def __summarize_single_day(data: List[TimeRecord]) -> ScopeSummary:
        working_seconds = 0
        all_overtime = next((f for f in data if f.all_overtime), False)
        for part in data:
            working_seconds += (part.end - part.start).seconds

        # todo: get actual working hours from config
        day = data[0].start

        hours_per_day = 8 * 60 * 60

        match day.weekday():
            case 7:
                overtime_seconds = working_seconds
            case 6:
                overtime_seconds = working_seconds
            case _:
                if all_overtime:
                    overtime_seconds = working_seconds
                else:
                    overtime_seconds = working_seconds - hours_per_day

        return ScopeSummary(
            scope=day,
            working_seconds=working_seconds,
            overtime_seconds=overtime_seconds,
        )

    def get_total_overtime_seconds(self) -> int:
        result = 0
        for _ in self.data_by_year:
            result += _.overtime_seconds

        return result

    def get_total_overtime_hours(self) -> float:
        return self.get_total_overtime_seconds() / 60 / 60

    def add_record(self, new_record: TimeRecord):
        self.raw_data.append(new_record)
        self.raw_data = sorted(self.raw_data, key=lambda row: row.start)
        self.analyse_raw_data()

    def dump_analysis(self):
        print("Statistics by month:")
        for scope in self.data_by_month:
            year_visible = scope.scope_as_month()
            worked = "{:.2f}".format(scope.working_seconds / 60 / 60)
            overtime = "{:.2f}".format(scope.overtime_seconds / 60 / 60)
            print(f"{year_visible}: {worked}h  {overtime}h ")

        total_overtime = "{:.2f}".format(self.get_total_overtime_seconds() / 60 / 60)
        print(f"Current overtime: {total_overtime}h")
