# -*- coding: utf-8 -*-
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from random import randint
from db import UsersInfo as user
import time

def main():
    vk_session = vk_api.VkApi(token='ваш token сообщества')

    longpoll = VkBotLongPoll(vk_session, 'ваш ID сообщества')

    vk = vk_session.get_api()

    try:
        for event in longpoll.listen():

            if event.type == VkBotEventType.MESSAGE_NEW:
                text = event.obj.text
                user_id = event.obj.from_id
                if event.obj.peer_id < 2000000000:
                    if user.is_reg(user_id) == False:
                        if text.lower() == "начать":
                            user.insert(user_id)
                            keyboard = VkKeyboard(one_time = False, inline = False)
                            keyboard.add_button(label = 'Клик 💥', color = VkKeyboardColor.PRIMARY)
                            keyboard.add_line()
                            keyboard.add_button(label = 'Топ игроков 👥', color = VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button(label = 'Помощь 📚', color = VkKeyboardColor.POSITIVE) 
                            vk.messages.send(user_id = user_id,
                            random_id = get_random_id(),
                            keyboard = keyboard.get_keyboard(),
                            message = "Вы зарегистирировались в чат-игре Кликер 👍🏻\nКликайте на кнопку 'Клик' и зарабатывайте очки 💥\n\nДля просмотра топа игроков по кликам нажмите кнопку 'Топ игроков' 👥\n\nЕсли нужна помощь используйте команду 'помощь' 📣\n\nПриятной игры 😘")

                    else:
                        if text.lower() == "помощь" or text == "Помощь 📚":
                            vk.messages.send(user_id = user_id,
                            random_id = get_random_id(),
                            message = "Чат-игра кликер - игра, суть которой заключается в наборе очков топа благодаря кликам на главную кнопку 💥\n\nЕсли у вас пропала клавиатура напишите любое сообщение, которое не похоже на команды 💡")
                        
                        elif text.lower() == "клик" or text == "Клик 💥":
                            point = randint(1, 3)
                            vk.messages.send(user_id = user_id,
                            random_id = get_random_id(),
                            message = f"Вы кликнули и получили +{point} {'очко' if point == 1 else 'очка'} топа 💥")
                            user.update(user_id, user.get_clicks(user_id) + point)

                        elif text.lower() == "топ игроков" or text == "Топ игроков 👥":
                            if user.rows() <= 15:
                                mes_text = "Топ игроков по кликам 👥\n\n"
                                top = user.get_top(user.rows())
                                data = vk.users.get(user_ids = ", ".join([str(i[0]) for i in top]))
                                for i, value in enumerate(top):
                                    name = data[i]["first_name"]
                                    family = data[i]["last_name"]
                                    mes_text += f"- {name} {family} [{value[1]} шт.] 👍🏻\n" 

                                mes_text += "\nКликайте больше и возвышайтесь в топы 📣"
                                vk.messages.send(user_id = user_id,
                                random_id = get_random_id(),
                                message = mes_text)
                            else:
                                mes_text = "Топ-15 игроков по кликам 👥\n\n"
                                top = user.get_top(15)
                                data = vk.users.get(user_ids = ", ".join([str(i[0]) for i in top]))
                                for i, value in enumerate(top):
                                    name = data[i]["first_name"]
                                    family = data[i]["last_name"]
                                    mes_text += f"- {name} {family} [{value[1]} шт.] 👍🏻\n" 

                                mes_text += "\nКликайте больше и возвышайтесь в топы 📣"
                                vk.messages.send(user_id = user_id,
                                random_id = get_random_id(),
                                message = mes_text)
                        else:
                            keyboard = VkKeyboard(one_time = False, inline = False)
                            keyboard.add_button(label = 'Клик 💥', color = VkKeyboardColor.PRIMARY)
                            keyboard.add_line()
                            keyboard.add_button(label = 'Топ игроков 👥', color = VkKeyboardColor.POSITIVE)
                            keyboard.add_line()
                            keyboard.add_button(label = 'Помощь 📚', color = VkKeyboardColor.POSITIVE) 
                            vk.messages.send(user_id = user_id,
                            random_id = get_random_id(),
                            message = "Неизвестная команда 🚫\n\n\nКлавиатура отправлена ✅")

    except TimeoutError:
            print("--------------- [ СЕТЕВАЯ ОШИБКА ] ---------------")
            print("Переподключение к серверам...")
            time.sleep(3)                                                   

                

if __name__ == '__main__':
    main()