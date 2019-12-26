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


class User:
    def __init__(self, i):
        self.uid = i
        self.name = ''
        self.total = 0
        self.online = 0
        self.now = False
        
villains = []

pts_ids_list = [
    #2023a
    #/2023a
    #2022a
     460838671, 221493415, 246178303, 415526037,
     258691338, 266035392, 178101321, 167326970,
     212694300, 257244889, 287018057, 387610057,
     429317016, 418500776, 396305534, 247633967,
     517859380, 351851366, 244962256, 289416361,
     229801802, 195947948, 570392202, 572297054,    
    #/2022a
    #2022b
    #/2022b
    #2021a
    #/2021a
    #2021b
    #/2021b
    #2021v
    #/2021v
    #2020a
    #/2020a
    #2020b
    #/2020b
    #2020v
    #/2020v
]



class Robot:
    def __init__(self, log: str, pas: str):
        self.__session = requests.Session()
        self.vk = vk_api.VkApi(log, pas, token)
        self.vk.auth(token_only=True)

    def __online(self, uid):
        inf = self.__whois(uid, 'online')[0]
        return inf['online']

    def __many_online(self, uids):
        inf = self.vk.method(
            'users.get',
            {
                'user_ids': str(list(uids))[1:-1], #', '.join([str(x) for x in uids])
                'fields': 'online'
            }
        )
        res = dict()
        for i in inf:
            res[i['id']] = i['online']
        return res

    def __whois(self, uid, fields=''):
        return self.vk.method(
            'users.get',
            {
                'user_ids': uid,
                'fields': fields
            }
        )

    def __name(self, uid):
        inf = self.__whois(uid)[0]
        return inf['first_name'] + ' ' + inf['last_name']

    def __friends(self, uid, fields=''):
        return self.vk.method(
            'friends.get',
            {
                'user_id': uid,
                'fields': fields
            }
        )

    def routine(self):
        pass

def main(args):
    Robot(login, password).routine()
    return 0
if __name__ == '__main__':
    exit(main(sys.argv))
