import ctypes
import threading
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

from EmailUtil import EmailUtil


class QiuTanSelenium(object):
    def __init__(self):
        self.infourl = "http://live.win007.com/"
        self.ballteammap = {}
        self.emails = ["1161369126@qq.com","chu1624@126.com"]
    def getInfo(self,driver):
            matchs = []
            if self.isclean():
                self.ballteammap.clear()
            try:
                driver.get(self.infourl)
                driver.set_page_load_timeout(3)
                driver.set_window_size(800, 480)
                driver.find_element_by_id("button6").click()
                pageSource = driver.page_source
                soup = BeautifulSoup(pageSource, 'lxml')
                matchs = soup.select("table.mytable tbody tr[align]")
                if len(matchs) < 1:
                    return
                del matchs[0]
                strs = ""
            except TimeoutException:
                print(11111)
                pass

            for i in matchs:
                if len(i.select("td")) <= 7:
                    continue
                league = i.select("td")[1].text
                times = i.select("td")[3].text
                teama = i.select("td")[4].text
                if len(i.select("td")[5].text.split("-")) < 2 or i.select("td")[5].text ==  "-":
                    continue
                score = int(i.select("td")[5].text.split("-")[0]) + int(i.select("td")[5].text.split("-")[1])
                if not times.isdigit():
                    times = 0
                teamb = i.select("td")[6].text
                # print(league,times,teama,teamb,score)
                if 0 < int(times) < 30 and int(score) >= 3:
                    count = self.add(teama + teamb)
                    if count < 3:
                        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        strs = strs + "北京时间%s,%s联赛:%s队和%s队在开始比赛30分钟前进球数大于等于3\n" % (nowtime, league, teama, teamb)
            if strs != "":
                EmailUtil().send(strs, self.emails)
                self.writefile(strs)
                # self.AutoCloseMessageBoxW(strs, 5)


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

    def begin(self):
        driver = webdriver.Chrome()
        while True:
            self.getInfo(driver)
            time.sleep(15)

    def isclean(self):
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        times = nowtime.split(" ")[1].split(":")
        if (times[0] == "12" and times[1] == "00" and times[1] == "00") or (times[0] == "00" and times[1] == "00" and times[1] == "00"):
            return True
        else:
            return False
if __name__ == '__main__':
    QiuTanSelenium().begin()