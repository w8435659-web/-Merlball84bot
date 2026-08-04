import qrcode
import io
import base64
import datetime
import random
import re
from PIL import Image
import barcode
from barcode import EAN13, UPCA, Code128
from barcode.writer import ImageWriter

def unit_converter(text):
    """Convert between units"""
    if not text or len(text.strip()) < 1:
        return "❌ Usage: [value] [from_unit] to [to_unit]\nExample: 10 km to miles"
    
    # Parse input
    parts = text.lower().split(' to ')
    if len(parts) != 2:
        return "❌ Usage: [value] [from_unit] to [to_unit]\nExample: 10 km to miles"
    
    try:
        # Parse first part
        from_parts = parts[0].strip().split()
        if len(from_parts) < 2:
            return "❌ Invalid format! Example: 10 km to miles"
        
        value = float(from_parts[0])
        from_unit = from_parts[1]
        to_unit = parts[1].strip()
        
        # Conversion logic
        conversions = {
            # Length
            'km': {'miles': 0.621371, 'meters': 1000, 'feet': 3280.84},
            'miles': {'km': 1.60934, 'meters': 1609.34, 'feet': 5280},
            'meters': {'km': 0.001, 'miles': 0.000621371, 'feet': 3.28084},
            'feet': {'km': 0.0003048, 'miles': 0.000189394, 'meters': 0.3048},
            
            # Weight
            'kg': {'lbs': 2.20462, 'grams': 1000, 'oz': 35.274},
            'lbs': {'kg': 0.453592, 'grams': 453.592, 'oz': 16},
            'grams': {'kg': 0.001, 'lbs': 0.00220462, 'oz': 0.035274},
            'oz': {'kg': 0.0283495, 'lbs': 0.0625, 'grams': 28.3495},
            
            # Temperature (special handling)
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
        
        return f"""
📅 *Age Calculator*

🎂 Birthdate: {birthdate}
📆 Today: {today.strftime('%Y-%m-%d')}

✅ Age: {age} years
✅ Days alive: {(today - birth).days:,} days
✅ Hours alive: {int((today - birth).total_seconds() / 3600):,} hours
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
