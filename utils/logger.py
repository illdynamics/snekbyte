import logging
import sys

def setup_logging():
    """
    Configures the basic logging for the application.
    Logs INFO level and above to standard output.
    """
    # Using basicConfig is a simple way to set up logging to a stream.
    # It configures the root logger.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )
    logging.info("Logging configured.")