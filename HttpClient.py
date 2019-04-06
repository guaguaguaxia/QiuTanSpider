import requests
import os
from enum import Enum


TIME_OUT=25
class Method(Enum):
    GET=1
    POST=2 
class HttpClient(object):
    def __init__(self):
        self.session=requests.session()
        self.cookies = None
    def request(self,url,method,cookies=None,postData=None,headers=None,formats="json",encoding=None,timeout = TIME_OUT,allow_redirects = True):
        print("%s %s => postData:%s",method,url,postData)
        if headers:
            self.session.headers.update(headers)

        #如果有设置则使用设置
        if self.cookies:
            self.session.cookies = self.cookies

        #如果参数中有传入则使用参数的
        if cookies:
            self.session.cookies=cookies

        try:
            if method == Method.GET:
                response = self.session.get(url,timeout= timeout,allow_redirects=allow_redirects)
            else:
                response=self.session.post(url,data=postData,timeout=timeout)

            if response.status_code==200 :
                self.session.close()
                if formats=="response":
                    return response
                if formats=="json":
                    return response.json()
                elif formats=="url":
                    return response.url
                elif formats=='file':
                    return response.content
                else:
                    responseText = ""
                    if encoding:
                        response.encoding = encoding
                        responseText = response.text
                    else:
                        responseText = response.text
                    if formats=="UrlText":
                        return (response.url,responseText)
                    else:
                        return responseText
            elif response.status_code==302:
                return response.headers.get('Location')
            else:
                self.session.close()
                print("网络请求异常 status_code:%s",response.status_code)
                return response
        except Exception as e:
            self.session.close()
            print(e)
            return None
    def download(self,url,dirPath,fileName,headers=None):
        if headers:
            self.session.headers.update(headers)
        try:
            response = self.session.get(url,timeout=TIME_OUT)
            if response.status_code==200:
                if not os.path.exists(dirPath):
                    os.makedirs(dirPath)
                with open(os.path.join(dirPath,fileName),"wb") as code:
                    code.write(response.content)
                response.close()
                return os.path.join(dirPath,fileName)
            else:
                response.close()
                return None
            
        except Exception as e :
            self.session.close()
            return None


    def getCookies(self):
        cookiesDict = {c.name:c.value for c in self.session.cookies}
        return str(cookiesDict)


    #设置cookies
    def setCookies(self,cookies):
        self.cookies = cookies
        pass

if __name__ == "__main__":
    client=HttpClient()
    result = client.request("http://www.baidu.com",Method.GET,formats="text")
    print(result)
    print(client.getCookies())
    #HttpClient().download('http://img.guopan.cn/2017-05-09/1494312126762.png','test','icon.png')
