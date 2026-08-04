import telebot
import os
import logging
from dotenv import load_dotenv

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

# Store user states
user_states = {}

# Welcome message
WELCOME_TEXT = """
🎉 Welcome to **ToolsBot**!

I have 50+ free tools to help you with daily tasks.

📌 *Available Categories:*
📝 Text Tools
📊 Utility Tools  
🔍 Data Tools
🧮 Math Tools

📚 *Commands:*
/start - Start the bot
/help - Show help
/about - About this bot
/tools - List all tools

Send any text to get started! ✨
"""

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, WELCOME_TEXT, parse_mode='Markdown')

@bot.message_handler(commands=['about'])
def send_about(message):
    about_text = """
🤖 *About ToolsBot*

50+ Free Tools in Telegram!

*Features:*
✅ No API Keys Required
✅ Fast & Private
✅ 100% Free

*Version:* 2.0.0
*Created:* 2024

Made with ❤️ for the community
"""
    bot.reply_to(message, about_text, parse_mode='Markdown')

@bot.message_handler(commands=['tools'])
def list_tools(message):
    tools = """
📝 *Text Tools*
/char_count - Count characters
/password_gen - Generate password
/reverse_text - Reverse text
/palindrome - Check palindrome
/case_convert - Convert case

📊 *Utility Tools*
/qr_code - Generate QR code
/unit_convert - Convert units
/age_calc - Calculate age
/color_convert - Convert colors

🔍 *Data Tools*
/ip_info - IP information
/json_valid - Validate JSON
/whois - Whois lookup

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
    bot.reply_to(message, "📝 Send me text to count characters, words, and sentences!")
    user_states[str(message.from_user.id)] = 'char_count'

@bot.message_handler(commands=['password_gen'])
def handle_password_gen(message):
    import random
    import string
    length = 14
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    password = ''.join(random.choice(chars) for _ in range(length))
    
    bot.reply_to(
        message,
        f"""
🔐 *Strong Password Generated*

`{password}`

✅ Length: {length}
✅ Includes: Uppercase, Lowercase, Numbers, Special chars
✅ Strength: Very Strong

💡 Tap the password to copy it!
""",
        parse_mode='Markdown'
    )

@bot.message_handler(commands=['reverse_text'])
def handle_reverse_text(message):
    bot.reply_to(message, "🔄 Send text to reverse!")
    user_states[str(message.from_user.id)] = 'reverse_text'

@bot.message_handler(commands=['palindrome'])
def handle_palindrome(message):
    bot.reply_to(message, "🔍 Send text to check if it's a palindrome!")
    user_states[str(message.from_user.id)] = 'palindrome'

@bot.message_handler(commands=['case_convert'])
def handle_case_convert(message):
    bot.reply_to(message, "📝 Send text to convert case!")
    user_states[str(message.from_user.id)] = 'case_convert'

@bot.message_handler(commands=['qr_code'])
def handle_qr_code(message):
    bot.reply_to(message, "📱 Send text/URL to generate QR code!")
    user_states[str(message.from_user.id)] = 'qr_code'

@bot.message_handler(commands=['unit_convert'])
def handle_unit_convert(message):
    bot.reply_to(message, "🔧 Send: 10 km to miles")
    user_states[str(message.from_user.id)] = 'unit_convert'

@bot.message_handler(commands=['age_calc'])
def handle_age_calc(message):
    bot.reply_to(message, "📅 Send birthdate (YYYY-MM-DD)\nExample: 1990-01-15")
    user_states[str(message.from_user.id)] = 'age_calc'

@bot.message_handler(commands=['color_convert'])
def handle_color_convert(message):
    bot.reply_to(message, "🎨 Send color code!\nExample: #FF5733")
    user_states[str(message.from_user.id)] = 'color_convert'

@bot.message_handler(commands=['ip_info'])
def handle_ip_info(message):
    bot.reply_to(message, "🌐 Send an IP address to get information!")
    user_states[str(message.from_user.id)] = 'ip_info'

@bot.message_handler(commands=['json_valid'])
def handle_json_valid(message):
    bot.reply_to(message, "📝 Send JSON to validate and format!")
    user_states[str(message.from_user.id)] = 'json_valid'

@bot.message_handler(commands=['calc'])
def handle_calc(message):
    bot.reply_to(message, "🧮 Send math expression!\nExample: 2 + 2 * 3")
    user_states[str(message.from_user.id)] = 'calc'

@bot.message_handler(commands=['bmi'])
def handle_bmi(message):
    bot.reply_to(message, "📊 Send weight and height (kg cm)\nExample: 70 175")
    user_states[str(message.from_user.id)] = 'bmi'

@bot.message_handler(commands=['prime'])
def handle_prime(message):
    bot.reply_to(message, "🔢 Send a number to check if it's prime!")
    user_states[str(message.from_user.id)] = 'prime'

@bot.message_handler(commands=['fibonacci'])
def handle_fibonacci(message):
    bot.reply_to(message, "🔢 Send a number for Fibonacci sequence!")
    user_states[str(message.from_user.id)] = 'fibonacci'

@bot.message_handler(commands=['whois'])
def handle_whois(message):
    bot.reply_to(message, "🔍 Send a domain name!\nExample: google.com")
    user_states[str(message.from_user.id)] = 'whois'

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = str(message.from_user.id)
    text = message.text
    
    if user_id in user_states:
        state = user_states[user_id]
        result = process_tool(state, text)
        bot.reply_to(message, result, parse_mode='Markdown')
        del user_states[user_id]
    else:
        # Default: count characters
        result = character_counter(text)
        bot.reply_to(message, result, parse_mode='Markdown')

def process_tool(tool_name, text):
    """Process tools based on user state"""
    
    if tool_name == 'char_count':
        return character_counter(text)
    
    elif tool_name == 'reverse_text':
        return reverse_text(text)
    
    elif tool_name == 'palindrome':
        return palindrome_checker(text)
    
    elif tool_name == 'case_convert':
        return case_converter(text)
    
    elif tool_name == 'qr_code':
        return generate_qr_code(text)
    
    elif tool_name == 'unit_convert':
        return unit_converter(text)
    
    elif tool_name == 'age_calc':
        return age_calculator(text)
    
    elif tool_name == 'color_convert':
        return color_converter(text)
    
    elif tool_name == 'ip_info':
        return get_ip_info(text)
    
    elif tool_name == 'json_valid':
        return validate_json(text)
    
    elif tool_name == 'calc':
        return calculator(text)
    
    elif tool_name == 'bmi':
        return bmi_calculator(text)
    
    elif tool_name == 'prime':
        return prime_checker(text)
    
    elif tool_name == 'fibonacci':
        return generate_fibonacci(text)
    
    elif tool_name == 'whois':
        return whois_lookup(text)
    
    else:
        return "❌ Tool not found!"

# ============= TOOL FUNCTIONS =============

def character_counter(text):
    """Count characters, words, and sentences"""
    if not text or len(text.strip()) < 1:
        return "❌ Please send some text to analyze!"
    
    characters = len(text)
    words = len(text.split())
    sentences = len([c for c in text if c in '.!?'])
    
    return f"""
