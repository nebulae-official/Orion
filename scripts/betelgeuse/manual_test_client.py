import os

from dotenv import load_dotenv

from nebula_orion.betelgeuse import NotionClient
from nebula_orion.betelgeuse.errors import AuthenticationError
from nebula_orion.log_config import get_logger

load_dotenv()  # Load environment variables from .env file if present
logger = get_logger("Betelgeuse")

try:
    client = NotionClient(auth_token=os.environ.get("NOTION_API_TOKEN"))
    logger.info("SUCCESS: Client initialized successfully!")
    logger.info(f"Client representation: {client}")
except AuthenticationError as e:
    logger.exception(f"FAILURE: Caught unexpected AuthenticationError: {e}")
except Exception as e:
    logger.exception(f"FAILURE: Caught unexpected error: {type(e).__name__}: {e}")
