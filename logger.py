import logging
import sys

def setup_logging():
    """
    Configures the basic logging for the application.
    Logs INFO level and above to standard output.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )