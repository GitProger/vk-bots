#!/usr/bin/env python3

import sys, os, requests
import vk_api, json, time, datetime
import math

login = 'telephone_number_as_a_string'
password = 'password'

def cur_date():
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
def cur_time():
    info = datetime.datetime.now()
    h = int(info.strftime("%H"))
    m = int(info.strftime("%M"))
#    s = int(info.strftime("%S"))
    return (h, m)

class Lesson:
    def __init__(self, bh, bm, eh, em):
        self.begin = bh * 60 + bm
        self.end   = eh * 60 + em
School = [
    Lesson( 9,  0  ,   9, 40),
    Lesson( 9, 50  ,  10, 30),
    Lesson(10, 45  ,  11, 25),
    Lesson(11, 35  ,  12, 15),
    Lesson(12, 50  ,  13, 30),
    Lesson(13, 40  ,  14, 20),
]

