"""
Módulo dos logs do projeto
"""

import logging
import sys
from typing import NamedTuple


class LoggerConfig(NamedTuple):
    "Configuração de LOGS"
    log_file: str = "app.log"
    log_level: str = "DEBUG"


def setup_logger(logger_name):
    "Configurações de logger"
    config = LoggerConfig()

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = logging.FileHandler(config.log_file)
    file_handler.setLevel(config.log_level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(config.log_level)
    console_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
