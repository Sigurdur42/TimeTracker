import logging
import itertools
from .models import TimeRecord
from .models import SingleDaySummary
from typing import List


class TimeAnalysis:
    def __init__(self, data: List[TimeRecord]):
        self.raw_data = data
        self.__analyseRawData()

    def __analyseRawData(self):
        def by_day(record: TimeRecord):
            return record.start.date()

        grouped = {
            key: list(group) for key, group in itertools.groupby(self.raw_data, by_day)
        }
        print(grouped)
        print(len(grouped))

        for single_day in grouped.values():
            single = self.__summarizeSingleDay(single_day)
            print(single)

    def __summarizeSingleDay(self, data: List[TimeRecord]) -> SingleDaySummary:
        working_seconds = 0
        for part in data:
            working_seconds += (part.end - part.start).seconds

        return SingleDaySummary(day=data[0], working_seconds=working_seconds)

    def dumpAnalysis(self):
        logging.info("Hier könnte Ihre Analyse stehen")
