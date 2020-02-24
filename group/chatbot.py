#!/usr/bin/env python3


import sys, os, requests, re
import vk_api, json, time, datetime
import math
from rbase import ChatbotBase

token = 'your_access_token'

bot = ChatbotBase(token)
bot.routine()

