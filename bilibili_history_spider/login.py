from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# 登录
def login():
    web = webdriver.Chrome(executable_path="D:/chromedriver/chromedriver_version_102/chromedriver.exe")
    web.get(url="https://passport.bilibili.com/login")
    input("登录成功后再输入任意字符继续")
    return web


# 点击历史记录界面
def get_history_page(web):
    history_button = web.find_element(By.XPATH, "//*[@class='right-entry']/li[6]")
    history_button.click()
    time.sleep(3)
    # 切换至新窗口
    windows = web.window_handles
    web.switch_to.window(windows[1])
    return web


# 下拉滚动条并且返回源码
def get_text(web):
    status = True
    height = web.execute_script("return action=document.body.scrollHeight")
    web.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(0.5)

    while status:
        new_height = web.execute_script("return action=document.body.scrollHeight")
        if new_height > height:
            web.execute_script("window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(0.5)
            height = new_height
        else:
            status = False

    with open(file="history.html", mode="w", encoding="utf-8") as file:
        file.write(web.page_source)
    return web.page_source


def start():
    web_d = login()
    get_history_page(web_d)
    get_text(web_d)
