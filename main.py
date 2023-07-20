import logging
import sys

from PyQt5.QtWidgets import QApplication
from appdata import AppDataPaths

from src.BetterConfigParser import BetterConfigParser
from src.Controller import Controller
from src.MainWindowQt import MainWindowQt

applicationName = "TimeTracker"
version = '1.0.6'


def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname).4s: %(message)s',
        level="INFO")

    print(f'Welcome to {applicationName} V{version}')

    # Init basic folders
    app_paths = AppDataPaths(applicationName)
    app_paths.setup()
    logging.info(f"Created app folders in {app_paths.app_data_path}...")

    config = BetterConfigParser(app_paths.config_path)
    controller = Controller(config, app_paths)

    # QT variant
    app = QApplication(sys.argv)
    window = MainWindowQt(controller, version)
    app.exec_()


if __name__ == "__main__":
    main()
