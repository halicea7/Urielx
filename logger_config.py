import os
import logging

# Set up logging configuration
log_directory = 'logs'
os.makedirs(log_directory, exist_ok=True)

# Clear existing handlers to prevent duplicates
for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(log_directory, 'research_summary.log'), mode='a'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Log initial message to confirm logging works
logger.info("Logging system initialized")
