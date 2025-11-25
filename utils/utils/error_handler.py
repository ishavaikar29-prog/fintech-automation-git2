import logging
from datetime import datetime
import os

LOG_FILE = "error.log"

# basic logging config
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger(__name__)

def log_error(context, exc):
    """Log error message (and print short message)."""
    msg = f"{context}: {exc}"
    logger.error(msg)

def log_info(msg):
    logger.info(msg)

def attachable_log_exists():
    return os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0
