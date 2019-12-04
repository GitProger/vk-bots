#!/usr/bin/env python3

import sys, os, requests
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

class Robot:
    # vk is a vk api session
    def __init__(self, tok):
        self.__session = requests.Session()
        self.vk = vk_api.VkApi(token=tok)
        self.authorizated = False;
        self.longpoll = VkLongPoll(self.vk)

    def auth(self):
        if not self.authorizated:
            try:
                self.vk.auth(token_only=True)
                self.authorizated = True
            except vk_api.AuthError as error_msg:
                print(error_msg)
                return

    def method(self, meth, json_dict):
        return self.vk.method(method, json_dict)

    def whois(self, uid):
        return self.vk.method(
            'users.get', 
            {
                'user_ids': uid,
                'fields': 'city'
            }
        )

    def msg(self, user_id, message):
        return self.vk.method(
            'messages.send', 
            {
                'user_id': user_id,
                'message': message
            }
        )

    def routine(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                #print('from ', event.used_id, ':\n', event.text, sep="")
                if event.text.lower().find('кста') != -1:
                    self.msg(event.user_id, '1/100\nскибид вапа)')

                
def main(args):
    token = ''; #your personal key here
    bot = Robot(token)
    bot.auth();
    bot.routine();
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except Exception as e:
        print('An exception occured:', type(e))
        print('info:', e)
