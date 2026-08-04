import re
import random
import string
from collections import Counter

def character_counter(text):
    """Count characters, words, and sentences in text"""
    if not text or len(text.strip()) < 1:
        return "❌ Please send some text to analyze!"
    
    characters = len(text)
    words = len(text.split())
    sentences = len(re.findall(r'[.!?]+', text))
    
    # Fixed: Removed backslash from f-string
    avg_word_length = characters / words if words > 0 else 0
    words_per_sentence = words / sentences if sentences > 0 else words
    
    return f"""
📊 *Text Analysis Results*

📝 Characters: {characters}
📝 Characters (no spaces): {len(text.replace(' ', ''))}
📝 Words: {words}
📝 Sentences: {sentences}
📝 Paragraphs: {len(text.split(chr(10) + chr(10)))}

✅ Average word length: {avg_word_length:.1f} characters
✅ Words per sentence: {words_per_sentence:.1f}
"""

def case_converter(text):
    """Convert text between different cases"""
    if not text or len(text.strip()) < 1:
        return "❌ Please send text to convert!"
    
    return f"""
📝 *Case Conversion*

🔹 UPPER CASE: {text.upper()}
🔹 lower case: {text.lower()}
🔹 Title Case: {text.title()}
🔹 Capitalize: {text.capitalize()}
🔹 sWaP cAsE: {text.swapcase()}
"""

def password_generator(text=None):
    """Generate a strong password"""
    length = 14
    chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
    password = ''.join(random.choice(chars) for _ in range(length))
    
    return f"""
🔐 *Strong Password Generated*

`{password}`

✅ Length: {length}
✅ Includes: Uppercase, Lowercase, Numbers, Special chars
✅ Strength: Very Strong

💡 Tap the password to copy it!
"""

def palindrome_checker(text):
    """Check if text is a palindrome"""
    if not text or len(text.strip()) < 1:
        return "❌ Send text to check if it's a palindrome!"
    
    # Remove spaces and punctuation, convert to lowercase
    clean_text = re.sub(r'[^a-zA-Z0-9]', '', text).lower()
    is_palindrome = clean_text == clean_text[::-1]
    
    return f"""
🔍 *Palindrome Check*

📝 Text: "{text}"
🔤 Cleaned: "{clean_text}"

{'✅ YES! This is a palindrome!' if is_palindrome else '❌ NO! This is not a palindrome.'}

💡 A palindrome reads the same forwards and backwards.
"""

def reverse_text(text):
    """Reverse text"""
    if not text or len(text.strip()) < 1:
        return "❌ Send text to reverse!"
    
    reversed_chars = text[::-1]
    reversed_words = ' '.join(text.split()[::-1])
    
    return f"""
🔄 *Reversed Text*

📝 Original: {text}

⬅️ Reversed: {reversed_chars}

📊 Words reversed: {reversed_words}
"""

def word_frequency(text):
    """Analyze word frequency in text"""
    if not text or len(text.strip()) < 1:
        return "❌ Send text to analyze word frequency!"
    
    words = re.findall(r'[a-zA-Z]+', text.lower())
    if not words:
        return "❌ No words found in your text!"
    
    freq = Counter(words)
    top_words = freq.most_common(10)
    total_words = len(words)
    unique_words = len(freq)
    
    result = "📊 *Word Frequency Analysis*\n\n"
    result += f"📝 Total words: {total_words}\n"
    result += f"📝 Unique words: {unique_words}\n\n"
    
    result += "*Top 10 most common words:*\n"
    for word, count in top_words:
        percentage = (count / total_words) * 100
        result += f"• {word}: {count} times ({percentage:.1f}%)\n"
    
    return result

def lorem_ipsum(text=None):
    """Generate lorem ipsum text"""
    lorem_texts = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        "Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium.",
        "Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit.",
        "Neque porro quisquam est, qui dolorem ipsum quia dolor sit amet, consectetur, adipisci velit."
    ]
    
    num_paragraphs = random.randint(2, 4)
    selected = random.sample(lorem_texts, min(num_paragraphs, len(lorem_texts)))
    result = "\n\n".join(selected)
    
    return f"""
📝 *Lorem Ipsum Generator*

{result}

💡 Placeholder text for design and layout testing.
"""

def acronym_generator(phrase):
    """Generate acronym from phrase"""
    if not phrase or len(phrase.strip()) < 1:
        return "❌ Send a phrase to generate acronym!"
    
    words = phrase.split()
    acronym = ''.join(word[0].upper() for word in words if word)
    
    return f"""
🔤 *Acronym Generator*

📝 Phrase: {phrase}
🔠 Acronym: {acronym}

💡 Used for creating memorable abbreviations!
"""

def random_word_generator(count=5):
    """Generate random words"""
    word_list = [
        'apple', 'banana', 'cherry', 'dragon', 'eagle', 'forest', 'garden',
        'horizon', 'island', 'journey', 'kingdom', 'liberty', 'mountain',
        'nature', 'ocean', 'planet', 'river', 'sunshine', 'tree', 'unicorn',
        'valley', 'waterfall', 'xenon', 'youth', 'zeppelin'
    ]
    
    words = random.sample(word_list, min(count, len(word_list)))
    return "📝 *Random Words*\n\n" + "\n".join(f"• {word}" for word in words)
