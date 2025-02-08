# Robot.py!
# Robot settings should be in environment variables.
# WARNING: Tailchat 随时可能出现 Break Change，所以这个脚本不一定可以长久工作。（草）

import pdb

import traceback
import colorama as color
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import getenv
from msvcrt import getwch

WEB_DRIVER = webdriver.Edge

def NextStep(msg: str = ""):
    if len(msg) > 0:
        print(f"{color.Back.BLACK}{color.Fore.WHITE}{msg}{color.Style.RESET_ALL}\n", end = "")
    print(">> Wait for a key to continue...")
    res = getwch()
    if res == '\3':
        print("!Ctrl + C Exit")
        exit()
    return res

def waitUntilElementFound(driver, by, value, timeout = 10):
    return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

def findElement(driver, by, value):
    try:
        return driver.find_element(by, value)
    except:
        return None

def highlightElement(driver, element):
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
    def __init__(self, rootPath: str):
        self.rootPath = rootPath

class Message:
    def __init__(self, content: str, userName: str, time: str):
        self.content = content
        self.userName = userName
        self.time = time

class ChatPanel:
    def __init__(self, driver: WEB_DRIVER):
        self.driver = driver

        self.inputBox = waitUntilElementFound(self.driver, By.XPATH, '//*[@id="tailchat-app"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/textarea')
        self.actions = webdriver.ActionChains(self.driver)
        self.contentBoxXPath = '//*[@id="tailchat-app"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]'
        self.contentBox = self.driver.find_element(By.XPATH, self.contentBoxXPath)

    def SendMessage(self, msg: str):
        # Perhaps no problems while sending messages
        self.inputBox.send_keys(msg + '\n')

    def GetMessages(self):
        messages = []
        highlightElement(self.driver, self.contentBox)

        # 草最喜欢重写了
        contentBoxDiv = self.contentBox.find_elements(By.TAG_NAME, "div")
        # for element in contentBoxDiv:
        for i in range(1, len(contentBoxDiv) + 1):
            element = contentBoxDiv[i]
            elementXPath = self.contentBoxXPath + f"/div[{i}]"
            highlightElement(self.driver, element)
            try:
                # 展开到下级 Div
                # 以下过程全是魔法
                # 对照 MAD.PNG

                # Major XPATH
                # Chatbox:
                # //*[@id="tailchat-app"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]
                # //*[@id="tailchat-app"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]
                # (In Chatbox...) For each message:
                # element
                # For TRUE messages: Find the last div
                # MAJOR = element/div[last()]/div[0]
                # For avatar:
                # MAJOR/div[0]/span[0]/img[0]
                # For content:
                # CONTENT = MAJOR/div[1]
                # For Username:
                # CONTENT/div[0]/div[0]
                # For Time:
                # CONTENT/div[0]/div[1]
                # For Message:
                # CONTENT/div[1]  /div[0]/div[0]  /span[0]
                # I hope it works

                majorXPath = elementXPath + '/div[last()]/div[1]'
                major = self.driver.find_element(By.XPATH, majorXPath)

                contentElementXPath = majorXPath + '/div[2]'
                contentElement = self.driver.find_element(By.XPATH, contentElementXPath)

                userNameElementXPath = contentElementXPath + '/div[1]/div[1]'
                #userNameElement = self.driver.find_element(By.XPATH, userNameElementXPath)
                userNameElement = None

                timeElementXPath = contentElementXPath + '/div[1]/div[2]'
                #timeElement = self.driver.find_element(By.XPATH, timeElementXPath)
                timeElement = None

                messageElementXPath = contentElementXPath + '/div[2]/div[1]/div[1]/span[1]'
                messageElementXPath = contentElementXPath + '/div[1]/div/div/span'
                messageElement = self.driver.find_element(By.XPATH, messageElementXPath)

                avatarElementXPath = majorXPath + '/div[1]/span[1]/img[1]'
                #avatarElement = self.driver.find_element(By.XPATH, avatarElementXPath)
                avatarElement = None


                print(f"----------",
                      f"userName: {userNameElementXPath}",
                      f"time: {timeElementXPath}",
                      f"message: {messageElementXPath}",
                      f"",
                      f"userName: {userNameElement}",
                      f"time: {timeElement}",
                      f"message: {messageElement.text}",
                      f"----------",
                      sep='\n')
                NextStep()
            except:
                traceback.print_exc()
                NextStep()
                continue


        return messages

    def GetMessageFromUserName(self, userName: str):
        pass

    def GetLastMessage(self, callBack):
        pass

    def WaitForNewMessage(self, callBack):
        pass

class Robot:
    def __init__(self, email: str, password: str):
        self.tailchat = Tailchat("https://nightly.paw.msgbyte.com")
        self.tailchat.controlPanel = '/main/group/67933ad81c1f93773739da0b/67933ad81c1f93773739da0a'

        self.driver = None
        self.email = email
        self.password = password
        self.chatPanel = None

    def SignIn(self):
        """
        登录 Tailchat。
        """

        emailInput = self.driver.find_element(By.NAME, "login-email")
        passwordInput = self.driver.find_element(By.NAME, "login-password")
        loginButton = self.driver.find_element(By.XPATH, '//*[@id="tailchat-app"]/div/div[1]/div/div[2]/button[1]')
        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        loginButton.click()

    def PassTutorial(self):
        """
        跳过 Tailchat 默认教程。
        """
        # 检查按钮是否存在
        # closeButton = self.driver.find_element(By.CLASS_NAME, "shepherd-button-secondary")
        closeButton = waitUntilElementFound(self.driver, By.CLASS_NAME, "shepherd-button-secondary")
        closeButton.click()

    def InitChatPanel(self):
        self.chatPanel = ChatPanel(self.driver)

    def Run(self):
        self.driver = WEB_DRIVER()
        self.driver.get(self.tailchat.rootPath)

        NextStep("SignIn()")
        self.SignIn()
        NextStep("PassTutorial()")
        self.PassTutorial()
        self.driver.get(JoinPath(self.tailchat.rootPath, self.tailchat.controlPanel))

        # 发送测试信息
        NextStep("InitChatPanel()")
        self.InitChatPanel()
        NextStep("SendMessage()")
        self.chatPanel.SendMessage("人机登录成功。")
        NextStep("GetMessage()")
        self.chatPanel.GetMessages()

        NextStep("结束")
        self.Quit()

    def Quit(self):
        self.driver.quit()

    def TestGetMessages(self):
        self.driver = WEB_DRIVER()
        self.driver.get(getenv("chatPanelTestPage"))
        NextStep("InitChatPanel()")
        self.InitChatPanel()
        NextStep("GetMessages()")
        self.chatPanel.GetMessages()
        NextStep("Done")
        self.Quit()


if __name__ == '__main__':
    color.init(wrap = True)
    robot = Robot(getenv("botEmail"), getenv("botPassword"))
    try:
        robot.TestGetMessages()
    except SystemExit:
        pass
    except:
        traceback.print_exc()

    robot.Quit()