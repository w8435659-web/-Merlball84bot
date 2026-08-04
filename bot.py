import telebot
import os
import logging
from dotenv import load_dotenv
from config import Config
from tools import text_tools, utility_tools, data_tools, math_tools
from utils.helpers import get_main_keyboard, get_tools_keyboard

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize bot
bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))

# Welcome message
WELCOME_TEXT = """
🎉 Welcome to **ToolsBot** - Your Swiss Army Knife on Telegram!

I have 50+ free tools to help you with daily tasks. No API keys needed!

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

🔍 *Quick Examples:*
/tool character_counter
/tool password_generator
/tool qr_code

Let's get started! Send any text or use /tools to explore! ✨
"""

HELP_TEXT = """
📚 *How to Use ToolsBot*

*Commands:*
/start - Start the bot
/help - Show this help
/about - About this bot
/tools - List all tools

*Using Tools:*
1. Type /tool [tool_name]
2. Follow the instructions
3. Get your result instantly!

*Examples:*
/tool password_generator
/tool qr_code
/tool age_calculator

*Quick Tips:*
• You can also just send text and I'll auto-detect tools!
• Use /tools to see all available tools
• All tools are completely free!
"""

ABOUT_TEXT = """
🤖 *About ToolsBot*

This bot provides 50+ free online tools directly in Telegram.

*Features:*
✅ 50+ Tools
✅ No API Keys Required
✅ Fast & Private
✅ Works Without Internet (for most tools)
✅ Regular Updates

*Built With:*
- Python
- PyTelegramBotAPI
- ❤️ for the community

*Version:* 2.0.0
*Created:* 2024

📊 *Statistics:*
• Total Tools: 50+
• Categories: 4
• Users: Growing daily!

For support or suggestions, contact @yourusername
"""

TOOLS_LIST = """
📝 *Text Tools* (12 tools)
/char_count - Count characters, words, sentences
/case_convert - Change text case (UPPER/lower/Title)
/password_gen - Generate strong passwords
/palindrome - Check if text is palindrome
/reverse_text - Reverse text
/word_freq - Analyze word frequency
/lorem_ipsum - Generate placeholder text
/acronym - Generate acronym from phrase
/vowel_count - Count vowels and consonants
/random_word - Generate random words
/text_summary - Summarize text
/readability - Calculate readability score

📊 *Utility Tools* (13 tools)
/unit_convert - Convert between units
/age_calc - Calculate age from birthdate
/qr_code - Generate QR code
/color_convert - Convert color codes (HEX/RGB/HSL)
/barcode - Generate barcode
/binary_trans - Translate binary
/base64 - Encode/decode Base64
/url_encode - Encode/decode URLs
/time_zone - Convert time zones
/countdown - Set countdown timer
/stopwatch - Simple stopwatch
/random_num - Generate random number
/currency - Convert currency

🔍 *Data Tools* (12 tools)
/ip_info - Get IP address information
/json_valid - Validate and format JSON
/xml_convert - Convert XML to JSON
/csv_convert - Convert CSV to JSON
/html_minify - Minify HTML
/css_minify - Minify CSS
/sql_format - Format SQL queries
/markdown_convert - Convert Markdown to HTML
/whois - Whois domain lookup
/dns_lookup - DNS lookup
/http_check - Check HTTP status
/domain_age - Check domain age

🧮 *Math Tools* (13 tools)
/calc - Scientific calculator
/bmi - Calculate BMI
/prime - Check if number is prime
/fibonacci - Generate Fibonacci sequence
/factorial - Calculate factorial
/rand_num - Generate random number
/uuid_gen - Generate UUID
/lottery - Generate lottery numbers
/percent - Calculate percentages
/base_convert - Convert number bases
/roman - Convert Roman numerals
/sqrt - Calculate square root
/power - Calculate power

💡 Usage: /tool [tool_name]
Example: /tool qr_code
"""

# Command Handlers
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_name = message.from_user.first_name
    bot.reply_to(
        message,
        WELCOME_TEXT.format(name=user_name),
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, HELP_TEXT, parse_mode='Markdown')

@bot.message_handler(commands=['about'])
def send_about(message):
    bot.reply_to(message, ABOUT_TEXT, parse_mode='Markdown')

@bot.message_handler(commands=['tools'])
def list_tools(message):
    bot.reply_to(message, TOOLS_LIST, parse_mode='Markdown')

