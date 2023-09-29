import logging
import os
import sys

import darkdetect
import qdarktheme
from PyQt6.QtWidgets import QApplication
from appdata import AppDataPaths
from PyQt6.QtGui import QIcon

from src.BetterConfigParser import BetterConfigParser
from src.Controller import Controller
from src.MainWindowQt import MainWindowQt

applicationName = "TimeTracker"
version = '1.1.4'


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

    if darkdetect.isDark():
        qdarktheme.setup_theme("dark")
    else:
        qdarktheme.setup_theme("light")
    
    base_path = os.path.dirname(__file__)
    app.setWindowIcon(QIcon(os.path.join(base_path, 'src','clock.png')))
    window = MainWindowQt(controller, version)
    app.exec()


if __name__ == "__main__":
    main()
