import telebot  # This is correct - telebot is the package name after installation
import os
import logging
from dotenv import load_dotenv
from config import Config
from tools import text_tools, utility_tools, data_tools, math_tools
from utils.helpers import get_main_keyboard

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize bot
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    logger.error("BOT_TOKEN not found in environment variables!")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# ... rest of your code
