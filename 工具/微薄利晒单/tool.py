
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



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




    #登录淘宝
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
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login-but')))
        submit.click()


        # self.browser.get('http://www.vboly.com/web/buyers/selectMyOrders.htm')
        # self.browser.switch_to.window(self.browser.window_handles[-1])


        # 跳转到我的微薄利
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#topbar > div > div.topbar1200-l > div.t-member-inof-container.topbar1200-l > a')))
        submit.click()

        # 将处理对象变为新标签页面，否则浏览器操作对象会找不到要操作页面中的元素
        self.browser.switch_to.window(self.browser.window_handles[-1])
        
        # 跳转到我的订单
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#wrapper > div > div.m-sidebar > div.m-sidebar-box.mb10 > div:nth-child(1)')))
        submit.click()

        # 跳转到我的订单
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#wrapper > div > div.m-sidebar > div.m-sidebar-box.mb10 > div:nth-child(1) > ul > li:nth-child(1) > a')))
        submit.click()


        # 未晒单评价
        submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#l > li:nth-child(5)')))
        submit.click()



        # submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#maingridgrid > div.l-grid2')))


        # self.browser.switch_to.window(self.browser.window_handles[-1])
        # submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#maingrid|2|r1001|c109')))




        

        # # 将处理对象变为新标签页面，否则浏览器操作对象会找不到要操作页面中的元素
        # self.browser.switch_to.window(self.browser.window_handles[-1])

        # # 点击晒实物
        # submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#maingrid|2|r1003|c109 > div > button:nth-child(2)')))
        # submit.click()

        # 


        # # 点击确认按钮
        # submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'body > div.l-dialog.l-dialog-win > table > tbody > tr:nth-child(2) > td.l-dialog-cc > div > div.l-dialog-buttons > div > div:nth-child(2) > div.l-dialog-btn-inner')))
        # submit.click()
        

        


        





        


        # submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#job_test-wb-parent > td:nth-child(7) > a')))
        # submit.click()

        # submit = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#job_test-wb-vue > td:nth-child(7) > a')))
        # submit.click()

        # self.browser.close()


if __name__ == "__main__":
    # 浏览器驱动
    chromedriver_path = "D:/chrome/chromedriver.exe"

    v_username = "17600296522"
    v_password = "hj123456"

    v = v_infos()
    v.login()
 