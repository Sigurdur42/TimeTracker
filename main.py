import logging
import os
from appdata import AppDataPaths
import configparser
from src.serializers import TimeRecordSerializer
from src.TimeAnalysis import TimeAnalysis

applicationName = "TimeTracker"
version = '0.1'


def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname).4s: %(message)s',
        level="INFO")

    print(f'Welcome to {applicationName} V{version}')

    # Init basic folders
    app_paths = AppDataPaths(applicationName)
    app_paths.setup()
    logging.info(f"Created app folders in {app_paths.app_data_path}...")

    # read ini
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(app_paths.config_path)

    # todo: Create better wrapper for this
    if config.has_option('Recent', 'LastDataFile'):
        last_data_file = config['Recent']['LastDataFile']
    else:
        last_data_file = os.path.join(app_paths.app_data_path, 'DataFile.csv')
        if not config.has_section('Recent'):
            config.add_section('Recent')

        config.set('Recent', 'LastDataFile', last_data_file)
        with open(app_paths.config_path, 'w') as file:
            config.write(file)

    logging.info(f'Using data file {last_data_file}')

    data_reader = TimeRecordSerializer()
    data = data_reader.read_from_csv_file(last_data_file)

    logging.info(f'Have read {len(data)} records from data file')

    # todo: Analyse it
    analysis = TimeAnalysis(data)
    analysis.dump_analysis()


if __name__ == "__main__":
    main()
