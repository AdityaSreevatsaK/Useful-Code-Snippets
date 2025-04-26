import logging


def setup_logging():
    """
    Set up logging configuration.

    This function configures the logging module to display log messages
    with a specific format and log level.

    Logging Configuration:
    - Level: INFO
    - Format: %(asctime)s - %(levelname)s - %(message)s
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


setup_logging()
logging.info("This is an info message.")
logging.error("This is an error message.")
