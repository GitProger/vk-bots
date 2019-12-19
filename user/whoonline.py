#!/usr/bin/env python3

import sys, os, requests
import vk_api, json, time

login = 'telephone_number_as_string'
password = 'password'

def cur_date():
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M")

class User:
    def __init__(self, i):
        self.uid = i
        self.name = ''
        self.total = 0
        self.online = 0
        self.now = False
def make_list(users):
    res = []
    for u in users:
        res.append(User(u))
    return res

class Robot:
    # vk is a vk api session
    @staticmethod
    def jsonprint(jsn):
        print(json.dumps(jsn, sort_keys=True, ensure_ascii=False, indent=4))

    def __init__(self, log: str, pas: str):
        self.__session = requests.Session()
        self.vk = vk_api.VkApi(log, pas, token)
        self.vk.auth(token_only=True)

    #possible fields:
    # nickname, screen_name, sex, bdate, city, country, timezone,
    # photo_50, photo_100, photo_200_orig, has_mobile, contacts,
    # education, online, counters, relation, last_seen, status,
    # can_write_private_message, can_see_all_posts, can_post, universities
    def __online(self, uid):
        inf = self.__whois(uid, 'online')[0]
        return inf['online']


    def __many_online(self, uids):
        inf = self.vk.method(
            'users.get',
            {
                'user_ids': str(list(uids))[1:-1],
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
        watch = (
            #ids
	)
        totaltime = 0
        usrs = make_list(watch)
        for user in usrs:
            user.name = self.__name(user.uid)

        while True:
            time.sleep(60 * 5)
            totaltime += 5
            os.system('clear')

            onlineinfo = self.__many_online(watch)
            for user in usrs:
                user.total += 5
                if onlineinfo[user.uid] == 1: # self.__online(user.uid) == onlineinfo[user.uid]
                    user.online += 5
                    user.now = '*'
                else:
                    user.now = ' '
                amnt = 100 * user.online / user.total
                amnt = math.ceil(1000 * amnt) / 1000
                print(
                    user.name, (30 - len(user.name)) * ' ' ,
                    user.now, ' : ',
                    amnt, '%', (9 - len(str(amnt))) * ' ',
                    'time online', sep=''
                )
            print()
            print(
                'Total time: ',
                 totaltime // (24 * 60), 'd, ',
                 (totaltime % (24 * 60)) // 60, 'h, ',
                 totaltime % 60, 'm', sep=''
            )
            print('Now:', cur_date())
            print('* - online users');

def main(args):
    Robot(login, password).routine()
    return 0

if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except Exception as e:
        print('An exception occured:', type(e))
        print('info:', e)
