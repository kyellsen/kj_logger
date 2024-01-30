import logging
from pathlib import Path
from datetime import datetime

# Default configuration
DEFAULT_WORKING_DIRECTORY = Path(r"C:\kyellsen\005_Projekte\Z_DEFAUT_LOGGER")
DEFAULT_LOG_LEVEL = "Error"
DEFAULT_SAFE_LOGS_TO_FILE = False


class LogManager:
    """ Manages logging configuration. """
    LOG_LEVELS = {
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG,
    }

    def __init__(self, working_directory: str, log_level: str, save_logs_to_file: bool):
        self.working_directory = working_directory
        self.log_level = self.LOG_LEVELS.get(log_level.lower(), logging.INFO)
        self.safe_logs_to_file = save_logs_to_file
        self.log_directory = Path(working_directory) / "logs"
        self.configure_logging()

    def configure_logging(self):
        """ Configures logging handlers and format. """
        log_format = "%(asctime)s [%(levelname)s] %(name)s.%(funcName)s: %(message)s"
        date_format = "%Y-%m-%d %H:%M:%S"
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(ColorfulFormatter(log_format, date_format))
        handlers = [console_handler]

        if self.safe_logs_to_file:
            self.log_directory.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file = self.log_directory / f"log_{timestamp}.txt"
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(logging.Formatter(log_format, date_format))
            handlers.append(file_handler)

        logging.basicConfig(level=self.log_level, handlers=handlers)
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        logging.basicConfig(level=self.log_level, handlers=handlers)

    def update_config(self, working_directory=None, log_level=None, save_logs_to_file=None):
        """ Updates the logging configuration. """
        if working_directory is not None:
            self.working_directory = working_directory
            self.log_directory = Path(working_directory) / "logs"
        if log_level is not None:
            self.log_level = self.LOG_LEVELS.get(log_level.lower(), self.log_level)
        if save_logs_to_file is not None:
            self.safe_logs_to_file = save_logs_to_file
        self.configure_logging()


class ColorfulFormatter(logging.Formatter):
    """ Custom formatter to add color to logging output. """
    COLOR_CODES = {
        logging.CRITICAL: '\033[91m',  # Red
        logging.ERROR: '\033[91m',  # Red
        logging.WARNING: '\033[93m',  # Yellow
        logging.INFO: '\033[92m',  # Green
        logging.DEBUG: '\033[94m',  # Blue
    }
    RESET_CODE = '\033[0m'

    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)

    def format(self, record):
        color_code = self.COLOR_CODES.get(record.levelno, self.RESET_CODE)
        record.levelname = f"{color_code}{record.levelname}{self.RESET_CODE}"
        return super().format(record)


# Instantiate LogManager with default configuration
LOG_MANAGER = LogManager(str(DEFAULT_WORKING_DIRECTORY), DEFAULT_LOG_LEVEL, DEFAULT_SAFE_LOGS_TO_FILE)


def get_logger(name: str) -> logging.Logger:
    """ Retrieves a logger with the specified name. """
    return logging.getLogger(name)
