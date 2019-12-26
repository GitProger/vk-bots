#!/usr/bin/env python3

import sys, os, requests
import vk_api, json, time, datetime
import math

login = 'telephone_number_as_a_string'
password = 'password'

def cur_date():
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
def cur_time():
    h = 0
    m = 0
    s = 0
    return (h, m, s)
