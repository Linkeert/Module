import random
import json
from datetime import datetime, timedelta

class Operator:
    def __init__(self, operator_id, name, city, birthdate, position, experience):
        self.operator_id = operator_id
        self.name = name
        self.city = city
        self.birthdate = birthdate
        self.position = position
        self.experience = experience
        self.chats = []

    def __repr__(self):
        return f"Operator({self.operator_id}, {self.name}, {self.city}, {self.birthdate}, {self.position}, {self.experience})"


class User:
    def __init__(self, user_id, name, city, birthdate):
        self.user_id = user_id
        self.name = name
        self.city = city
        self.birthdate = birthdate
        self.chats = []

    def __repr__(self):
        return f"User({self.user_id}, {self.name}, {self.city}, {self.birthdate})"


class Chat:
    def __init__(self, chat_id, user, operator, messages=None, csat=None):
        self.chat_id = chat_id
        self.user = user
        self.operator = operator
        self.messages = messages if messages else []
        self.csat = csat
        self.created_at = datetime.now()
        self.closed_at = None

    def add_message(self, sender, message):
        self.messages.append({
            "sender": sender,
            "message": message,
            "timestamp": datetime.now().isoformat()
        })

    def close_chat(self, csat):
        self.closed_at = datetime.now()
        self.csat = csat

    def __repr__(self):
        return f"Chat({self.chat_id}, {self.user.name}, {self.operator.name}, {self.csat}, {self.created_at}, {self.closed_at})"


class SupportPlatform:
    def __init__(self):
        self.operators = []
        self.users = []
        self.chats = []
        self._next_operator_id = 1
        self._next_user_id = 1
        self._next_chat_id = 1

    def add_operator(self, name, city, birthdate, position, experience):
        operator = Operator(self._next_operator_id, name, city, birthdate, position, experience)
        self.operators.append(operator)
        self._next_operator_id += 1

    def add_user(self, name, city, birthdate):
        user = User(self._next_user_id, name, city, birthdate)
        self.users.append(user)
        self._next_user_id += 1

    def create_chat(self, user_id):
        user = self._get_user_by_id(user_id)
        if not user:
            return None
        operator = self._get_random_available_operator()
        if not operator:
            return None
        chat = Chat(self._next_chat_id, user, operator)
        self.chats.append(chat)
        user.chats.append(chat)
        operator.chats.append(chat)
        self._next_chat_id += 1
        return chat

    def close_chat(self, chat_id, csat):
        chat = self._get_chat_by_id(chat_id)
        if chat:
            chat.close_chat(csat)

    def get_chats(self):
        return self.chats

    def get_chats_by_operator(self, operator_id):
        return [chat for chat in self.chats if chat.operator.operator_id == operator_id]

    def get_chats_by_user(self, user_id):
        return [chat for chat in self.chats if chat.user.user_id == user_id]

    def get_operators(self):
        return self.operators

    def get_users(self):
        return self.users

    def _get_user_by_id(self, user_id):
        for user in self.users:
            if user.user_id == user_id:
                return user
        return None

    def _get_chat_by_id(self, chat_id):
        for chat in self.chats:
            if chat.chat_id == chat_id:
                return chat
        return None

    def _get_random_available_operator(self):
        if not self.operators:
            return None
        return random.choice(self.operators)

    def export_data(self):
        data = {
            "operators": [vars(op) for op in self.operators],
            "users": [vars(user) for user in self.users],
            "chats": []
        }
        for chat in self.chats:
            serialized_chat = {
                "chat_id": chat.chat_id,
                "user": chat.user.name,
                "operator": chat.operator.name,
                "messages": chat.messages,
                "csat": chat.csat,
                "created_at": chat.created_at.isoformat(),
                "closed_at": chat.closed_at.isoformat() if chat.closed_at else None
            }
            data["chats"].append(serialized_chat)
        return data

    def export_to_json(self, filename):
        data = self.export_data()
        with open(filename, 'w') as f:
            json.dump(data, f, default=str, indent=4)