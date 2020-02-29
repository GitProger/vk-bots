#!/usr/bin/env python3

import sys, os, requests, re, random
import vk_api, json, time, datetime
from vk_api.longpoll import VkLongPoll, VkEventType


def list_to_string(lst):
    return ', '.join(map(str, lst))
def jsonprint(jsn):
    print(json.dumps(jsn, sort_keys=True, ensure_ascii=False, indent=4))
def get_json(jsn):
    return json.dumps(jsn, sort_keys=True, ensure_ascii=False, indent=4)

class ChatbotBase:
    def __init__(self, tok):
        self.vk_sess = vk_api.VkApi(token=tok)
        self.longpoll = VkLongPoll(self.vk_sess)
        self.vk = self.vk_sess.get_api()
        self.appeals = ["Bot", "Бот"]

    def was_called(self, message):
        for name in self.appeals:
            if re.match("^" + name + "\s*,", message) \
                    or re.match("^" + name.lower() + "\s*,", message):
                return True
        return False

    def send(self, uid, text):
        self.vk.messages.send(
            user_id = uid,
            message = text,
            random_id = random.randint(0, 2 ** 24),
        )

    def who(self, uid, key=''):
        jsn = self.vk.users.get(user_ids=uid, fields='')[0]
        if key == 'name':
            return jsn['first_name']
        elif key == 'surname':
            return jsn['last_name']
        else:
            return jsn['first_name'] + ' ' + jsn['last_name']

    def solve_exc(self, e):
        print("[ERR] ", type(e)," ", e, sep="")

    def routine(self):
        for event in self.longpoll.listen():
            try:
                self.process(event)
            except Exception as e:
                self.solve_exc(e)

    def process(self, event):
        pass
