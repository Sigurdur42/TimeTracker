import logging
import itertools
from .models import TimeRecord, SingleMonthSummary, SingleYearSummary
from .models import SingleDaySummary
from typing import List


class TimeAnalysis:
    def __init__(self, data: List[TimeRecord]):
        self.data_by_day = list[SingleDaySummary]()
        self.data_by_month = list[SingleMonthSummary]()
        self.data_by_year = list[SingleYearSummary]()
        self.raw_data = data
        self.__analyse_raw_data()

    def __analyse_raw_data(self):
        self.__analyse_raw_data_by_day()
        self.__analyse_data_by_month()

    def __analyse_raw_data_by_day(self):
        def by_day(_: TimeRecord):
            return _.start.date()

        grouped = {
            key: list(group) for key, group in itertools.groupby(self.raw_data, by_day)
        }

        self.data_by_day.clear()
        for single_day in grouped.values():
            self.data_by_day.append(self.__summarize_single_day(single_day))

    def __analyse_data_by_month(self):
        def by_month(_: SingleDaySummary):
            return _.day.strftime('%m.%Y')

        grouped = {
            key: list(group) for key, group in itertools.groupby(self.data_by_day, by_month)
        }

        self.data_by_month.clear()
        month_time_spend = 0
        for month in grouped.values():
            for record in month:
                month_time_spend += record.working_seconds

            by_month = SingleMonthSummary(month[0].day, month_time_spend)
            self.data_by_month.append(by_month)

    def __analyse_data_by_year(self):
        def by_year(_: SingleMonthSummary):
            return _.month.strftime('%Y')

        grouped = {
            key: list(group) for key, group in itertools.groupby(self.data_by_month, by_year)
        }

        self.data_by_year.clear()
        year_time_spend = 0
        for year in grouped.values():
            for record in year:
                year_time_spend += record.working_seconds

            by_year = SingleYearSummary(year[0].day, year_time_spend)
            self.data_by_year.append(by_year)

    @staticmethod
    def __summarize_single_day(data: List[TimeRecord]) -> SingleDaySummary:
        working_seconds = 0
        for part in data:
            working_seconds += (part.end - part.start).seconds

        return SingleDaySummary(day=data[0].start, working_seconds=working_seconds)

    def dump_analysis(self):
        logging.info("Hier könnte Ihre Analyse stehen")