@bot.message_handler(commands=['char_count'])
def handle_char_count(message):
    bot.reply_to(message, "📝 Send me text to count characters, words, and sentences!")
    Config.set_user_state(message.from_user.id, 'char_count')

@bot.message_handler(commands=['password_gen'])
def handle_password_gen(message):
    bot.reply_to(message, text_tools.password_generator())

@bot.message_handler(commands=['qr_code'])
def handle_qr_code(message):
    bot.reply_to(message, "📱 Send text or URL to generate QR code!")
    Config.set_user_state(message.from_user.id, 'qr_code')

@bot.message_handler(commands=['calc'])
def handle_calc(message):
    bot.reply_to(message, "🧮 Send a math expression to calculate!\nExample: 2 + 2 * 3")
    Config.set_user_state(message.from_user.id, 'calc')

@bot.message_handler(commands=['bmi'])
def handle_bmi(message):
    bot.reply_to(message, "📊 Send weight and height!\nExample: 70 175 (kg cm)")
    Config.set_user_state(message.from_user.id, 'bmi')

@bot.message_handler(commands=['ip_info'])
def handle_ip_info(message):
    bot.reply_to(message, "🌐 Send an IP address to get information!")
    Config.set_user_state(message.from_user.id, 'ip_info')

@bot.message_handler(commands=['json_valid'])
def handle_json_valid(message):
    bot.reply_to(message, "📝 Send JSON to validate and format!")
    Config.set_user_state(message.from_user.id, 'json_valid')

@bot.message_handler(commands=['unit_convert'])
def handle_unit_convert(message):
    bot.reply_to(message, "🔧 Send conversion!\nExample: 10 km to miles")
    Config.set_user_state(message.from_user.id, 'unit_convert')

@bot.message_handler(commands=['age_calc'])
def handle_age_calc(message):
    bot.reply_to(message, "📅 Send birthdate!\nExample: 1990-01-15")
    Config.set_user_state(message.from_user.id, 'age_calc')

@bot.message_handler(commands=['prime'])
def handle_prime(message):
    bot.reply_to(message, "🔢 Send a number to check if it's prime!")
    Config.set_user_state(message.from_user.id, 'prime')

@bot.message_handler(commands=['fibonacci'])
def handle_fibonacci(message):
    bot.reply_to(message, "🔢 Send a number for Fibonacci sequence!")
    Config.set_user_state(message.from_user.id, 'fibonacci')

@bot.message_handler(commands=['reverse_text'])
def handle_reverse_text(message):
    bot.reply_to(message, "🔄 Send text to reverse!")
    Config.set_user_state(message.from_user.id, 'reverse_text')

@bot.message_handler(commands=['word_freq'])
def handle_word_freq(message):
    bot.reply_to(message, "📊 Send text to analyze word frequency!")
    Config.set_user_state(message.from_user.id, 'word_freq')

@bot.message_handler(commands=['lorem_ipsum'])
def handle_lorem_ipsum(message):
    bot.reply_to(message, text_tools.lorem_ipsum())

@bot.message_handler(commands=['acronym'])
def handle_acronym(message):
    bot.reply_to(message, "🔤 Send a phrase to generate acronym!")
    Config.set_user_state(message.from_user.id, 'acronym')

@bot.message_handler(commands=['color_convert'])
def handle_color_convert(message):
    bot.reply_to(message, "🎨 Send color code!\nExample: #FF5733 or rgb(255,87,51)")
    Config.set_user_state(message.from_user.id, 'color_convert')

@bot.message_handler(commands=['barcode'])
def handle_barcode(message):
    bot.reply_to(message, "📊 Send 12-digit number for barcode!")
    Config.set_user_state(message.from_user.id, 'barcode')

@bot.message_handler(commands=['binary_trans'])
def handle_binary_trans(message):
    bot.reply_to(message, "📊 Send text or binary to translate!")
    Config.set_user_state(message.from_user.id, 'binary_trans')

@bot.message_handler(commands=['base64'])
def handle_base64(message):
    bot.reply_to(message, "📊 Send text to encode or Base64 to decode!")
    Config.set_user_state(message.from_user.id, 'base64')

@bot.message_handler(commands=['url_encode'])
def handle_url_encode(message):
    bot.reply_to(message, "🔗 Send URL to encode or decode!")
    Config.set_user_state(message.from_user.id, 'url_encode')

@bot.message_handler(commands=['whois'])
def handle_whois(message):
    bot.reply_to(message, "🔍 Send a domain name!\nExample: google.com")
    Config.set_user_state(message.from_user.id, 'whois')

