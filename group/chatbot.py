#!/usr/bin/env python3


import sys, os, requests, re, random
import vk_api, json, time, datetime
import math
from vk_api.longpoll import VkLongPoll, VkEventType
from rbase import ChatbotBase

token = 'your_access_token'

def cur_time():
    return datetime.datetime.now().strftime("%H:%M")


class MyBot(ChatbotBase):
    def log(self, event):
        json = self.vk.users.get(user_ids=uid, fields='')
        inf = json[0]
        n = inf['first_name'] + ' ' + inf['last_name']
        print(event.user_id, " (" + n + "): ", event.text, sep="")
    def send(self, uid, text):
        self.vk.messages.send(
            user_id = uid,
            message = text,
            random_id = random.randint(0, 2 ** 24),
        )

    def parse(self, txt, conf):
        ptxt = txt.lower()
        uname = self.who(conf.user_id)
        if re.search("врем((я)|(ени))", ptxt):
            return "Сейчас " + cur_time() + "."
        elif ptxt == "help":
            return '''
                   Это тестовая версия бота, пока ты можешь только:
                    * спросить сколько времени,
                    * как тебя зовут
                   '''
        elif re.search("(как\s.*меня\s.*зовут|имя)", ptxt):
            return "Тебя зовут " + uname + "."
        else:
            return "Привет, " + uname + "!"
            
    def process(self, event):
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            self.log(event)
            uid = event.user_id
            txt = event.text
            self.send(uid, self.parse(txt, event))            

bot = MyBot(token)
bot.routine()

