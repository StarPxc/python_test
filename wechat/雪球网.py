"""
 @Author 浦希成
 @Date 2018/8/13 8:32
 @Description 爬取雪球网https://xueqiu.com/
 
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random

options = webdriver.ChromeOptions()

# 设置中文
options.add_argument('lang=zh_CN.UTF-8')
uaList  = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3298.4 Safari/537.36']

agent = random.choice(uaList)
print(agent)
options.binary_location = r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
# options.binary_location = '/opt/google/chrome/chrome'
# 更换头部
options.add_argument('user-agent="{}"'.format(agent))
# chrome_options = Options()
options.add_argument('window-size=1200x800') #指定浏览器分辨率
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu') #谷歌文档提到需要加上这个属性来规避bug
# chrome_options.add_argument('--hide-scrollbars') #隐藏滚动条, 应对一些特殊页面
# chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
options.add_argument('--no-sandbox')
#options.add_argument('--headless') #浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
# chrome_options.binary_location = r'/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary' #手动指定使用的浏览器位置
#options.binary_location = r'/opt/google/chrome/chrome'

# opener = webdriver.Chrome(r'/usr/local/bin/chromedriver', chrome_options=chrome_options)

driver = webdriver.Chrome(r'E:\chromedriver.exe', chrome_options=options)
wait = WebDriverWait(driver, 10)
driver.set_window_size(1200, 800)
driver.get("https://xueqiu.com/")
#找到登陆按钮并点击
loginButton=wait.until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR,'#app > nav > div > div.nav__rt > div > div > span'
                )
            )
        )
loginButton.click()
#选择验证码登陆
verification_code_login=wait.until(
    EC.element_to_be_clickable(
        (
            By.CSS_SELECTOR,
         '#app > div.modals.dimmer.js-shown > div:nth-child(1) > div.modal.modal__login > div.modal__login__main > div.modal__login__mod > div.modal__login__sign > div.modal__login__control > a:nth-child(1)'
        )
    )
)
verification_code_login.click()
#输入手机号
# wait.until(
#     EC.text_to_be_present_in_element(
#         (By.CSS_SELECTOR,
#          '#app > div.modals.dimmer.js-shown > div:nth-child(1) > div.modal.modal__login > div.modal__login__main > div.modal__login__mod > div.modal__login__sign > div.modal__login__form > div > form > div:nth-child(1) > input[type="text"]'
#          )
#         , '18852897377'
#     )
# )
driver.find_element_by_css_selector('#app > div.modals.dimmer.js-shown > div:nth-child(1) > div.modal.modal__login > div.modal__login__main > div.modal__login__mod > div.modal__login__sign > div.modal__login__form > div > form > div:nth-child(1) > input[type="text"]').send_keys('18852897377')
#发送验证码
send_verification_code=wait.until(
    EC.element_to_be_clickable(
        (
            By.CSS_SELECTOR,
         '#app > div.modals.dimmer.js-shown > div:nth-child(1) > div.modal.modal__login > div.modal__login__main > div.modal__login__mod > div.modal__login__sign > div.modal__login__form > div > form > div:nth-child(1) > span:nth-child(3) > a'
        )
    )
)
send_verification_code.click()

verification_code=input("请输入验证码：")
#输入验证码
driver.find_element_by_css_selector('#app > div.modals.dimmer.js-shown > div:nth-child(1) > div.modal.modal__login > div.modal__login__main > div.modal__login__mod > div.modal__login__sign > div.modal__login__form > div > form > div:nth-child(2) > input[type="text"]').send_keys(verification_code)

#登陆提交
logon_submit=wait.until(
    EC.element_to_be_clickable(
        (
            By.CSS_SELECTOR,
         '#app > div.modals.dimmer.js-shown > div:nth-child(1) > div.modal.modal__login > div.modal__login__main > div.modal__login__btn'
        )
    )
)
logon_submit.click()
print(driver.page_source)