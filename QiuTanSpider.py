import ctypes
import os
import sys

import easygui as easygui
from apscheduler.triggers.interval import IntervalTrigger

sys.path.append("..")
import time
from tkinter import messagebox, Tk
from apscheduler.schedulers.blocking import BlockingScheduler
from HttpClient import HttpClient, Method


class QiuTanSpider(object):
    def __init__(self):
        self.infourl = "http://live.win007.com/vbsxml/bfdata.js?r=007%s000"
        self.httpClient = HttpClient()

    def getInfo(self):
        try:
            r = self.httpClient.request(self.infourl % int(time.time()), Method.GET, headers=self.getHeader(),formats="text", encoding="gbk")
            rlist = r.split("\r\n")
            strs = ""
            for i in rlist:
                if i.startswith("A"):
                    j = i.split("^")
                    teama = j[5]
                    teamb = j[8]
                    begintime = j[11]
                    scorea = j[14]
                    scoreb = j[15]
                    if self.caldifftime(begintime) and (int(scorea) + int(scoreb)) >= 3:
                        strs = strs + "%s队和%s队在开始比赛30分钟前进球数大于等于3\n" % (teama, teamb)
            if strs != "":
                self.hit_me(strs)
        except Exception as e:
            self.hit_me(e)

    def getHeader(self):
        return {
            "Host": "live.win007.com",
            "Referer": "http://live.win007.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }

    def hit_me(self, strs):
        easygui.msgbox(strs, '分数提醒')



    def caldifftime(self, time2):
        nowtimestamp = int(time.time())
        now = time.localtime()
        format_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
        timestr = format_time.split(" ")[0] + " " + time2
        ts = time.strptime(timestr, "%Y-%m-%d %H:%M")
        ts = int(time.mktime(ts))
        if (nowtimestamp - ts) > 0 and (nowtimestamp - ts) < 1800:
            return True
        else:
            return False

    def begin(self):
        scheduler = BlockingScheduler()
        trigger = IntervalTrigger(seconds=10)
        scheduler.add_job(self.getInfo, trigger)
        scheduler.start()



if __name__ == '__main__':
    # QiuTanSpider().hit_me("211111111111111111111")
    QiuTanSpider().begin()
