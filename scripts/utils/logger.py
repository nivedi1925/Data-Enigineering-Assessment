# scripts/utils/logger.py

import logging
import os
from config.config import LOG_LEVEL



def setup_logger(name=__name__, log_file='etl.log', to_console=False):
    logger = logging.getLogger(name)
    level = getattr(logging, LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)

    if not logger.handlers:
        # File handler (always enabled)
        fh = logging.FileHandler(log_file)
        fh.setLevel(level)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        # Console handler (optional)
        if to_console:
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

    return logger

