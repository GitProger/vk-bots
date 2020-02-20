#!/usr/bin/env python3

import sys, os, requests
import vk_api, json, time, datetime
import math

login = '+telephone'
password = 'password'

################################################################################
################################################################################
################################################################################

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
    return [User(u) for u in users]

def write_to_file(users, tm):
    f = open('data.txt', 'w')
    f.write(str(tm) + '\n')
    for user in users:
        f.write('{} {} {}\n'.format(user.uid, user.online, user.total))
    f.close()

def read_from_file():
    f = open('data.txt', 'r')
    users = []
    tm = 0
    ss = f.readlines()
    tm = int(ss[0])
    for i in range(1, len(ss)):
        pars = ss[i].split()
        while len(pars) < 3:
            pars.append(0)
        if pars[0] == 0:
            break
        users.append(User(int(pars[0])))
        users[-1].online = int(pars[1])
        users[-1].total = int(pars[2])
    f.close()
    return (tm, users)

################################################################################
################################################################################
################################################################################


class BasicRobot:
    def __init__(self, log: str, pas: str):
        self.__session = requests.Session()
        self.vk = vk_api.VkApi(log, pas)
        self.vk.auth(token_only=True)

    def _online(self, uid):
        inf = self._whois(uid, 'online')[0]
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
        inf = self._whois(uid)[0]
        return inf['first_name'] + ' ' + inf['last_name']

    def _friends(self, uid, fields=''):
        return self.vk.method(
            'friends.get',
            {
                'user_id': uid,
                'fields': fields
            }
        )

################################################################################
################################################################################
################################################################################

class MyRobot(BasicRobot):
    def routine(self):
        if 0 == 0:
             watch = (
                  460838671, 221493415, 246178303, 415526037,
                  258691338, 266035392, 178101321, 167326970,
                  212694300, 257244889, 287018057, 387610057,
                  429317016, 418500776, 396305534, 247633967,
                  517859380, 351851366, 244962256, 289416361,
                  229801802, 195947948, 570392202, 572297054,
             )
             totaltime = 0
             usrs = make_list(watch)
        else:
            totaltime, usrs = read_from_file()

        INTERVAL = 5
        for user in usrs:
            user.name = self._name(user.uid)

        print('Initialized.')

        while True:
            try:
                time.sleep(60 * INTERVAL)
                os.system('clear')

                totaltime += INTERVAL
                users_online = 0
                onlineinfo = self._many_online([u.uid for u in usrs])

                for user in usrs:
                    user.total += INTERVAL
                    if onlineinfo[user.uid] == 1: # self.__online(user.uid)
                        user.online += INTERVAL
                        user.now = '*'
                        users_online += 1
                    else:
                        user.now = ' '

                    amnt = 100 * user.online / user.total
                    amnt = math.ceil(1000 * amnt) / 1000
                    print(
                        user.name, (30 - len(user.name)) * ' ',
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
                print('* - online users')
                print(users_online, 'users online')

            except:
                write_to_file(usrs, totaltime)
                return -1

def main(args):
    MyRobot(login, password).routine()
    return 0

if __name__ == '__main__':
    exit(main(sys.argv))
