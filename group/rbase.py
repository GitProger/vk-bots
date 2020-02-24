#!/usr/bin/env python3

import sys, os, requests, re, random
import vk_api, json, time, datetime
from vk_api.longpoll import VkLongPoll, VkEventType


def list_to_string(lst):
    return ', '.join(map(str, lst))

class ChatbotBase:
    def __init__(self, tok):
        self.vk_sess = vk_api.VkApi(token=tok)
        self.longpoll = VkLongPoll(self.vk_sess)
        self.vk = self.vk_sess.get_api()

    def was_called(self, message):
        for name in self.appeals:
            if bool(re.match("^" + name + "\s*,", message)):
                return True
        return False

    def solve_exc(self, e):
        print("Error:", e)

    def routine(self):
        for event in self.longpoll.listen():
            try:
                self.process(event)
            except Exception as e:
                self.solve_exc(e)

    def who(self, uid):
        json = self.vk.users.get(user_ids=uid, fields='')
        inf = json[0]
        return inf['first_name'] #+ ' ' + inf['last_name']


    def process(self, event):
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print(event.user_id, " (" + self.who(event.user_id) + "): ", event.text, sep="")


            self.vk.messages.send(
                user_id = event.user_id,
                message = 'Привет, ' + self.who(event.user_id),
                random_id = random.randint(0, 2 ** 24),
            )

            '''
            if event.text.find('hi') != -1:
                if event.from_user:
                    self.vk.messages.send(
                        user_id=event.user_id,
                        message='Hello'
		            )
                elif event.from_chat:
                    self.vk.messages.send(
                        chat_id=event.chat_id,
                        message='Hello'
		            )
            '''
