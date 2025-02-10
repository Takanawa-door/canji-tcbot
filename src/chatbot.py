from basic import *
from robot import *

class ChatPanel:
    def __init__(self, driver: WEB_DRIVER):
        self.driver = driver
        self.messages = []

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

    def CountMessages(self) -> int:
        """
        获取当前面板消息数量。
        """

        contentBoxDiv = self.driver.find_elements(By.XPATH, f"{self.contentBoxXPath}/div")
        return len(contentBoxDiv)

    def GetMessage(self, msgID: int) -> MessageType:
        """
        获取特定消息。
        msgID：消息 ID，从 1 开始。本质上是 div 的索引。应当小于等于 CountMessages()。
        """

        elementXPath = self.contentBoxXPath + f"/div[{msgID}]"
        # 此往下 3 个 div 并在一起
        majorXPath = elementXPath + '/div[last()]/div[1]'
        major = self.driver.find_element(By.XPATH, majorXPath)

        # 判断是否为系统信息
        # systemMessage 即进入消息元素，找得到（返回值非 None）则是。
        systemMessage = findElement(major, By.CLASS_NAME, "bg-black")

        if systemMessage is not None:
            # TODO: 完成系统信息处理。
            Aa654321 = systemMessage.get_attribute("textContent")
            return MemberOperateMessage("", "", "", Aa654321)

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

        else:
            timeElementXPath = f"{leftZoomElementXPath}/div"
            messageElementXPath = f"{majorXPath}/div[2]/div/div/div/span"

            timeElement = self.driver.find_element(By.XPATH, timeElementXPath)
            messageElement = self.driver.find_element(By.XPATH, messageElementXPath)

            currentMessage.content = messageElement.get_attribute("textContent")
            currentMessage.time = timeElement.get_attribute("textContent")

        return currentMessage

    def UpdateMessages(self, startIndex: int | None = None) -> list:
        """
        刷新消息列表。返回一个列表，具有面板下所有消息。

        返回值：list 可能元素类型：
        Message & MemberOperateMessage
        """

        contentBoxDiv = self.driver.find_elements(By.XPATH, f"{self.contentBoxXPath}/div")
        for i in range(len(self.messages) + 1 if startIndex is None else startIndex,
                       len(contentBoxDiv) + 1):
            try:
                currentMessage = self.GetMessage(i)
                if type(currentMessage) == UserMessage and currentMessage.userName == "":
                    # 查找上一个名字非空的
                    for j in range(len(self.messages) - 1, -1, -1):
                        if type(self.messages[j]) == UserMessage and self.messages[j].userName != "":
                            currentMessage.userName = self.messages[j].userName
                            break

                self.messages.append(currentMessage)
            except:
                traceback.print_exc()
                continue

        return self.messages

    def GetMessageFromUserName(self, userName: str):
        pass

    def GetLastMessage(self, onlyForUser: bool = True) -> MessageType:
        """
        获取最后一条消息。

        onlyForUser: 是否只获取用户消息，即获取最后一条用户消息。默认为 True。
        """

        self.UpdateMessages()
        if not onlyForUser:
            return self.messages[-1]

        for i in range(len(self.messages) - 1, -1, -1):
            if type(self.messages[i]) == UserMessage:
                return self.messages[i]

        return None

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
        self.chatPanel.UpdateMessages()

        NextStep("结束")
        self.Quit()


    def TestGetMessages(self):
        """
        测试获取消息功能。
        """

        NextStep("GetMessages()")
        print(f"Count: {self.chatPanel.CountMessages()}")
        print(f"Get Single Message: {self.chatPanel.GetMessage(1)}")
        self.chatPanel.UpdateMessages()
        print(self.chatPanel.GetLastMessage(True).content)
        NextStep("Done")
        self.Quit()