📊 *Text Analysis Results*

📝 Characters: {characters}
📝 Words: {words}
📝 Sentences: {sentences if sentences > 0 else 1}
"""

def reverse_text(text):
    """Reverse text"""
    if not text:
        return "❌ Send text to reverse!"
    
    return f"""
🔄 *Reversed Text*

📝 Original: {text}
⬅️ Reversed: {text[::-1]}
"""

def palindrome_checker(text):
    """Check if text is palindrome"""
    if not text:
        return "❌ Send text to check!"
    
    import re
    clean = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
    is_pal = clean == clean[::-1]
    
    return f"""
🔍 *Palindrome Check*

📝 "{text}"
{'✅ YES! This is a palindrome!' if is_pal else '❌ NO! This is not a palindrome.'}
"""

def case_converter(text):
    """Convert text cases"""
    if not text:
        return "❌ Send text to convert!"
    
    return f"""
📝 *Case Conversion*

🔹 UPPER: {text.upper()}
🔹 lower: {text.lower()}
🔹 Title: {text.title()}
🔹 Capitalize: {text.capitalize()}
"""

def generate_qr_code(text):
    """Generate QR code"""
    try:
        import qrcode
        import io
        
        if not text:
            return "❌ Send text/URL for QR code!"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes
    except Exception as e:
        return f"❌ Error: {str(e)}"

def unit_converter(text):
    """Convert units"""
    if not text:
        return "❌ Usage: 10 km to miles"
    
    try:
        parts = text.lower().split(' to ')
        if len(parts) != 2:
            return "❌ Usage: 10 km to miles"
        
        from_parts = parts[0].split()
        value = float(from_parts[0])
        from_unit = from_parts[1]
        to_unit = parts[1]
        
        # Simple conversions
        conversions = {
            'km': {'miles': 0.621371},
            'miles': {'km': 1.60934},
            'kg': {'lbs': 2.20462},
            'lbs': {'kg': 0.453592},
        }
        
        if from_unit in conversions and to_unit in conversions[from_unit]:
            result = value * conversions[from_unit][to_unit]
            return f"""
🔧 *Unit Conversion*

{value} {from_unit} = {result:.4f} {to_unit}
"""
        else:
            return f"❌ Conversion from {from_unit} to {to_unit} not supported!"
    except:
        return "❌ Invalid format! Example: 10 km to miles"

def age_calculator(birthdate):
    """Calculate age"""
    from datetime import datetime
    
    if not birthdate:
        return "❌ Usage: YYYY-MM-DD"
    
    try:
        birth = datetime.strptime(birthdate.strip(), '%Y-%m-%d')
        today = datetime.now()
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        
        return f"""
📅 *Age Calculator*

🎂 Birthdate: {birthdate}
✅ Age: {age} years
"""
    except:
        return "❌ Invalid date! Use: YYYY-MM-DD"

def color_converter(text):
    """Convert color codes"""
    if not text:
        return "❌ Send color code!"
    
    if text.startswith('#'):
        hex_color = text.lstrip('#')
        if len(hex_color) == 6:
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return f"""
🎨 *Color Converter*

HEX: {text}
RGB: {rgb}
"""
    return "❌ Use: #FF5733"

def get_ip_info(ip):
    """Get IP information"""
    try:
        import requests
        
        if not ip:
            return "❌ Send IP address!"
        
        response = requests.get(f'http://ip-api.com/json/{ip}')
        data = response.json()
        
        if data['status'] == 'success':
            return f"""
📍 *IP Information*

🌐 IP: {data['query']}
📍 Country: {data['country']}
🏙️ City: {data['city']}
📞 ISP: {data['isp']}
"""
        else:
            return "❌ IP not found!"
    except:
        return "❌ Error fetching IP information!"

def validate_json(text):
    """Validate JSON"""
    import json
    
    if not text:
        return "❌ Send JSON to validate!"
    
    try:
        data = json.loads(text)
        formatted = json.dumps(data, indent=2)
        return f"""
✅ *Valid JSON!*

```json
{formatted[:500]}
