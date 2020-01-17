
#coding=utf-8


# 淘宝评价+截图

# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#定义一个taobao类
class taobao_infos:

    #对象初始化
    def __init__(self):
        url = 'https://login.taobao.com/member/login.jhtml'
        self.url = url

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-automation']) # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium

        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.wait = WebDriverWait(self.browser, 10) #超时时长为10s



    #登录淘宝
    def login(self):

        # 打开网页
        self.browser.get(self.url)
        self.browser.maximize_window()


        # # 淘宝账号登录
        # self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_QRCodeLogin > div.login-links > a.forget-pwd.J_Quick2Static'))).click()

        # self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TPL_username_1'))).send_keys(weibo_username)

        # self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#TPL_password_1'))).send_keys(weibo_password)


        # 等待 密码登录选项 出现
        password_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.qrcode-login > .login-links > .forget-pwd')))
        password_login.click()

        # 等待 微博登录选项 出现
        weibo_login = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.weibo-login')))
        weibo_login.click()

        # 等待 微博账号 出现
        weibo_user = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.username > .W_input')))
        weibo_user.send_keys(weibo_username)

        # 等待 微博密码 出现
        weibo_pwd = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.password > .W_input')))
        weibo_pwd.send_keys(weibo_password)

        # 等待 登录按钮 出现
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.btn_tip > a > span')))
        submit.click()

        # # 直到获取到淘宝会员昵称才能确定是登录成功
        # taobao_name = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.site-nav-bd > ul.site-nav-bd-l > li#J_SiteNavLogin > div.site-nav-menu-hd > div.site-nav-user > a.site-nav-login-info-nick ')))
        # # 输出淘宝昵称
        # print(taobao_name.text)

        # 我的淘宝
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#J_SiteNavMytaobao > div.site-nav-menu-hd > a'))).click()


        # 我的订单
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#bought'))).click()

        # 搜索订单号
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tp-bought-root > form > div.search-mod__simple-part___3YVUs > input'))).send_keys('794361859382636535')
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#tp-bought-root > form > div.search-mod__simple-part___3YVUs > button.search-mod__order-search-button___1q3E0'))).click()


        # 评价
        # self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#rateOrder'))).click()


        # # 确认收货
        # self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#confirmGood'))).click()

        # time.sleep(10)
        # # 将处理对象变为新标签页面，否则浏览器操作对象会找不到要操作页面中的元素
        # self.browser.switch_to.window(self.browser.window_handles[-1])
        # time.sleep(10)
        # self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#payPassword_container > div > span'))).send_keys('5')




#confirmGood
#confirmGood


# 820526210611636535

        


if __name__ == "__main__":
    
    # 浏览器驱动
    chromedriver_path = "D:/chrome/chromedriver.exe"

    weibo_username = "17600296522" #改成你的微博账号
    weibo_password = "hj05220623." #改成你的微博密码

    a = taobao_infos()
    a.login() #登录





