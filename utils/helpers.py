from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    """Create main menu keyboard"""
    keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    
    btn1 = KeyboardButton("📝 Text Tools")
    btn2 = KeyboardButton("📊 Utility Tools")
    btn3 = KeyboardButton("🔍 Data Tools")
    btn4 = KeyboardButton("🧮 Math Tools")
    btn5 = KeyboardButton("❓ Help")
    
    keyboard.add(btn1, btn2, btn3, btn4, btn5)
    return keyboard

def get_tools_keyboard():
    """Create tools category keyboard"""
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    btn_text = InlineKeyboardButton("📝 Text", callback_data='text_tools')
    btn_utility = InlineKeyboardButton("📊 Utility", callback_data='utility_tools')
    btn_data = InlineKeyboardButton("🔍 Data", callback_data='data_tools')
    btn_math = InlineKeyboardButton("🧮 Math", callback_data='math_tools')
    btn_all = InlineKeyboardButton("📋 All Tools", callback_data='all_tools')
    
    keyboard.add(btn_text, btn_utility, btn_data, btn_math, btn_all)
    return keyboard

def format_result(title, result, tool_type="text"):
    """Format tool result for display"""
    if tool_type == "text":
        return f"📝 *{title}*\n\n{result}"
    elif tool_type == "utility":
        return f"🔧 *{title}*\n\n{result}"
    elif tool_type == "data":
        return f"🔍 *{title}*\n\n{result}"
    elif tool_type == "math":
        return f"🧮 *{title}*\n\n{result}"
    else:
        return f"*{title}*\n\n{result}"

def format_error(message):
    """Format error message"""
    return f"❌ *Error*\n\n{message}"

def is_valid_url(url):
    """Check if URL is valid"""
    import re
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def truncate_text(text, max_length=1000):
    """Truncate text to max_length"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
