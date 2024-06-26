import logging
import os
import sys

from PyQt6.QtWidgets import QApplication, QStyleFactory
from appdata import AppDataPaths
from PyQt6.QtGui import QIcon

from timetracking.BetterConfigParser import BetterConfigParser
from timetracking.Controller import Controller
from timetracking.MainWindowQt import MainWindowQt

applicationName = "TimeTracker"
version = "1.1.9"


def main():
    logging.basicConfig(format = "%(asctime)s %(levelname).4s: %(message)s", level = "INFO")

    print(f"Welcome to {applicationName} V{version}")

    # Init basic folders
    app_paths = AppDataPaths(applicationName)
    app_paths.setup()
    logging.info(f"Created app folders in {app_paths.app_data_path}...")

    config = BetterConfigParser(app_paths.config_path)
    controller = Controller(config, app_paths)

    # sys.argv += ['-platform', 'windows:darkmode=2']
    app = QApplication(sys.argv)

    available_styles = QStyleFactory.keys()
    logging.info(f"Available styles: {available_styles}")
    app.setStyle('Fusion')
    # app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt6())

    base_path = os.path.dirname(__file__)
    app.setWindowIcon(QIcon(os.path.join(base_path, "src", "clock.png")))
    window = MainWindowQt(controller, version)
    app.exec()


if __name__ == "__main__":
    main()
