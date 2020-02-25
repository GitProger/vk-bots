#!/usr/bin/env python3


import sys, os, requests, re, random
import vk_api, json, time, datetime
import math
from vk_api.longpoll import VkLongPoll, VkEventType
from rbase import *

login = 'admin`s login'       # some methods (for instance 'likes.*') are not avaliable with group session
password = 'admin`s password' # so, these params requiered for warking with another sessions from the admin`s account

token = 'group_access_token'

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
        "прости|извини"                                : "Ничего)",
    }

def get_answer(text):
    tab = gen_table()
    for regexp in tab.keys():
        if re.search(regexp, text):
            return tab[regexp]
    return "Не понял запроса."

class MyBot(ChatbotBase):
    def __init__(self, tok, log, pas):
        ChatbotBase.__init__(self, tok)
        self.api = vk_api.VkApi(log, pas)
        self.api.auth(token_only=True)
        self.api = self.api.get_api()

    def log(self, event):
        i = event.user_id
        print("[MSG] [id", i, " (", self.who_full(i), ")]: ", event.text, sep="")
    def like_avatar(self, uid):
        ava = self.vk.users.get(user_ids=uid, fields="photo_id")[0]["photo_id"]
        self.api.likes.add(
            owner_id=uid,
            item_id=ava[ava.index("_") + 1:],
            type="photo",
        )

    def search(self, uid, fr_name): #in friends list
        inf = self.api.friends.search(user_id=uid, q=fr_name)["items"]
        return int(inf[0]["id"])
    def last_time(self, who, user):
        if user.isdigit():
            uid = int(user)
        else:
            uid = self.search(who, user)
        user = self.who_full(uid)
        info = self.api.users.get(user_ids=uid, fields="online, last_seen")[0]
        if info["online"]:
            return user + " онлайн."
        else:
            return user + " был(а) в " + time.ctime(info["last_seen"]["time"]) + "."

    def parse(self, txt, conf):
        ptxt = txt.lower()
        uname = self.who(conf.user_id)
        if re.search("врем(я|ени)", ptxt):
            return "Сейчас " + cur_time() + "."
        elif re.search("help", ptxt):
            return '''
                   Это тестовая версия бота, пока ты можешь только:
                    * спросить сколько времени,
                    * спросить как тебя зовут
                    * попросить лайкнуть аву
                    * спросить когда другой ползователь (должен быть другом) был онлайн

                    ко мне надо обратиться "Бот" или "Bot".
                   '''
        elif re.search("(как\s.*меня\s.*зовут|мо(е|ё).*\sимя|кто\s+я|я\s+кто)", ptxt):
            return "Тебя зовут " + uname + "."
        elif re.search("привет", ptxt):
            return "Привет, " + uname + "!"
        elif re.search("(лайк.*\sаву?|аву?.*\sлайк)", ptxt):
            self.like_avatar(conf.user_id)
            return "Хорошо)"

        elif re.search("когда\sбыл", ptxt) or re.search("когда\sзаходил", ptxt) :
            def get(key):
                nonlocal ptxt, conf
                inter = re.search("(?<=" + key + ").*(?=[\S\W])", ptxt)
                if not inter:
                    return None
                inter = inter.span()
                wanted = txt[inter[0]:inter[1]]
                return self.last_time(conf.user_id, wanted)
            for k in ["когда\sбыла\s", "когда\sбыл\s", "когда\sзаходила\s", "когда\sзаходил\s"]:
                if get(k):
                    return get(k)
            return "Error"
        else:
            return get_answer(ptxt)

    def process(self, event):
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            self.log(event)
            uid = event.user_id
            txt = event.text
            if self.was_called(txt) or txt.lower() == "help":
                self.send(uid, self.parse(txt, event))

bot = MyBot(token, login, password)
bot.routine()
