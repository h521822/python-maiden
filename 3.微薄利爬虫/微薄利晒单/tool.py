#coding=utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import random
import win32api, win32con  # 安装 pywin32或者pypiwin32


VK_CODE ={'ctrl':0x11, 't':0x54, 'tab':0x09}

# 键盘键按下
def keyDown(keyName):
    win32api.keybd_event(VK_CODE[keyName], 0, 0, 0)
# 键盘键抬起
def keyUp(keyName):
    win32api.keybd_event(VK_CODE[keyName], 0, win32con.KEYEVENTF_KEYUP, 0)

# 封装的按键方法
def simulateKey(firstKey, secondKey):
    keyDown(firstKey)
    keyDown(secondKey)
    keyUp(secondKey)
    keyUp(firstKey)

#定义一个wb类
class v_infos:

    #对象初始化
    def __init__(self):
        url = 'http://login.vboly.com/web/user/loginForm.htm?jump=http%3A%2F%2Fwww.vboly.com%2Fweb%2Findex.htm'
        self.url = url

        options = webdriver.ChromeOptions()
        # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        # 超时时长为10s
        self.wait = WebDriverWait(self.browser, 10)




    #登录账号
    def login(self):

        # 打开网页
        self.browser.get(self.url)
        self.browser.maximize_window()


        # 等待 账号 出现
        v_account = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#account')))
        v_account.send_keys(v_username)

        # 等待 密码 出现
        wb_pwd = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#pwdwarp')))
        wb_pwd.send_keys(v_password)

        # 等待 登录按钮 出现
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login-but'))).click()


        # 跳转到我的微薄利
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#topbar > div > div.topbar1200-l > div.t-member-inof-container.topbar1200-l > a'))).click()

        # 将处理对象变为新标签页面，否则浏览器操作对象会找不到要操作页面中的元素
        self.browser.switch_to.window(self.browser.window_handles[-1])
        
        # 跳转到我的订单
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#wrapper > div > div.m-sidebar > div.m-sidebar-box.mb10 > div:nth-child(1)'))).click()

        # 跳转到我的订单
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#wrapper > div > div.m-sidebar > div.m-sidebar-box.mb10 > div:nth-child(1) > ul > li:nth-child(1) > a'))).click()


        # 未晒单评价
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#l > li:nth-child(5)'))).click()

        simulateKey("ctrl", "t")
        self.browser.get('http://www.baidu.com')


        stop = random.uniform(1, 5)
        time.sleep(stop)
        buttons = self.browser.find_elements_by_css_selector("[type=button]")
        for b in buttons:
            if (b.get_attribute('innerHTML') == '晒实物'):
                b.click()

                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.l-dialog-buttons-inner > div:nth-child(2) > div:nth-child(3)'))).click()

                self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#file_upload'))).click()

                # 需上传图片的路径
                file_path = "D:\\yongzhou.jpg"
                # 执行autoit上传文件
                os.system("D:\\22222211.exe %s" % file_path)  
                break
        
        # 关闭当前窗口
        # self.browser.close()

        # 退出浏览器
        # self.driver.quit()
        


if __name__ == "__main__":
    # 浏览器驱动
    chromedriver_path = "D:/chrome/chromedriver.exe"

    v_username = "17600296522"
    v_password = "hj123456"

    t_username = "17600296522"
    t_password = "hj123456"

    v = v_infos()
    v.login()
 