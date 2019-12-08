#!/usr/bin/env python3

import sys, os, requests
import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType

login = 'yourtelephonenumber'
password = 'yourpass'
token = '' #not nessasary for user bot
# longpool and most of messages.*
# dont work with user account

class Robot:
    # vk is a vk api session
    @staticmethod
    def jsonprint(jsn):
        print(json.dumps(jsn, sort_keys=True, ensure_ascii=False, indent=4))
    
    def __init__(self, log: str, pas: str):
        self.__session = requests.Session()
        self.vk = vk_api.VkApi(log, pas, token)
        self.authorizated = False;
    #    self.longpoll = VkLongPoll(self.vk)
    def auth(self):
        if not self.authorizate:
            try:
                self.vk.auth(token_only=True)
                self.authorizated = True
            except vk_api.AuthError as error_msg:
                print(error_msg)
                return

    #possible fields:
    # nickname, screen_name, sex, bdate, city, country, timezone,
    # photo_50, photo_100, photo_200_orig, has_mobile, contacts,
    # education, online, counters, relation, last_seen, status,
    # can_write_private_message, can_see_all_posts, can_post, universities        

    def __whois(self, uid, fields=''):
        return self.vk.method(
            'users.get', 
            {
                'user_ids': uid,
                'fields': fields
            }
        )
    def __msg(self, user_id, message):
        return self.vk.method(
            'messages.send', 
            {
                'user_id': user_id,
                'random_id': 1, ## 
                'message': message
            }
        )
    def __chatinfo(self, chat_id, fields=''): # doents work
        return self.vk.method(
            'messages.getChat', 
            {
                'chat_id': chat_id,
                'fields': fields
            }
        )

    def __friends(self, uid, fields=''):
        return self.vk.method(
            'friends.get', 
            {
                'user_id': uid,
                'fields': fields
            }
        )

    def routine(self):
        while True:
            try:
                cmds = list(map(str, input().split()))
                cmd = cmds[0]
                if cmds[1] != 'me':
                    _id = int(cmds[1])
                else:
                    _id = your_id
                fl = ''
                if len(cmds) == 3:
                    fl = cmds[2]
                if cmd == 'user':
                    Robot.jsonprint(self.__whois(_id, fl))
                elif cmd == 'friends':
                    Robot.jsonprint(self.__friends(_id, fl))
            except KeyboardInterrupt:
                print('Exited')
                exit(1)
            except:
                print('Error')
#            for event in self.longpoll.listen():
#                if event.type == VkEventType.MESSAGE_NEW:
#                    print('user', event.used_id, 'sent')
#                    print(event.text)
                
def main(args):
    bot = Robot(login, password)
    bot.auth();
    bot.routine();
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except Exception as e:
        print('An exception occured:', type(e))
        print('info:', e)
