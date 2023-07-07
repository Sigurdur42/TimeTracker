from configparser import ConfigParser
from dataclasses import dataclass


@dataclass
class BetterConfigParser:
    def __init__(self, config_file_name: str):
        self.__parser = ConfigParser(allow_no_value=True)
        self.__config_file_name = config_file_name
        self.__parser.read(config_file_name)

    def get_value(self, section: str, key: str, default_value: str) -> str:
        if self.__parser.has_option(section, key):
            return self.__parser[section][key]
        else:
            if not self.__parser.has_section(section):
                self.__parser.add_section(section)

            self.__parser.set(section, 'LastDataFile', default_value)
            self.__write_data_file()
            return default_value

    def set_value(self, section: str, key: str, value: str):
        found = self.get_value(section, key, value)
        if found != value:
            self.__parser[section][key] = value
            self.__write_data_file()

    def __write_data_file(self):
        with open(self.__config_file_name, 'w') as file:
            self.__parser.write(file)
