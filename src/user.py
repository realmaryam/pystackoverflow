from src.db import db
from src.constants import keys
import emoji

class User:
    def __init__(self, chat_id, mongodb, bot):
        self.chat_id = chat_id
        self.db = mongodb
        self.bot = bot

    @property
    def user(self):
        return self.db.find_one({'chat.id': self.chat_id})
    
    @property
    def state(self):
        return self.db.users.get('state')

    @property
    def current_question(self):
        """
        get the current question message
        """
        user = self.user
        if not user or not user.get("current_question"):
            return ' '
        
        current_question = ':pencil: Question Preview\n\n'
        current_question += '\n'.join(user['current_question'])
        current_question += f'\n {"_" * 40}\n When done, click {keys.send_question}.'
        return current_question
    
    def send_message(self, text, reply_markup=None, emojize=True):
        """
        send message to the user
        """
        #TODO: fix duplicate send_message in run.py and here
        if emojize:
            text = emoji.emojize(text)
        self.bot.send_message(self.chat_id, text, reply_markup=reply_markup)


    def update_state(self, state):
        """
        update user state
        """
        self.db.users.update_one(
            {"chat_id": self.chat_id},
            {"$set": {"state": state}}
            )
        
    def reset(self):
        self.db.users.update_one(
            {"chat_id": self.chat_id},
            {"$set": {"current_question": []}}
        )

if __name__ == '__main__':
    u = User(104668291)
    print(u.current_question())