@bot.message_handler(commands=['factorial'])
def handle_factorial(message):
    bot.reply_to(message, "🔢 Send a number to calculate factorial!")
    Config.set_user_state(message.from_user.id, 'factorial')

@bot.message_handler(commands=['random_num'])
def handle_random_num(message):
    bot.reply_to(message, "🎲 Send range!\nExample: 1-100")
    Config.set_user_state(message.from_user.id, 'random_num')

@bot.message_handler(commands=['uuid_gen'])
def handle_uuid_gen(message):
    bot.reply_to(message, math_tools.uuid_generator())

@bot.message_handler(commands=['lottery'])
def handle_lottery(message):
    bot.reply_to(message, math_tools.lottery_numbers())

@bot.message_handler(commands=['html_minify'])
def handle_html_minify(message):
    bot.reply_to(message, "📝 Send HTML to minify!")
    Config.set_user_state(message.from_user.id, 'html_minify')

@bot.message_handler(commands=['css_minify'])
def handle_css_minify(message):
    bot.reply_to(message, "🎨 Send CSS to minify!")
    Config.set_user_state(message.from_user.id, 'css_minify')

@bot.message_handler(commands=['sql_format'])
def handle_sql_format(message):
    bot.reply_to(message, "🗄️ Send SQL to format!")
    Config.set_user_state(message.from_user.id, 'sql_format')

@bot.message_handler(commands=['markdown_convert'])
def handle_markdown_convert(message):
    bot.reply_to(message, "📝 Send Markdown to convert to HTML!")
    Config.set_user_state(message.from_user.id, 'markdown_convert')

@bot.message_handler(commands=['xml_convert'])
def handle_xml_convert(message):
    bot.reply_to(message, "📊 Send XML to convert to JSON!")
    Config.set_user_state(message.from_user.id, 'xml_convert')

@bot.message_handler(commands=['csv_convert'])
def handle_csv_convert(message):
    bot.reply_to(message, "📊 Send CSV to convert to JSON!")
    Config.set_user_state(message.from_user.id, 'csv_convert')

@bot.message_handler(commands=['case_convert'])
def handle_case_convert(message):
    bot.reply_to(message, "📝 Send text to convert case!")
    Config.set_user_state(message.from_user.id, 'case_convert')

@bot.message_handler(commands=['palindrome'])
def handle_palindrome(message):
    bot.reply_to(message, "🔍 Send text to check if it's a palindrome!")
    Config.set_user_state(message.from_user.id, 'palindrome')

# Handle all text messages
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = message.from_user.id
    text = message.text
    state = Config.get_user_state(user_id)
    
    # Handle button clicks
    if text == "📝 Text Tools":
        bot.reply_to(message, "📝 *Text Tools*\n\n" + 
                    "/char_count - Count characters\n"
                    "/password_gen - Generate password\n"
                    "/qr_code - Generate QR code\n"
                    "/reverse_text - Reverse text\n"
                    "/palindrome - Check palindrome\n"
                    "/case_convert - Convert case\n\n"
                    "Use /tools for all tools!", parse_mode='Markdown')
        return
    
    elif text == "📊 Utility Tools":
        bot.reply_to(message, "📊 *Utility Tools*\n\n" +
                    "/unit_convert - Convert units\n"
                    "/age_calc - Calculate age\n"
                    "/color_convert - Convert colors\n"
                    "/barcode - Generate barcode\n"
                    "/binary_trans - Binary translator\n\n"
                    "Use /tools for all tools!", parse_mode='Markdown')
        return
    
    elif text == "🔍 Data Tools":
        bot.reply_to(message, "🔍 *Data Tools*\n\n" +
                    "/ip_info - IP information\n"
                    "/json_valid - Validate JSON\n"
                    "/whois - Whois lookup\n"
                    "/html_minify - Minify HTML\n"
                    "/sql_format - Format SQL\n\n"
                    "Use /tools for all tools!", parse_mode='Markdown')
        return
    
    elif text == "🧮 Math Tools":
        bot.reply_to(message, "🧮 *Math Tools*\n\n" +
                    "/calc - Calculator\n"
                    "/bmi - Calculate BMI\n"
                    "/prime - Prime checker\n"
                    "/fibonacci - Fibonacci sequence\n"
                    "/random_num - Random number\n\n"
                    "Use /tools for all tools!", parse_mode='Markdown')
        return
    
    elif text == "❓ Help":
        send_help(message)
        return
    
    # Process state-based tools
    if state:
        result = process_tool(user_id, state, text)
        bot.reply_to(message, result, parse_mode='Markdown')
        Config.clear_user_state(user_id)
    else:
        # Auto-detect tools
        handle_auto_detection(message)

