#!/usr/bin/env python3

import sys, os, requests
import vk_api, json, time, datetime
import math

login = '+79811203733'
password = '#1$1%9@6%35'
token = '5511f03bf65c185d47d085904ad239bb7d678beb32caebfce81ef76d90d9727a32e8a26d3b1283b486f20'

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

def check_is_online(time):
    global School
    t = time[0] * 60 + time[1]
    for l in School:
        if (l.begin <= t) and (t < l.end):
            return True
    return False

def log_crime(text):
    f = open("log.txt", "a")
    f.write(text)
    f.close()

class User:
    def __init__(self, i):
        self.uid = i
        self.name = ''
        
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



class BasicRobot:
    def __init__(self, log: str, pas: str):
        self.__session = requests.Session()
        self.vk = vk_api.VkApi(log, pas, token)
        self.vk.auth(token_only=True)

    def _online(self, uid):
        inf = self.__whois(uid, 'online')[0]
        return inf['online']

    def _many_online(self, uids):
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

    def _whois(self, uid, fields=''):
        return self.vk.method(
            'users.get',
            {
                'user_ids': uid,
                'fields': fields
            }
        )

    def _name(self, uid):
        inf = self.__whois(uid)[0]
        return inf['first_name'] + ' ' + inf['last_name']

    def _many_names(self, uids):
        inf = self.vk.method('users.get',
            {
                'user_ids': str(list(uids))[1:-1], #', '.join([str(x) for x in uids])
            }
        )
        res = dict()
        for i in inf:
            res[i['id']] = i['first_name'] + ' ' + i['last_name']
        return res

    def _friends(self, uid, fields=''):
        return self.vk.method(
            'friends.get',
            {
                'user_id': uid,
                'fields': fields
            }
        )
        
    def routine(self):
        pass


class LessonRobot(BasicRobot):
    def routine(self):
        def make_list(users):
            return [User(u) for u in users]
        global pts_ids_list
        INTERVAL = 0.5
        print("Initialized.")

        usrs = make_list(pts_ids_list)
        names = self._many_names(pts_ids_list)
        for user in usrs:
            user.name = names[user.uid]

        while True:
            time.sleep(60 * INTERVAL)
            onlineinfo = self._many_online(pts_ids_list)
            curtime = cur_time()
            for user in usrs:
                if onlineinfo[user.uid] == 1:
                     if check_is_online(curtime):
                         log_crime(user.name + " " + str(curtime[0]) + ":" + str(curtime[1]))

def main(args):
    try:
        LessonRobot(login, password).routine()
    except Exception as e:
        print("An exception occured: ", type(e))
        print("Info: " + 44 * "=" + "\n", e, "\n" + "=" * 50)
    finally:
        print("Exited.")
    return 0
if __name__ == '__main__':
    exit(main(sys.argv))
