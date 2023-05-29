import datetime

import lessons
import posts
from config import bot_help, timetable


def process_input(msg):
    """

    :param msg: сообщение пользователя
    :return: tuple с двумя элементами: текст сообщения и его вложения (один из аргументов может быть пустой строкой)
    """
    message_words = msg.split(' ')

    if message_words[0] == '!пост' and len(message_words) > 1:
        public_name = ' '.join(message_words[1:])
        return posts.get_post(public_name)
    elif message_words[0] == '!пост' and len(message_words) <= 1:
        return 'Не указан паблик.', ''

    elif message_words[0] == '!расписание':
        days = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье']
        if len(message_words) > 1:
            return lessons.get_lessons(message_words[1]), ''
        else:
            if len(timetable) < datetime.datetime.today().isoweekday():
                return str(lessons.get_lessons(days[0])), ''
            else:
                return str(lessons.get_lessons(days[datetime.datetime.today().isoweekday()])), ''

    elif message_words[0] == '!помощь':
        return bot_help, ''
    elif message_words[0] == '!корги':
        return posts.get_post('/corgo')
