from basic import *
from robot import *

class ChatPanel:
    def __init__(self, driver: WEB_DRIVER):
        self.driver = driver

    def InitElements(self):
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

class ChatRobot(Robot):
    """
    聊天机器人。

    启动方法：
    1. 初始化 ChatRobot 实例。
    2. 使用 GoToPage() 方法进入聊天面板。
    3. 调用 InitOnPage() 方法。
    """

    def __init__(self, email, password, tailchat):
        super().__init__(email, password, tailchat)
        self.chatPanel = ChatPanel(self.driver)

    def InitOnPage(self):
        """
        初始化 ChatPanel。
        注意：在调用此函数之前，请确保已经登录并进入聊天页面。
        """
        self.chatPanel.InitElements()

    def Run(self):
        """
        自动化运行机器人。
        """
        NextStep("SignIn()")
        self.SignIn()
        NextStep("PassTutorial()")
        self.PassTutorial()
        self.driver.get(JoinPath(self.tailchat.rootPath, self.tailchat.controlPanel))

        # 发送测试信息
        NextStep("SendMessage()")
        self.chatPanel.SendMessage("人机登录成功。")
        NextStep("GetMessage()")
        self.chatPanel.GetMessages()

        NextStep("结束")
        self.Quit()


    def TestGetMessages(self):
        NextStep("GetMessages()")
        self.chatPanel.GetMessages()
        NextStep("Done")
        self.Quit()