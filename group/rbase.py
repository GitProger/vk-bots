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
        self.appeals = ["Bot", "Бот"]

    def was_called(self, message):
        for name in self.appeals:
            if bool(re.match("^" + name + "\s*,", message.lower())):
                return True
        return False

    def send(self, uid, text):
        self.vk.messages.send(
            user_id = uid,
            message = text,
            random_id = random.randint(0, 2 ** 24),
        )

    def who(self, uid):
        json = self.vk.users.get(user_ids=uid, fields='')
        inf = json[0]
        return inf['first_name']
    def who_full(self, uid):
        json = self.vk.users.get(user_ids=uid, fields='')
        inf = json[0]
        return inf['first_name'] + ' ' + inf['last_name']

    def solve_exc(self, e):
        print("Error:", e)

    def routine(self):
        for event in self.longpoll.listen():
            try:
                self.process(event)
            except Exception as e:
                self.solve_exc(e)

    def process(self, event):
        pass
