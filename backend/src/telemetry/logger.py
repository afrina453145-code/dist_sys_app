import logging
import os
from logging.handlers import RotatingFileHandler

# Define the log file path relative to the backend root
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "app.log")

def setup_logger():
    # Create logger
    logger = logging.getLogger("campus_ride")
    logger.setLevel(logging.DEBUG)

    # Prevent adding multiple handlers if setup_logger is called more than once
    if not logger.handlers:
        # Create formatter with OSI mapping context
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)s | %(message)s'
        )

        # File Handler (Rotating to avoid massive files)
        file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10*1024*1024, backupCount=5)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        # Console Handler for real-time debugging
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.DEBUG)

        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Initialize the global logger instance
logger = setup_logger()

def log_osi_trace(layer: int, concept: str, details: str):
    """
    Specially formatted log for educational purposes in Distributed Systems course.
    """
    layers = {
        7: "L7_APPLICATION",
        6: "L6_PRESENTATION",
        5: "L5_SESSION",
        4: "L4_TRANSPORT",
        3: "L3_NETWORK",
        2: "L2_DATALINK",
        1: "L1_PHYSICAL",
        0: "DATABASE_LAYER"
    }
    
    layer_name = layers.get(layer, "UNKNOWN_LAYER")
    trace_msg = f"[{layer_name}] | {concept} | {details}"
    logger.info(trace_msg)
