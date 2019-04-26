import sys

from EmailUtil import EmailUtil

sys.path.append("..")
import threading
import easygui as easygui
from apscheduler.triggers.interval import IntervalTrigger
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from HttpClient import HttpClient, Method
import ctypes


class QiuTanSpider(object):
    def __init__(self):
        self.infourl = "http://live.win007.com/vbsxml/bfdata.js?r=007%s000"
        self.httpClient = HttpClient()
        self.tipmaxtimes = 3
        self.ballteammap = {}
        self.emails = ["1030056125@qq.com"]
    def getInfo(self):
        try:
            r = self.httpClient.request(self.infourl % int(time.time()), Method.GET, headers=self.getHeader(),formats="text", encoding="gbk")
            rlist = r.split("\r\n")
            strs = ""
            for i in rlist:
                if i.startswith("A"):
                    j = i.split("^")
                    if len(j) < 15:
                        continue
                    league = j[2]
                    teama = j[5]
                    teamb = j[8]
                    begintime = j[11]
                    scorea = j[14]
                    scoreb = j[15]
                    if self.caldifftime(begintime) and (int(scorea) + int(scoreb)) >= 3:
                        count = self.add(teama + teamb)
                        if count < 3:
                            nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                            strs = strs + "北京时间%s,%s联赛:%s队和%s队在开始比赛30分钟前进球数大于等于3\n" % (nowtime,league,teama,teamb)
            if strs != "":
                self.writefile(strs)
                EmailUtil().send(strs,self.emails)
        except Exception as e:
            self.AutoCloseMessageBoxW("代码异常:"+ str(e),5)

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
        while True:
            self.getInfo()
            time.sleep(15)

    def get(self,teamname):
        return self.ballteammap.get(teamname)

    def set(self,teamname,count):
        self.ballteammap[teamname] = count

    def add(self,teamname):
        count = self.get(teamname)
        if count is None:
            self.set(teamname,1)
            return 1
        else:
            count = count + 1
            self.set(teamname,count)
            return count

    def test(self):
        MessageBox = ctypes.windll.user32.MessageBoxW
        MessageBox(None, 'Hello', 'Window title', 0)

    def worker(self,title, close_until_seconds):
        time.sleep(close_until_seconds)
        wd = ctypes.windll.user32.FindWindowW(0, title)
        ctypes.windll.user32.SendMessageW(wd, 0x0010, 0, 0)
        return

    def AutoCloseMessageBoxW(self,text, close_until_seconds):
        t = threading.Thread(target=self.worker, args=("分数提醒", close_until_seconds))
        t.start()
        ctypes.windll.user32.MessageBoxW(0, text, "分数提醒", 0)

    def writefile(self,text):
        f = open("./历史提醒.txt","a+")
        f.write(text)
        f.flush()
        f.close()


if __name__ == '__main__':
    met = QiuTanSpider()
    met.begin()
