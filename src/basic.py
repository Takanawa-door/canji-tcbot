# basic.py
# 存放着一些通用的函数、类型，例如调试句、元素获取句。
# 你去到那个 Seesion Chat 里问……
# 建议你写一下：这个不用写，第三方库
import colorama as color
from os import getenv
import traceback
from msvcrt import getwch
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 机器人使用的 WebDriver，根据实际情况而定
WEB_DRIVER = webdriver.Edge

def NextStep(msg: str = ""):
    """
    调试。
    """
    # 如果提供了msg参数，并且msg的长度大于0，打印出msg内容并设置背景颜色为黑色，文字颜色为白色
    if len(msg) > 0:
        print(f"{color.Back.BLACK}{color.Fore.WHITE}{msg}{color.Style.RESET_ALL}\n", end = "")
    # 打印提示信息，提示用户按任意键继续
    print(">> Wait for a key to continue...")
    
    # 调用getwch()函数等待用户输入一个字符
    res = getwch()
    
    # 如果用户输入的是Ctrl + C（即'\3'），则退出程序并打印提示信息
    if res == '\3':
        print("!Ctrl + C Exit")
        exit()
    # 返回用户输入的字符
    return res

def waitUntilElementFound(driver, by, value, timeout = 10):
    """
    等到元素加载才返回。
    """
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def findElement(driver, by, value):
    """
    不抛出异常查找元素。
    """
    try:
        return driver.find_element(by, value)
    except:
        return None

def highlightElement(driver, element):
    """
    高亮特定元素。
    """

    # 获取元素的原始背景颜色
    original_background_color = element.value_of_css_property("background-color")

    # 设置高亮样式
    highlight_style = "border: 2px solid red; outline: 2px solid red;"

    # 应用高亮样式
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, highlight_style)

    sleep(1)

    # 恢复原始背景颜色
    driver.execute_script("arguments[0].setAttribute('style', arguments[1]);", element, original_background_color)

def JoinPath(*args):
    """
    连接路径。
    """

    result = ""
    # 遍历每一项
    isStart = True
    for arg in args:
        if isStart:
            result = arg
            if result[len(result) - 1] == "/":
                result = result[:len(result) - 1]
            isStart = False
            continue
        if arg.startswith("/"):
            arg = arg[1:]
        result += "/" + arg
    return result

class Tailchat:
    """
    Tailchat 信息。
    """
    def __init__(self, rootPath: str):
        self.rootPath = rootPath

class Message:
    """
    消息。
    """
    def __init__(self, content: str, userName: str, time: str):
        self.content = content
        self.userName = userName
        self.time = time