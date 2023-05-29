import datetime
import json
import sys
import time
from random import randint

import requests
import schedule
from colorama import Fore, Style, reinit

from config import group_token, user_token


def send_and_pin():
    reinit()
    random_id = randint(0, 9223372036854775807)
    data = {'chat_id': 122, 'message': 'test', 'random_id': random_id,
            'access_token': group_token, 'v': '5.102'}
    response = json.loads(requests.post('https://api.vk.com/method/messages.send', data=data).text)
    print(response)
    # while True:
    #     try:
    #         photos = json.loads(
    #             requests.post('https://api.vk.com/method/messages.getHistoryAttachments', data=data).text)
    #         for attachment in photos['response']['items']:
    #             f.write('photo' + str(attachment['attachment']['photo']['owner_id']) + '_' + str(
    #                 attachment['attachment']['photo']['id']) + '_' + attachment['attachment']['photo'][
    #                         'access_key'] + '\n')
    #         data['start_from'] = photos['response']['next_from']
    #         time.sleep(.34)
    print(Fore.GREEN + str(datetime.datetime.now().replace(microsecond=0)) + " >> " + Style.RESET_ALL + 'Message sent.')


def run():
    try:
        send_and_pin()
    except Exception as z:
        e = sys.exc_info()[0]
        print(Fore.GREEN + str(datetime.datetime.now().replace(microsecond=0)) + " >> " +
              Style.RESET_ALL + 'Exception: ',
              e, ': ', z, '. Sleeping for 10s...', sep='')
        time.sleep(10)
        run()


schedule.every(10).seconds.do(run)
while True:
    schedule.run_pending()
    time.sleep(1)
