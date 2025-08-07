import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    """
    Configures the application's logging.
    Logs will go to both console and a rotating file.
    """
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file_path = os.path.join(log_dir, "dockit_backend.log")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO) # Set overall logging level

    # Clear existing handlers to prevent duplicate logs
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        "%(levelname)s:     %(name)s - %(message)s"
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File Handler (Rotating)
    # Max 1MB per file, keep 5 backup files
    file_handler = RotatingFileHandler(
        log_file_path, maxBytes=1024 * 1024, backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # Set specific loggers to avoid excessive output from libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)

    # Get a specific logger for your application
    app_logger = logging.getLogger("dockit_backend")
    app_logger.info("Logging setup complete.")