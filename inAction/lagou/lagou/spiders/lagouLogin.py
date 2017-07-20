import scrapy
from faker import Factory
import urllib.parse
f=Factory.create()
class lagouLogin(scrapy.Spider):
    name="lagouLogin"
    allowed_domains=['lagou.com','passport.lagou.com']
    start_urls=['https://www.lagou.com/']
    headers={
        'Accept':"text/html,application/xhtml+x…lication/xml;q=0.9,*/*;q=0.8",
        'Accept - Language':"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
        'Accept - Encoding':"gzip, deflate, br",
        'Connection':"keep-alive",
        'Host':'passport.lagou.com',
        'User-Agent':f.user_agent()
    }
    formdata={
        'username':'您的账号',
        'password':'您的密码',
        'login':'登录',
        'redir':'https://www.lagou.com/',
        'source':'None'
    }
    def start_requests(self):
        return scrapy.Request(url='https://passport.lagou.com/login/login.html',
                              headers=self.headers,
                              meta={'cookiejar':1},
                              callback=self.parse_login)

    def parse_login(self,response):
        #如果有验证码要人为处理
         if 'captcha_image' in response.body:
             print('Copy the link:')