import logging
from appdata import AppDataPaths

applicationName = "TimeTracker"

def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname).4s: %(message)s',
        level = "INFO")

    # TODO: Add welcome message    
    logging.info("Entering main() function")
    logging.warning("Entering main() function")
    
    # Init basic folders
    app_paths = AppDataPaths(applicationName)
    app_paths.setup()
    logging.info(f"Created app folders in {app_paths.app_data_path}...")
    
    
    
if __name__ == "__main__":
    main()