# basic.py
# 存放着一些通用的函数、类型，例如调试句、元素获取句。
import colorama as color
from os import getenv
import traceback
from typing import Union
from msvcrt import getwch
import warnings
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement

# 机器人使用的浏览器要有对应的 Options，根据实际情况而定
from selenium.webdriver.edge.options import Options

# 机器人使用的 WebDriver，根据实际情况而定
WEB_DRIVER = webdriver.Edge
DRIVER_OPTIONS = Options

def NextStep(msg: str = ""):
    """
    调试，按下任意键后继续执行。
    """

    if len(msg) > 0:
        print(f"{color.Back.BLACK}{color.Fore.WHITE}{msg}{color.Style.RESET_ALL}\n", end = "")
    print(">> Wait for a key to continue...")
    
    res = getwch()
    
    if res == '\3':
        print("!Ctrl + C Exit")
        exit()

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

class UserMessage:
    """
    消息。
    """

    def __init__(self, content: str = "", userName: str = "", time: str = ""):
        self.content = content
        self.userName = userName
        self.time = time

class SystemMessage:
    """
    系统消息。
    """

    def __init__(self, time: str = ""):
        self.time = time

MEMBER_JOIN_MESSAGE = "Join"
MEMBER_LEAVE_MESSAGE = "Leave"
MEMBER_KICK_MESSAGE = "Kick"

class MemberOperateMessage(SystemMessage):
    """
    加入消息。
    """

    def __init__(self, userName: str = "", time: str = "", kind: str = "",
                 originalText: str = ""):
        """
        尼玛硬编码。
        kind: "Join" or "Leave" or "Kick" <=>
              MEMBER_JOIN_MESSAGE or MEMBER_LEAVE_MESSAGE or MEMBER_KICK_MESSAGE.
        """
        self.userName = userName
        self.time = time
        self.kind = kind
        self.originalText = originalText

MessageType = Union[UserMessage, SystemMessage, MemberOperateMessage]