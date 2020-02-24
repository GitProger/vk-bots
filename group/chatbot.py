#!/usr/bin/env python3


import sys, os, requests, re, random
import vk_api, json, time, datetime
import math
from vk_api.longpoll import VkLongPoll, VkEventType
from rbase import ChatbotBase

token = 'your_access_token'

def cur_time():
    return datetime.datetime.now().strftime("%H:%M")

def gen_table():
    return {
        "спасибо": "Пожалуйста",
        "пока"   : "Пока(",
    }

def get_answer(text):
    tab = gen_table()
    for regexp in tab.keys():
        if re.search(regexp, text):
            return tab[regexp]
    return "Не понял запроса."

class MyBot(ChatbotBase):
    def log(self, event):
        i = event.user_id
        print(i, " (", self.who_full(i), "): ", event.text, sep="")

    def parse(self, txt, conf):
        ptxt = txt.lower()
        uname = self.who(conf.user_id)
        if re.search("врем(я|ени)", ptxt):
            return "Сейчас " + cur_time() + "."
        elif ptxt == "help":
            return '''
                   Это тестовая версия бота, пока ты можешь только:
                    * спросить сколько времени,
                    * как тебя зовут
                    * команда chg:
                    --* По умолчанию выключена.
                    --* Переключает режим.
                    --* Если включена, то чтобы я ответил на сообщение 
                    -- ко мне надо обратиться "Бот" или "Bot".
                   '''
        elif re.search("(как\s.*меня\s.*зовут|мо(е|ё).*\sимя|кто\s+я|я\s*кто)", ptxt):
            return "Тебя зовут " + uname + "."
        elif re.search("привет", ptxt):
            return "Привет, " + uname + "!"
        elif re.search("chg\.?$", ptxt):
            self.mode ^= 1
            return "Ок"
        else:
            return get_answer(ptxt)


    def process(self, event):
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            self.log(event)
            uid = event.user_id
            txt = event.text
            if self.ap_mode:
                if self.was_called(txt):
                    self.send(uid, self.parse(txt, event))
            else:
                self.send(uid, self.parse(txt, event))

    def __init__(self, tok):
        ChatbotBase.__init__(self, tok)
        self.ap_mode = 0

bot = MyBot(token)
bot.routine()

