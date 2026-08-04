import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Bot configuration"""
    
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    PORT = int(os.getenv('PORT', 8080))
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    # User state management (in-memory for development)
    user_states = {}
    
    @classmethod
    def get_user_state(cls, user_id):
        """Get current state for user"""
        return cls.user_states.get(str(user_id))
    
    @classmethod
    def set_user_state(cls, user_id, state):
        """Set state for user"""
        cls.user_states[str(user_id)] = state
    
    @classmethod
    def clear_user_state(cls, user_id):
        """Clear state for user"""
        if str(user_id) in cls.user_states:
            del cls.user_states[str(user_id)]
    
    @classmethod
    def is_valid_token(cls):
        """Check if bot token is set"""
        return cls.BOT_TOKEN and cls.BOT_TOKEN != 'YOUR_BOT_TOKEN_HERE'