def process_tool(user_id, tool_name, text):
    """Process tool with user input"""
    
    tool_handlers = {
        'char_count': text_tools.character_counter,
        'password_gen': text_tools.password_generator,
        'qr_code': utility_tools.qr_code,
        'calc': math_tools.calculator,
        'bmi': math_tools.bmi_calculator,
        'ip_info': data_tools.ip_info,
        'json_valid': data_tools.json_validator,
        'unit_convert': utility_tools.unit_converter,
        'age_calc': utility_tools.age_calculator,
        'prime': math_tools.prime_checker,
        'fibonacci': math_tools.fibonacci,
        'reverse_text': text_tools.reverse_text,
        'word_freq': text_tools.word_frequency,
        'acronym': text_tools.acronym_generator,
        'color_convert': utility_tools.color_converter,
        'barcode': utility_tools.barcode_generator,
        'binary_trans': utility_tools.binary_translator,
        'base64': utility_tools.base64_converter,
        'url_encode': utility_tools.url_encoder,
        'whois': data_tools.whois_lookup,
        'factorial': math_tools.factorial,
        'random_num': math_tools.random_number,
        'html_minify': data_tools.html_minifier,
        'css_minify': data_tools.css_minifier,
        'sql_format': data_tools.sql_formatter,
        'markdown_convert': data_tools.markdown_converter,
        'xml_convert': data_tools.xml_converter,
        'csv_convert': data_tools.csv_converter,
        'case_convert': text_tools.case_converter,
        'palindrome': text_tools.palindrome_checker
    }
    
    if tool_name in tool_handlers:
        handler = tool_handlers[tool_name]
        try:
            return handler(text)
        except Exception as e:
            logger.error(f"Error processing {tool_name}: {str(e)}")
            return f"❌ Error processing your request. Please try again."
    else:
        return f"❌ Tool '{tool_name}' not found!"

def handle_auto_detection(message):
    """Auto-detect what tool the user wants"""
    text = message.text.lower()
    
    # Check for keyword patterns
    if any(word in text for word in ['password', 'pass', 'pwd']):
        bot.reply_to(message, text_tools.password_generator(), parse_mode='Markdown')
    
    elif any(word in text for word in ['qr', 'qrcode']):
        bot.reply_to(message, "📱 Send text/URL to generate QR code:")
        Config.set_user_state(message.from_user.id, 'qr_code')
    
    elif any(word in text for word in ['calc', 'math', 'calculate', '2+2']):
        bot.reply_to(message, "🧮 Send a math expression:")
        Config.set_user_state(message.from_user.id, 'calc')
    
    elif any(word in text for word in ['bmi', 'weight', 'height']):
        bot.reply_to(message, "📊 Send weight and height (kg cm):")
        Config.set_user_state(message.from_user.id, 'bmi')
    
    elif any(word in text for word in ['ip', 'ip address']):
        bot.reply_to(message, "🌐 Send an IP address:")
        Config.set_user_state(message.from_user.id, 'ip_info')
    
    elif any(word in text for word in ['json']):
        bot.reply_to(message, "📝 Send JSON to validate:")
        Config.set_user_state(message.from_user.id, 'json_valid')
    
    elif any(word in text for word in ['convert', 'km', 'miles', 'kg']):
        bot.reply_to(message, "🔧 Send conversion (e.g., 10 km to miles):")
        Config.set_user_state(message.from_user.id, 'unit_convert')
    
    else:
        # Default: count characters
        result = text_tools.character_counter(message.text)
        bot.reply_to(message, result, parse_mode='Markdown')

# Handle media messages
@bot.message_handler(content_types=['document', 'photo', 'audio', 'video', 'voice', 'sticker', 'gif'])
def handle_media(message):
    bot.reply_to(
        message,
        "📎 I can only process text messages. Please send text for tools!",
        parse_mode='Markdown'
    )

# Error handler
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    bot.answer_callback_query(call.id, "Processing...")

if __name__ == '__main__':
    logger.info("🤖 ToolsBot is running...")
    try:
        bot.infinity_polling()
    except Exception as e:
        logger.error(f"Bot stopped: {str(e)}")
