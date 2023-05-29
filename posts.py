import datetime
import json
import random

import requests
from colorama import Fore, Style


def get_post(command):
    """

    :param command: ссылка на паблик
    :return: tuple с двумя элементами: текст сообщения и его вложения (один из аргументов может отсутствовать)
    """
    from config import user_token

    if len(command.split('/')) > 1:
        public_id = command.split('/')[-1]

    else:
        return 'Неверно указан паблик.', ''
    try:
        # Определение короткой ссылки на паблик
        public_arguments = {'group_id': public_id, 'access_token': user_token, 'v': '5.101'}
        public_response = requests.post('https://api.vk.com/method/groups.getById', data=public_arguments)
        public_name = json.loads(public_response.text)['response'][0]['name']
        public_id = int(json.loads(public_response.text)['response'][0]['id'])

        # Определение количества постов
        post_arguments = {'owner_id': -1 * public_id, 'count': 1, 'offset': 0, 'access_token': user_token,
                          'v': '5.101'}
        post_response = requests.post('https://api.vk.com/method/wall.get', data=post_arguments)
        post_response = json.loads(post_response.text)
        post_count = post_response['response']['count']

        # Выбор offset и получение поста
        post_arguments['offset'] = random.randint(0, post_count - 1)
        post_response = requests.post('https://api.vk.com/method/wall.get', data=post_arguments)
        post_response = json.loads(post_response.text)
        post_items = post_response['response']['items'][0]

        message_attachments = ''
        post_text = ''

        # Создание сообщения
        if post_items.get('text') is not None:
            post_text = post_items['text']

        if post_items.get('attachments') is not None:
            post_attachments = post_items['attachments']

            for attachment in post_attachments:
                message_attachments += attachment['type'] + str(
                    attachment[attachment['type']]['owner_id']) + '_' + str(
                    attachment[attachment['type']]['id']) + ','

            message_attachments = message_attachments.strip(',')

        message_text = public_name + '\n' + 'https://vk.com/wall' + str(post_items['from_id']) + '_' + str(
            post_items['id']) + '\n\n' + post_text

        # Проверка на репост
        if post_items.get('copy_history') is not None:

            post_items = post_items['copy_history'][0]

            if post_items.get('text') is not None:
                message_text += '\n\n---НАЧАЛО РЕПОСТА---\n' + post_items['text'] + '\n---КОНЕЦ РЕПОСТА---'

            if post_items.get('attachments') is not None:
                post_attachments = post_items['attachments']

                for attachment in post_attachments:
                    try:
                        message_attachments += ',' + attachment['type'] + str(
                            attachment[attachment['type']]['owner_id']) + '_' + str(
                            attachment[attachment['type']]['id']) + ','
                    except KeyError:
                        pass
                message_attachments = message_attachments.strip(',')

        message = (message_text, message_attachments)
        return message
    except KeyError:
        print(Fore.GREEN + str(datetime.datetime.now().replace(microsecond=0)) + " >> " + Style.RESET_ALL +
              "Message not created, an error occurred. Returning error message.")
        return 'Ошибка при выборе поста, попробуйте позже.', ''
