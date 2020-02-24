#!/usr/bin/env python3

import sys, os, requests, re
import vk_api, json, time, datetime
from vk_api.longpoll import VkLongPoll, VkEventType

class BasicSessionResponder:
    def __init__(self, log, pas, tok):
        self.__session = requests.Session()
        self.vk = vk_api.VkApi(log, pas, tok)
        self.vk.auth(token_only=True)
    def __init__(self, tok):
        self.__session = requests.Session()
        self.vk = vk_api.VkApi(tok)
        self.vk.auth(token_only=True)

    def online(self, uid):
        inf = self._whois(uid, 'online')[0]
        return inf['online']

    def many_online(self, uids):
        inf = self.vk.method(
            'users.get',
            {
                'user_ids': ', '.join(map(str, uids)),
                'fields': 'online',
            }
        )
        res = dict()
        for i in inf:
            res[i['id']] = i['online']
        return res

    def whois(self, uid, fields=''):
        return self.vk.method(
            'users.get',
            {
                'user_ids': uid,
                'fields': fields
            }
        )

    def name(self, uid):
        inf = self._whois(uid)[0]
        return inf['first_name'] + ' ' + inf['last_name']

    def friends(self, uid, fields=''):
        return self.vk.method(
            'friends.get',
            {
                'user_id': uid,
                'fields': fields
            }
        )

    def send(self, user_id, message):
        return self.vk.method(
            'messages.send', 
            {
                'user_id': user_id,
                'random_id': 1, ## 
                'message': message
            }
        )
    def chatinfo(self, chat_id, fields=''): # doents work
        return self.vk.method(
            'messages.getChat', 
            {
                'chat_id': chat_id,
                'fields': fields
            }
        )
        

class ChatbotBase(BasicSessionResponder):
    def __init__(self, tok, names=["Bot"]):
        BasicSessionResponder.__init__(self, tok)
        self.longpoll = VkLongPoll(self.vk)
        self.appeals = names
		
    def was_called(self, message):
        for name in self.appeals:
            if bool(re.match("^" + name + "\s*,", message)):
                return True
        return False

    def routine(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                uid = event.used_id
                txt = event.text
                if self.was_called(txt) != -1:
                    self.send(uid, 'msg')


