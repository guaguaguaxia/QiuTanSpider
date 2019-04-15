import ctypes
import threading
import time

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.interval import IntervalTrigger
from bs4 import BeautifulSoup
from selenium import webdriver

class QiuTanSelenium(object):
    def __init__(self):
        self.infourl = "http://live.win007.com/"
        self.ballteammap = {}
    def getInfo(self,driver):
        try:
            driver.get(self.infourl)
            driver.set_window_size(800, 480)
            driver.find_element_by_id("button6").click()
            pageSource = driver.page_source
            soup = BeautifulSoup(pageSource, 'lxml')
            matchs = soup.select("table.mytable tbody tr[align]")
            if len(matchs) < 1 :
                return
            del matchs[0]
            strs = ""
            for i in matchs:
                if len(i) <= 7:
                    continue
                league = i.select("td")[1].text
                times = i.select("td")[3].text
                teama = i.select("td")[4].text
                if len(i.select("td")[5].text.split("-")[0]) <= 2:
                    continue
                score = int(i.select("td")[5].text.split("-")[0]) + int(i.select("td")[5].text.split("-")[1])
                if not times.isdigit():
                    times = 0
                teamb = i.select("td")[6].text
                if int(times) < 30 and int(score) >= 3:
                    count = self.add(teama + teamb)
                    if count < 3:
                        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        strs = strs + "北京时间%s,%s联赛:%s队和%s队在开始比赛30分钟前进球数大于等于3\n" % (nowtime, league, teama, teamb)
            if strs != "":
                self.writefile(strs)
                self.AutoCloseMessageBoxW(strs, 5)
        except Exception as e:
            self.AutoCloseMessageBoxW("代码异常:"+ str(e),5)

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
        scheduler = BlockingScheduler()
        trigger = IntervalTrigger(seconds=10)
        scheduler.add_job(self.getInfo, trigger,args=[driver])
        scheduler.start()

if __name__ == '__main__':
    QiuTanSelenium().begin()