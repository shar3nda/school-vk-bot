import datetime
import sys
from time import sleep

from colorama import Fore, Style, reinit

from config import vk_api_token, bot_group_id
from server import Server


def start_server():
    try:
        print(Fore.GREEN + str(datetime.datetime.now().replace(microsecond=0)) + " >> " +
              Style.RESET_ALL + 'Starting server...')
        server1.start()
    except Exception as z:
        e = sys.exc_info()[0]
        print(Fore.GREEN + str(datetime.datetime.now().replace(microsecond=0)) + " >> " +
              Style.RESET_ALL + 'Exception: ',
              e, ': ', z, '. Sleeping for 10s...', sep='')
        sleep(10)
        start_server()


reinit()
server1 = Server(vk_api_token, bot_group_id, 'server1')
start_server()
