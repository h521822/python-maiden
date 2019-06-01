# 微薄利抢购
# 完善思路：多线程同时抢购多个商品

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time

# 定义一个微薄利类
class vboly_class:
    # 对象初始化
    def __init__(self):
        login_url = "http://login.vboly.com/web/user/loginForm.htm"
        self.login_url = login_url

        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
        options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
        self.browser = webdriver.Chrome(executable_path=chromedriver_path, options=options)
        self.browser.maximize_window()  # 将浏览器最大化显示
        self.wait = WebDriverWait(self.browser, 10)  # 超时时长为10s

    # 登陆
    def login(self):
        # 打开登陆网页
        self.browser.get(self.login_url)

        # 自适应等待，输入账号
        self.browser.implicitly_wait(30)  # 智能等待，直到网页加载完毕，最长等待时间为30s
        self.browser.find_element_by_id('account').send_keys(vboly_username)

        # 自适应等待，输入密码
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_id('pwdwarp').send_keys(vboly_password)

        # 自适应等待，点击确认登录按钮
        self.browser.implicitly_wait(30)
        self.browser.find_element_by_id('login-but').click()

    def good_buy(self):
        # 打开抢购网页
        self.browser.get(buy_url)

        # 自适应等待，获取状态
        self.browser.implicitly_wait(30)
        while (self.browser.find_element_by_id('bugstate').text != '填写订单号'):
            time.sleep(0.1)
            self.browser.refresh()  # 刷新页面

            # # 自适应等待，点击抢购按钮
            self.browser.implicitly_wait(30)
            self.browser.find_element_by_id('bugstate').click()



if __name__ == '__main__':

    # 抢购地址
    buy_url = "http://ls.vboly.com/web/vblgoods/info/goodsid/348422.htm"

    chromedriver_path = "C:/Users/He/AppData/Local/Google/Chrome/Application/chromedriver.exe"  # 改成你的chromedriver的完整路径地址
    vboly_username = "17600296522"  # 改成你的微薄利账号
    vboly_password = "hj123456"  # 改成你的微薄利密码

    vboly = vboly_class()
    vboly.login()  # 登录
    vboly.good_buy() # 抢购

