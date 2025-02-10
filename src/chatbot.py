from basic import *
from robot import *

class ChatPanel:
    def __init__(self, driver: WEB_DRIVER):
        self.driver = driver

    def InitElements(self):
        """
        初始化面板，获取输入框等元素。
        """
        self.inputBox = waitUntilElementFound(self.driver, By.XPATH, '//*[@id="tailchat-app"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/textarea')
        self.actions = webdriver.ActionChains(self.driver)
        self.contentBoxXPath = '//*[@id="tailchat-app"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]'

    def SendMessage(self, msg: str):
        """
        发送消息，仅限单行。
        """
        self.inputBox.send_keys(msg + '\n')

    def GetMessages(self) -> list:
        """
        获取消息。返回一个列表，具有面板下所有消息。

        [WARNING] 这是一个臃肿不堪的函数，肯定会重构的。

        返回值：list 可能元素类型：
        Message & MemberOperateMessage
        """
        messages = []
        contentBoxDiv = self.driver.find_elements(By.XPATH, f"{self.contentBoxXPath}/div")
        lastMessageSender = ""
        print(f"ContentBoxDiv: {len(contentBoxDiv)}")
        # for element in contentBoxDiv:
        for i in range(1, len(contentBoxDiv) + 1):
            elementXPath = self.contentBoxXPath + f"/div[{i}]"
            try:
                # 展开到下级 Div
                # Major XPATH
                # Chatbox:
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

                NextStep(f"Starting {i}: {elementXPath}")

                # 此往下 3 个 div 并在一起
                majorXPath = elementXPath + '/div[last()]/div[1]'
                major = self.driver.find_element(By.XPATH, majorXPath)

                # 判断是否为系统信息
                # systemMessage 即进入消息元素，找得到（返回值非 None）则是。
                systemMessage = findElement(major, By.CLASS_NAME, "bg-black")

                if systemMessage is not None:
                    # TODO: 完成系统信息处理。
                    Aa654321 = systemMessage.get_attribute("textContent")
                    messages.append(UserMessage(Aa654321, "", ""))
                    continue

                # 声明
                avatarElementXPath = None
                avatarElement = None
                userNameElementXPath = None
                userNameElement = None
                timeElementXPath = None
                timeElement = None
                messageElementXPath = None
                messageElement = None
                currentMessage = UserMessage()

                # 定义曰：带有头像的消息为“头消息（Header）”，不带的为“属消息（NonHeader）”。
                # 要区分头消息与属消息，最简单的方法是判断左侧位置是否有头像 Img。
                # 如果有，则为头消息，否则为属消息。
                leftZoomElementXPath = f"{majorXPath}/div[1]"
                isHeader = True if findElement(self.driver, By.XPATH, leftZoomElementXPath + "/span") else False

                if isHeader:
                    avatarElementXPath = f"{leftZoomElementXPath}/span/img"
                    avatarElement = self.driver.find_element(By.XPATH, avatarElementXPath)
                    avatarSource = avatarElement.get_attribute("src")

                    userNameElementXPath = f"{majorXPath}/div[2]/div/div"
                    timeElementXPath     = f"{majorXPath}/div[2]/div/div[2]"
                    messageElementXPath  = f"{majorXPath}/div[2]/div[2]/div/div/span"

                    userNameElement = self.driver.find_element(By.XPATH, userNameElementXPath)
                    timeElement     = self.driver.find_element(By.XPATH, timeElementXPath)
                    messageElement  = self.driver.find_element(By.XPATH, messageElementXPath)

                    currentMessage.userName = userNameElement.get_attribute("textContent")
                    currentMessage.content = messageElement.get_attribute("textContent")
                    currentMessage.time = timeElement.get_attribute("textContent")
                    lastMessageSender = currentMessage.userName

                else:
                    timeElementXPath = f"{leftZoomElementXPath}/div"
                    messageElementXPath = f"{majorXPath}/div[2]/div/div/div/span"

                    timeElement = self.driver.find_element(By.XPATH, timeElementXPath)
                    messageElement = self.driver.find_element(By.XPATH, messageElementXPath)

                    currentMessage.userName = lastMessageSender
                    currentMessage.content = messageElement.get_attribute("textContent")
                    currentMessage.time = timeElement.get_attribute("textContent")

                print(f"{currentMessage.userName} at {currentMessage.time}: {currentMessage.content}")

                messages.append(currentMessage)
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
        """
        测试获取消息功能。
        """
        NextStep("GetMessages()")
        self.chatPanel.GetMessages()
        NextStep("Done")
        self.Quit()