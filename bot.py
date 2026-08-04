import telebot
import os
import logging
from dotenv import load_dotenv
from config import Config
from tools import text_tools, utility_tools, data_tools, math_tools

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

# Welcome message
WELCOME_TEXT = """
🎉 Welcome to **ToolsBot** - Your Swiss Army Knife on Telegram!

I have 50+ free tools to help you with daily tasks.

📌 *Available Categories:*
📝 Text Tools
📊 Utility Tools  
🔍 Data Tools
🧮 Math Tools

📚 *Commands:*
/start - Start the bot
/help - Show this help
/about - About this bot
/tools - List all tools

Send any text and I'll help you! ✨
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, WELCOME_TEXT, parse_mode='Markdown')

@bot.message_handler(commands=['about'])
def send_about(message):
    bot.reply_to(message, "🤖 *About ToolsBot*\n\n50+ Free Tools!\nVersion: 2.0.0", parse_mode='Markdown')

@bot.message_handler(commands=['tools'])
def list_tools(message):
    tools = """
📝 *Text Tools*
/char_count - Count characters
/password_gen - Generate password
/qr_code - Generate QR code
/reverse_text - Reverse text
/palindrome - Check palindrome

📊 *Utility Tools*
/unit_convert - Convert units
/age_calc - Calculate age
/color_convert - Convert colors
/binary_trans - Binary translator

🔍 *Data Tools*
/ip_info - IP information
/json_valid - Validate JSON
/whois - Whois lookup
/html_minify - Minify HTML

🧮 *Math Tools*
/calc - Calculator
/bmi - Calculate BMI
/prime - Prime checker
/fibonacci - Fibonacci sequence

Use /tool [name] for details
"""
    bot.reply_to(message, tools, parse_mode='Markdown')

@bot.message_handler(commands=['char_count'])
def handle_char_count(message):
    bot.reply_to(message, "📝 Send me text to count characters!")
    Config.set_user_state(message.from_user.id, 'char_count')

@bot.message_handler(commands=['password_gen'])
def handle_password_gen(message):
    bot.reply_to(message, text_tools.password_generator(), parse_mode='Markdown')

@bot.message_handler(commands=['qr_code'])
def handle_qr_code(message):
    bot.reply_to(message, "📱 Send text/URL to generate QR code!")
    Config.set_user_state(message.from_user.id, 'qr_code')

@bot.message_handler(commands=['calc'])
def handle_calc(message):
    bot.reply_to(message, "🧮 Send math expression!")
    Config.set_user_state(message.from_user.id, 'calc')

@bot.message_handler(commands=['bmi'])
def handle_bmi(message):
    bot.reply_to(message, "📊 Send: weight height (kg cm)")
    Config.set_user_state(message.from_user.id, 'bmi')

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    text = message.text
    state = Config.get_user_state(user_id)
    
    if state:
        result = process_tool(user_id, state, text)
        bot.reply_to(message, result, parse_mode='Markdown')
        Config.clear_user_state(user_id)
    else:
        # Default: count characters
        result = text_tools.character_counter(text)
        bot.reply_to(message, result, parse_mode='Markdown')

def process_tool(user_id, tool_name, text):
    handlers = {
        'char_count': text_tools.character_counter,
        'qr_code': utility_tools.qr_code,
        'calc': math_tools.calculator,
        'bmi': math_tools.bmi_calculator,
    }
    
    if tool_name in handlers:
        return handlers[tool_name](text)
    return "❌ Tool not found!"

if __name__ == '__main__':
    logger.info("🤖 ToolsBot is running...")
    bot.infinity_polling()
