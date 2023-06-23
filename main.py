import logging
import os
from appdata import AppDataPaths
import configparser
from  src.serializers import TimeRecordSerializer
from src.TimeAnalysis import TimeAnalysis

applicationName = "TimeTracker"

def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname).4s: %(message)s',
        level = "INFO")

    # TODO: Add welcome message    
    
    # Init basic folders
    app_paths = AppDataPaths(applicationName)
    app_paths.setup()
    logging.info(f"Created app folders in {app_paths.app_data_path}...")
    
    # read ini
    config = configparser.ConfigParser(allow_no_value=True)
    config.read(app_paths.config_path)
    
    # todo: Create better wrapper for this
    if (config.has_option('Recent', 'LastDataFile')):
        lastDataFile = config['Recent']['LastDataFile']
    else:
        lastDataFile = os.path.join(app_paths.app_data_path, 'DataFile.csv')
        if (not config.has_section('Recent')):
            config.add_section('Recent')
            
        config.set('Recent', 'LastDataFile', lastDataFile)
        with open(app_paths.config_path, 'w') as file:
            config.write(file)
            
    logging.info(f'Using data file {lastDataFile}')
    
    dataReader = TimeRecordSerializer()
    data = dataReader.read_from_csv_file(lastDataFile)
    
    logging.info(f'Have read {len(data)} records from data file')
    
    # todo: Analyse it
    analysis = TimeAnalysis(data)
    analysis.dumpAnalysis()
    
    
if __name__ == "__main__":
    main()