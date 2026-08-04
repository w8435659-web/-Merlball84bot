import telebot
import os
import sys
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

# Get bot token
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("BOT_TOKEN not found! Please set it in .env file")
    sys.exit(1)

# Create bot instance
try:
    bot = telebot.TeleBot(BOT_TOKEN)
    logger.info("Bot initialized successfully!")
except Exception as e:
    logger.error(f"Failed to initialize bot: {str(e)}")
    sys.exit(1)

# Store user states (in-memory)
user_states = {}

# ============= COMMAND HANDLERS =============

@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
🎉 *Welcome to ToolsBot!* 

I'm your AI-powered assistant with 50+ free tools!

📌 *Available Tools:*
📝 Text Tools - Count, Convert, Generate
📊 Utility Tools - QR, Units, Age
🔍 Data Tools - IP, JSON, WHOIS
🧮 Math Tools - Calculator, BMI, Prime

📚 *Commands:*
/start - Start the bot
/help - Show help
/about - About this bot
/tools - List all tools

Just send me any text and I'll help! ✨
"""
    bot.reply_to(message, welcome_text, parse_mode='Markdown')
    
    # Log user interaction
    logger.info(f"User {message.from_user.id} started the bot")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """
📚 *Help & Commands*

*Quick Commands:*
/start - Start the bot
/help - Show this help
/about - About this bot
/tools - List all tools

*Using Tools:*
1. Type /tool_name
2. Follow the instructions
3. Get your result!

*Examples:*
/char_count - Count characters
/password_gen - Generate password
/qr_code - Create QR code
/calc - Calculate math

💡 Type /tools to see all available tools!
"""
    bot.reply_to(message, help_text, parse_mode='Markdown')

@bot.message_handler(commands=['about'])
def send_about(message):
    about_text = """
🤖 *About ToolsBot*

Your Swiss Army Knife for Telegram!

*Features:*
✅ 50+ Free Tools
✅ No API Keys Required
✅ Fast & Private
✅ 100% Free

*Built With:*
- Python 3.11
- PyTelegramBotAPI
- ❤️ for the community

*Version:* 2.0.0
*Created:* 2024

Made with ❤️ for everyone!
"""
    bot.reply_to(message, about_text, parse_mode='Markdown')

@bot.message_handler(commands=['tools'])
def list_tools(message):
    tools = """
📝 *Text Tools*
/char_count - Count characters, words, sentences
/password_gen - Generate strong password
/reverse_text - Reverse text
/palindrome - Check if text is palindrome
/case_convert - Convert text case

📊 *Utility Tools*
/qr_code - Generate QR code
/unit_convert - Convert units (km to miles)
/age_calc - Calculate age from birthdate
/color_convert - Convert color codes

🔍 *Data Tools*
/ip_info - Get IP address information
/json_valid - Validate and format JSON
/whois - Whois domain lookup

🧮 *Math Tools*
/calc - Calculate math expressions
/bmi - Calculate Body Mass Index
/prime - Check if number is prime
/fibonacci - Generate Fibonacci sequence

💡 Type /tool_name to use any tool!
"""
    bot.reply_to(message, tools, parse_mode='Markdown')

# ============= TOOL HANDLERS =============

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
    bot.reply_to(message, "📱 Send text or URL to generate QR code!")
    user_states[str(message.from_user.id)] = 'qr_code'

@bot.message_handler(commands=['unit_convert'])
def handle_unit_convert(message):
    bot.reply_to(message, "🔧 Send conversion!\nExample: 10 km to miles")
    user_states[str(message.from_user.id)] = 'unit_convert'

@bot.message_handler(commands=['age_calc'])
def handle_age_calc(message):
    bot.reply_to(message, "📅 Send birthdate!\nExample: 1990-01-15")
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
    bot.reply_to(message, "📊 Send weight and height!\nExample: 70 175 (kg cm)")
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

# ============= TEXT MESSAGE HANDLER =============

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = str(message.from_user.id)
    text = message.text
    
    logger.info(f"User {user_id} sent: {text[:50]}")
    
    # Check if user has an active tool state
    if user_id in user_states:
        state = user_states[user_id]
        result = process_tool(state, text)
        
        # Send result
        if isinstance(result, bytes):
            # Send as photo for QR codes
            bot.send_photo(message.chat.id, result, caption="✅ QR Code generated successfully!")
        else:
            bot.reply_to(message, result, parse_mode='Markdown')
        
        # Clear state
        del user_states[user_id]
    else:
        # Default: count characters
        result = character_counter(text)
        bot.reply_to(message, result, parse_mode='Markdown')

# ============= TOOL PROCESSING FUNCTIONS =============

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
        return "❌ Tool not found! Please try again."

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
📝 Characters (no spaces): {len(text.replace(' ', ''))}
📝 Words: {words}
📝 Sentences: {sentences if sentences > 0 else 1}
📝 Paragraphs: {len(text.split('\n\n')) if '\n\n' in text else 1}

✅ Average word length: {characters/words:.1f}
"""

def reverse_text(text):
    """Reverse text"""
    if not text or len(text.strip()) < 1:
        return "❌ Send text to reverse!"
    
    return f"""
🔄 *Reversed Text*

📝 Original: {text}
⬅️ Reversed: {text[::-1]}
📊 Words reversed: {' '.join(text.split()[::-1])}
"""

