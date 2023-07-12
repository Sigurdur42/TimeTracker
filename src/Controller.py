import logging
import os
from dataclasses import dataclass
from appdata import AppDataPaths

from src import BetterConfigParser, TimeAnalysis
from src.models import TimeRecord
from src.serializers import TimeRecordSerializer


@dataclass
class Controller:
    def __init__(
            self,
            config_parser: BetterConfigParser,
            app_data_paths: AppDataPaths):
        self.time_analysis = None
        self.__config_parser = config_parser
        self.__app_data_paths = app_data_paths        
        self.__data_reader = TimeRecordSerializer()

        self.last_data_file = self.__config_parser.get_value(
            'Recent',
            'LastDataFile',
            os.path.join(self.__app_data_paths.app_data_path, 'DataFile.csv'))
        logging.info(f'Using data file {self.last_data_file}')

    def load_data_file(self, file_name: str):
        logging.info(f'loading records from {file_name}...')
        data = self.__data_reader.read_from_csv_file(file_name)
        self.time_analysis = TimeAnalysis.TimeAnalysis(data)
        logging.info(f'Have read {len(data)} records from data file')

        self.__config_parser.set_value(
            'Recent',
            'LastDataFile',
            file_name)
        self.last_data_file = file_name

    def add_record(self, new_record: TimeRecord, file_name: str):
        self.time_analysis.add_record(new_record)
        self.__data_reader.write_csv_to_file(file_name, self.time_analysis.raw_data)