import datetime
import random

import vk_api.vk_api
from colorama import Fore, Style
from vk_api.bot_longpoll import VkBotEventType
from vk_api.bot_longpoll import VkBotLongPoll

from commands import process_input
from config import commands


class Server:

    def __init__(self, api_token, group_id, server_name: str = 'Empty'):
        self.server_name = server_name
        self.vk = vk_api.VkApi(token=api_token)
        self.long_poll = VkBotLongPoll(self.vk, group_id)
        self.vk_api = self.vk.get_api()

    def send_msg(self, send_id, message='', attachment=''):
        self.vk_api.messages.send(peer_id=send_id, message=message, attachment=attachment,
                                  random_id=random.randint(0, 9223372036854775807))

    def start(self):
        for event in self.long_poll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                if str(event.object.text).startswith(commands):
                    print(Fore.GREEN + str(datetime.datetime.now().replace(microsecond=0)) + " >> " + Style.RESET_ALL +
                          Fore.CYAN + '@' + str(event.object.peer_id) + Style.RESET_ALL + ' ' + event.object.text)
                    args = process_input(event.object.text)
                    self.send_msg(event.object.peer_id, *args)
                elif random.randint(1, 45) == 1 and event.object.peer_id == 2000000002:
                    if random.randint(1, 2) == 1:
                        args = list(process_input('!пост /corgo'))
                        args[0] = 'Вы выиграли в русскую рулетку!\n' + args[0]
                        self.send_msg(event.object.peer_id, *args)
                    else:
                        args = list(process_input('!пост /feminism_visually'))
                        args[0] = 'Вы проиграли в русскую рулетку!\n' + args[0]
                        self.send_msg(event.object.peer_id, *args)
