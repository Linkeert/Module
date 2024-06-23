import random
from datetime import datetime, timedelta
from support_platform import SupportPlatform

#Генерация данных
def generate_random_data():
    first_names = ["Алексей", "Борис", "Владимир", "Дмитрий", "Михаил"]
    last_names = ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов"]
    cities = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань"]
    positions = ["Агент поддержки", "Старший агент поддержки"]
    start_date = datetime(1980, 1, 1)
    end_date = datetime(2002, 12, 31)

    name = f"{random.choice(first_names)} {random.choice(last_names)}"
    city = random.choice(cities)
    birthdate = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    position = random.choice(positions)
    experience = random.randint(1, 20)

    return name, city, birthdate, position, experience

#Рандомные сообщения
def generate_random_message():
    messages = [
        "Я с вами. Чем помочь?",
        "Где мой заказ?",
        "Пришлите, пожалуйста, фотографии поврежденных позиций",
        "Конечно, я могу вам помочь.",
        "Спасибо за вашу помощь!",
    ]
    return random.choice(messages)

def create_demo_platform():
    platform = SupportPlatform()

    #Создание 10 операторов
    for _ in range(10):
        name, city, birthdate, position, experience = generate_random_data()
        platform.add_operator(name, city, birthdate, position, experience)

    #Создание 50 клиентов
    for _ in range(50):
        name, city, birthdate, *_ = generate_random_data()
        platform.add_user(name, city, birthdate)

    #Создание 100 чатов
    for _ in range(100):
        user_id = random.choice(platform.users).user_id
        chat = platform.create_chat(user_id)
        if chat:
            for _ in range(random.randint(1, 10)):
                sender = random.choice([chat.user.name, chat.operator.name])
                chat.add_message(sender, generate_random_message())
            if random.choice([True, False]):
                csat = random.randint(1, 5)
                platform.close_chat(chat.chat_id, csat)

    return platform


def main():
    platform = create_demo_platform()
    
    # Экспорт всех данных в JSON
    platform.export_to_json("support_platform_data.json")
    
    # Вывод чатов конкретного оператора
    operator_id = random.choice(platform.operators).operator_id
    print(f"\nЧаты оператора {operator_id}:")
    for chat in platform.get_chats_by_operator(operator_id):
        print(chat)
    
    # Вывод чатов конкретного пользователя
    user_id = random.choice(platform.users).user_id
    print(f"\nЧаты пользователя {user_id}:")
    for chat in platform.get_chats_by_user(user_id):
        print(chat)

if __name__ == "__main__":
    main()
