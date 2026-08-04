import telebot
import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    logger.error("❌ BOT_TOKEN not found!")
    sys.exit(1)

bot = telebot.TeleBot(BOT_TOKEN)
logger.info("✅ Bot initialized successfully!")

# Welcome message
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome = """
🎉 *Welcome!* I'm a bot with 50+ tools!

📚 *Commands:*
/start - Start
/help - Help
/about - About
/tools - List tools

Send me any text to start! ✨
"""
    bot.reply_to(message, welcome, parse_mode='Markdown')
    logger.info(f"✅ User {message.from_user.id} started")

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "📚 *Help*\n\nType /tools to see all available tools!", parse_mode='Markdown')

@bot.message_handler(commands=['about'])
def send_about(message):
    bot.reply_to(message, "🤖 *About*\n\nVersion: 2.0\nMade with ❤️", parse_mode='Markdown')

@bot.message_handler(commands=['tools'])
def send_tools(message):
    tools = """
📝 *Text Tools*
/char_count - Count characters
/password_gen - Generate password
/reverse_text - Reverse text
/palindrome - Check palindrome

📊 *Utility Tools*
/qr_code - Generate QR code
/unit_convert - Convert units
/age_calc - Calculate age

🔍 *Data Tools*
/ip_info - Get IP info
/json_valid - Validate JSON

🧮 *Math Tools*
/calc - Calculator
/bmi - Calculate BMI
/prime - Prime checker
"""
    bot.reply_to(message, tools, parse_mode='Markdown')

# Store user states
user_states = {}

@bot.message_handler(commands=['char_count'])
def handle_char_count(message):
    bot.reply_to(message, "📝 Send me text!")
    user_states[str(message.from_user.id)] = 'char_count'

@bot.message_handler(commands=['password_gen'])
def handle_password(message):
    import random, string
    pwd = ''.join(random.choice(string.ascii_letters + string.digits + "!@#$%^&*") for _ in range(14))
    bot.reply_to(message, f"🔐 *Password:* `{pwd}`", parse_mode='Markdown')

@bot.message_handler(commands=['qr_code'])
def handle_qr(message):
    bot.reply_to(message, "📱 Send text/URL for QR code!")
    user_states[str(message.from_user.id)] = 'qr'

@bot.message_handler(commands=['calc'])
def handle_calc(message):
    bot.reply_to(message, "🧮 Send math expression!")
    user_states[str(message.from_user.id)] = 'calc'

@bot.message_handler(commands=['bmi'])
def handle_bmi(message):
    bot.reply_to(message, "📊 Send: weight(kg) height(cm)")
    user_states[str(message.from_user.id)] = 'bmi'

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    user_id = str(message.from_user.id)
    text = message.text
    
    if user_id in user_states:
        state = user_states[user_id]
        
        if state == 'char_count':
            chars = len(text)
            words = len(text.split())
            bot.reply_to(message, f"📊 *Results*\nCharacters: {chars}\nWords: {words}", parse_mode='Markdown')
        
        elif state == 'qr':
            try:
                import qrcode, io
                qr = qrcode.QRCode(version=1, box_size=10, border=4)
                qr.add_data(text)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                img_bytes = io.BytesIO()
                img.save(img_bytes, format='PNG')
                img_bytes.seek(0)
                bot.send_photo(message.chat.id, img_bytes, caption="✅ QR Code generated!")
            except Exception as e:
                bot.reply_to(message, f"❌ Error: {str(e)}")
        
        elif state == 'calc':
            try:
                import re
                expr = re.sub(r'[^0-9+\-*/().%\s]', '', text)
                result = eval(expr)
                bot.reply_to(message, f"🧮 *Result:* {result}", parse_mode='Markdown')
            except:
                bot.reply_to(message, "❌ Invalid expression!")
        
        elif state == 'bmi':
            try:
                parts = text.split()
                weight = float(parts[0])
                height_cm = float(parts[1])
                height_m = height_cm / 100
                bmi = weight / (height_m ** 2)
                category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
                bot.reply_to(message, f"📊 *BMI:* {bmi:.1f}\nCategory: {category}", parse_mode='Markdown')
            except:
                bot.reply_to(message, "❌ Invalid! Use: 70 175")
        
        del user_states[user_id]
    else:
        bot.reply_to(message, "📝 Send a command or use /tools to see available tools!")

if __name__ == '__main__':
    logger.info("🤖 Bot is starting...")
    bot.polling()
