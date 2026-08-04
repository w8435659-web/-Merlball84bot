import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    PORT = int(os.getenv('PORT', 8080))
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    
    user_states = {}
    
    @classmethod
    def get_user_state(cls, user_id):
        return cls.user_states.get(str(user_id))
    
    @classmethod
    def set_user_state(cls, user_id, state):
        cls.user_states[str(user_id)] = state
    
    @classmethod
    def clear_user_state(cls, user_id):
        if str(user_id) in cls.user_states:
            del cls.user_states[str(user_id)]
