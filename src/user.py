from src.db import db

class User:
    def __init__(self, chat_id):
        self.chat_id = chat_id
        self.db = db
        self.user = self.db.users.find_one({'chat.id': self.chat_id})
        self.state = self.user.get('state')
    
    def current_question(self):
        """
        get the current question
        """
        if not self.user or not self.user.get("current_question"):
            return ' '
        
        current_question = '\n\n'.join(self.user['current_question'])
        return f':right_arrow: Preview Question\n\n {current_question}'
    
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