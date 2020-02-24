#!/usr/bin/env python3


import sys, os, requests, re, random
import vk_api, json, time, datetime
import math
from vk_api.longpoll import VkLongPoll, VkEventType
from rbase import ChatbotBase

token = 'your_access_token'

class MyBot(ChatbotBase):
    def process(self, event):
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.text:
            print(event.user_id, " (" + self.who(event.user_id) + "): ", event.text, sep="")

            self.vk.messages.send(
                user_id = event.user_id,
                message = 'Привет, ' + self.who(event.user_id),
                random_id = random.randint(0, 2 ** 24),
            )	

bot = MyBot(token)
bot.routine()

