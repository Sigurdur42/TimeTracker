import logging

def main():
    logging.basicConfig(
        format='%(asctime)s %(levelname).4s: %(message)s',
        level = "INFO")
    
    logging.info("Entering main() function")
    logging.warning("Entering main() function")
            
if __name__ == "__main__":
    main()