#!/usr/bin/env python3


import sys, os, requests, re, random
import vk_api, json, time, datetime
import math
from vk_api.longpoll import VkLongPoll, VkEventType
from rbase import ChatbotBase

token = '22208832096fb3b7036116cab6b409de2bca808eb0b292997ed5641fb0683b1efd59b6f129b5a101287bb'

def cur_time():
    return datetime.datetime.now().strftime("%H:%M")

def gen_table():
    return {
        "спасибо"                                      : "Пожалуйста",
        "пока"                                         : "Пока(",
        "((ты(\s|\s.*\s)кто)|(как\sтебя\sзовут))"      : "Я жираф)",
        ":\)"                                          : ":)",
        ":\("                                          : ":(",
        "так$"                                         : "Да?",
        "кста$"                                        : "?",
        "(х(о|а)-?)+"                                  : ";)",
        "(ты)?\s*(лох|дурак|д(е|и)бил|д(э|е)бик)"      : ":'(",
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
                   '''
#                    | ко мне надо обратиться "Бот" или "Bot".
#                   '''
        elif re.search("(как\s.*меня\s.*зовут|мо(е|ё).*\sимя|кто\s+я|я\s*кто)", ptxt):
            return "Тебя зовут " + uname + "."
        elif re.search("привет", ptxt):
            return "Привет, " + uname + "!"
        else:
            return get_answer(ptxt)


    def process(self, event):
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            self.log(event)
            uid = event.user_id
            txt = event.text
            if self.was_called(txt):
                self.send(uid, self.parse(txt, event))

bot = MyBot(token)
bot.routine()