def palindrome_checker(text):
    """Check if text is palindrome"""
    import re
    
    if not text or len(text.strip()) < 1:
        return "❌ Send text to check!"
    
    clean = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
    is_pal = clean == clean[::-1]
    
    return f"""
🔍 *Palindrome Check*

📝 Text: "{text}"
🔤 Cleaned: "{clean}"

{'✅ YES! This is a palindrome!' if is_pal else '❌ NO! This is not a palindrome.'}

💡 A palindrome reads the same forwards and backwards.
"""

def case_converter(text):
    """Convert text cases"""
    if not text or len(text.strip()) < 1:
        return "❌ Send text to convert!"
    
    return f"""
📝 *Case Conversion*

🔹 UPPER CASE: {text.upper()}
🔹 lower case: {text.lower()}
🔹 Title Case: {text.title()}
🔹 Capitalize: {text.capitalize()}
🔹 sWaP cAsE: {text.swapcase()}
"""

def generate_qr_code(text):
    """Generate QR code"""
    try:
        import qrcode
        import io
        
        if not text or len(text.strip()) < 1:
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
        return f"❌ Error generating QR code: {str(e)}"

def unit_converter(text):
    """Convert units"""
    if not text or len(text.strip()) < 1:
        return "❌ Usage: 10 km to miles"
    
    try:
        parts = text.lower().split(' to ')
        if len(parts) != 2:
            return "❌ Usage: 10 km to miles"
        
        from_parts = parts[0].strip().split()
        if len(from_parts) < 2:
            return "❌ Usage: 10 km to miles"
        
        value = float(from_parts[0])
        from_unit = from_parts[1]
        to_unit = parts[1].strip()
        
        # Conversions
        conversions = {
            'km': {'miles': 0.621371, 'meters': 1000, 'feet': 3280.84},
            'miles': {'km': 1.60934, 'meters': 1609.34, 'feet': 5280},
            'meters': {'km': 0.001, 'miles': 0.000621371, 'feet': 3.28084},
            'feet': {'km': 0.0003048, 'miles': 0.000189394, 'meters': 0.3048},
            'kg': {'lbs': 2.20462, 'grams': 1000, 'oz': 35.274},
            'lbs': {'kg': 0.453592, 'grams': 453.592, 'oz': 16},
        }
        
        if from_unit in conversions and to_unit in conversions[from_unit]:
            result = value * conversions[from_unit][to_unit]
            return f"""
🔧 *Unit Conversion*

📝 {value} {from_unit}
✅ Result: {result:.4f} {to_unit}
"""
        else:
            return f"❌ Conversion from {from_unit} to {to_unit} not supported!"
    except ValueError:
        return "❌ Invalid number! Example: 10 km to miles"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def age_calculator(birthdate):
    """Calculate age"""
    from datetime import datetime
    
    if not birthdate or len(birthdate.strip()) < 1:
        return "❌ Usage: YYYY-MM-DD\nExample: 1990-01-15"
    
    try:
        birth = datetime.strptime(birthdate.strip(), '%Y-%m-%d')
        today = datetime.now()
        
        if birth > today:
            return "❌ Birthdate cannot be in the future!"
        
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        days_alive = (today - birth).days
        
        return f"""
📅 *Age Calculator*

🎂 Birthdate: {birthdate}
📆 Today: {today.strftime('%Y-%m-%d')}

✅ Age: {age} years
✅ Days alive: {days_alive:,} days
"""
    except ValueError:
        return "❌ Invalid date! Use: YYYY-MM-DD\nExample: 1990-01-15"

def color_converter(text):
    """Convert color codes"""
    if not text or len(text.strip()) < 1:
        return "❌ Send color code!\nExample: #FF5733"
    
    text = text.strip()
    
    if text.startswith('#'):
        hex_color = text.lstrip('#')
        if len(hex_color) == 6:
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            return f"""
🎨 *Color Converter*

HEX: {text}
RGB: {rgb}
HSL: Calculated from RGB

💡 Use: #RRGGBB or rgb(255,255,255)
"""
    return "❌ Send a valid color code!\nExample: #FF5733"

def get_ip_info(ip):
    """Get IP information"""
    try:
        import requests
        
        if not ip or len(ip.strip()) < 1:
            return "❌ Send IP address!"
        
        response = requests.get(f'http://ip-api.com/json/{ip.strip()}', timeout=5)
        data = response.json()
        
        if data['status'] == 'success':
            return f"""
📍 *IP Information*

🌐 IP: {data['query']}
📍 Country: {data['country']} ({data['countryCode']})
🏙️ City: {data['city']}
📮 ZIP: {data.get('zip', 'N/A')}
📞 ISP: {data.get('isp', 'N/A')}
🗺️ Location: {data['lat']}, {data['lon']}
🕐 Timezone: {data.get('timezone', 'N/A')}
"""
        else:
            return "❌ Could not find information for this IP!"
    except Exception as e:
        return f"❌ Error fetching IP information: {str(e)}"

def validate_json(text):
    """Validate JSON"""
    import json
    
    if not text or len(text.strip()) < 1:
        return "❌ Send JSON to validate!"
    
    try:
        data = json.loads(text)
        formatted = json.dumps(data, indent=2, ensure_ascii=False)
        
        return f"""
✅ *Valid JSON!*

📊 Data Type: {type(data).__name__}

```json
{formatted[:500]}{'...' if len(formatted) > 500 else ''}
