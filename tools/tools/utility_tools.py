import qrcode
import io
import base64
import datetime
import random
import re
from PIL import Image
import barcode
from barcode import EAN13, Code128
from barcode.writer import ImageWriter

def unit_converter(text):
    """Convert between units"""
    if not text or len(text.strip()) < 1:
        return "❌ Usage: [value] [from_unit] to [to_unit]\nExample: 10 km to miles"
    
    parts = text.lower().split(' to ')
    if len(parts) != 2:
        return "❌ Usage: [value] [from_unit] to [to_unit]\nExample: 10 km to miles"
    
    try:
        from_parts = parts[0].strip().split()
        if len(from_parts) < 2:
            return "❌ Invalid format! Example: 10 km to miles"
        
        value = float(from_parts[0])
        from_unit = from_parts[1]
        to_unit = parts[1].strip()
        
        conversions = {
            'km': {'miles': 0.621371, 'meters': 1000, 'feet': 3280.84},
            'miles': {'km': 1.60934, 'meters': 1609.34, 'feet': 5280},
            'meters': {'km': 0.001, 'miles': 0.000621371, 'feet': 3.28084},
            'feet': {'km': 0.0003048, 'miles': 0.000189394, 'meters': 0.3048},
            'kg': {'lbs': 2.20462, 'grams': 1000, 'oz': 35.274},
            'lbs': {'kg': 0.453592, 'grams': 453.592, 'oz': 16},
            'grams': {'kg': 0.001, 'lbs': 0.00220462, 'oz': 0.035274},
            'oz': {'kg': 0.0283495, 'lbs': 0.0625, 'grams': 28.3495},
            'c': {'f': lambda c: c * 9/5 + 32, 'k': lambda c: c + 273.15},
            'f': {'c': lambda f: (f - 32) * 5/9, 'k': lambda f: (f - 32) * 5/9 + 273.15},
            'k': {'c': lambda k: k - 273.15, 'f': lambda k: (k - 273.15) * 9/5 + 32}
        }
        
        if from_unit in conversions and to_unit in conversions[from_unit]:
            result = conversions[from_unit][to_unit]
            if callable(result):
                result = result(value)
            else:
                result = value * result
            
            return f"""
🔧 *Unit Conversion*

📝 {value} {from_unit} = {result:.4f} {to_unit}

✅ Conversion successful!
"""
        else:
            return f"❌ Conversion from {from_unit} to {to_unit} not supported!"
    
    except ValueError:
        return "❌ Invalid number! Example: 10 km to miles"
    except Exception as e:
        return f"❌ Error: {str(e)}"

def age_calculator(birthdate):
    """Calculate age from birthdate"""
    if not birthdate or len(birthdate.strip()) < 1:
        return "❌ Usage: YYYY-MM-DD\nExample: 1990-01-15"
    
    try:
        birth = datetime.datetime.strptime(birthdate.strip(), '%Y-%m-%d')
        today = datetime.datetime.now()
        
        if birth > today:
            return "❌ Birthdate cannot be in the future!"
        
        age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
        next_birthday = datetime.datetime(today.year, birth.month, birth.day)
        if next_birthday < today:
            next_birthday = datetime.datetime(today.year + 1, birth.month, birth.day)
        
        days_until_birthday = (next_birthday - today).days
        days_alive = (today - birth).days
        hours_alive = int((today - birth).total_seconds() / 3600)
        
        return f"""
📅 *Age Calculator*

🎂 Birthdate: {birthdate}
📆 Today: {today.strftime('%Y-%m-%d')}

✅ Age: {age} years
✅ Days alive: {days_alive:,} days
✅ Hours alive: {hours_alive:,} hours
✅ Next birthday in: {days_until_birthday} days
"""
    except ValueError:
        return "❌ Invalid date format! Use: YYYY-MM-DD\nExample: 1990-01-15"

def qr_code(text):
    """Generate QR code from text"""
    if not text or len(text.strip()) < 1:
        return "❌ Send text/URL to generate QR code!"
    
    try:
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        return img_bytes
    except Exception as e:
        return f"❌ Error generating QR code: {str(e)}"

def color_converter(text):
    """Convert color codes between HEX, RGB, HSL"""
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

💡 Use: #RRGGBB, rgb(255,255,255), or hsl(0,100%,50%)
"""
    return "❌ Send a color code to convert!\nExample: #FF5733"

def barcode_generator(text):
    """Generate barcode from text"""
    if not text or len(text.strip()) < 1:
        return "❌ Send number for barcode!"
    
    if not text.isdigit():
        return "❌ Barcode must contain only numbers!"
    
    try:
        if len(text) == 12:
            ean = EAN13(text, writer=ImageWriter())
        else:
            ean = Code128(text, writer=ImageWriter())
        
        buffer = io.BytesIO()
        ean.write(buffer)
        buffer.seek(0)
        
        return buffer
    except Exception as e:
        return f"❌ Error generating barcode: {str(e)}"

def binary_translator(text):
    """Convert text to binary and vice versa"""
    if not text or len(text.strip()) < 1:
        return "❌ Send text to convert to/from binary!"
    
    if all(c in '01 ' for c in text):
        try:
            binary_values = text.split()
            text_result = ''.join(chr(int(binary, 2)) for binary in binary_values)
            return f"""
📊 *Binary Translator*

🔢 Binary: {text}
📝 Text: {text_result}
"""
        except:
            return "❌ Invalid binary format!"
    else:
        binary = ' '.join(format(ord(c), '08b') for c in text)
        return f"""
📊 *Binary Translator*

📝 Text: {text}
🔢 Binary: {binary}

💡 Send binary to convert back to text!
"""

def base64_converter(text):
    """Convert text to/from Base64"""
    if not text or len(text.strip()) < 1:
        return "❌ Send text to encode/decode!"
    
    try:
        decoded = base64.b64decode(text).decode('utf-8')
        return f"""
📊 *Base64 Converter*

🔐 Encoded: {text}
📝 Decoded: {decoded}
"""
    except:
        encoded = base64.b64encode(text.encode()).decode()
        return f"""
📊 *Base64 Converter*

📝 Text: {text}
🔐 Encoded: {encoded}

💡 Send Base64 to decode!
"""

def url_encoder(text):
    """Encode/Decode URL"""
    import urllib.parse
    
    if not text or len(text.strip()) < 1:
        return "❌ Send URL to encode or encoded URL to decode!"
    
    try:
        decoded = urllib.parse.unquote(text)
        if decoded != text:
            return f"""
📊 *URL Encoder/Decoder*

🔗 Decoded: {decoded}
🔐 Encoded: {text}
"""
    except:
        pass
    
    encoded = urllib.parse.quote(text)
    return f"""
📊 *URL Encoder/Decoder*

🔗 Original: {text}
🔐 Encoded: {encoded}
"""
