from .basic import *
from .robot import *
from shlex import split as SplitAsCommand
from functools import wraps
import threading
import time

class ChatPanel:
    def __init__(self, driver: WEB_DRIVER):
        self.driver = driver
        self.messages = []
        self.inputBoxLock = threading.Lock()

    def InitElements(self):
        """
        初始化面板，获取输入框等元素。
        """

        self.inputBox = waitUntilElementFound(self.driver, By.XPATH, '//*[@id="tailchat-app"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div/div/textarea', 200)
        self.actions = webdriver.ActionChains(self.driver)
        self.contentBoxXPath = '//*[@id="tailchat-app"]/div[1]/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div/div[1]/div[1]'
        self.messages = []
        self.inputBoxLock.acquire()

    def SendMessage(self, msg: str):
        """
        发送消息，仅限单行。
        """

        self.inputBoxLock.acquire()
        lines = msg.splitlines()
        for i in lines:
            self.inputBox.send_keys(i)
            if id(i) != id(lines[-1]):
                self.inputBox.send_keys(Keys.SHIFT, '\n')
        self.inputBox.send_keys(Keys.ENTER)
        self.inputBoxLock.release()

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
            # avatarElementXPath = f"{leftZoomElementXPath}/span/img"
            # avatarElement = self.driver.find_element(By.XPATH, avatarElementXPath)
            # avatarSource = avatarElement.get_attribute("src")

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

    def WaitForNewMessage(self, timeBreak = 0.1, timeLimit = 10) -> list[MessageType]:
        """
        等待新消息，当有新消息时，返回包含新消息的列表。会阻塞当前线程！

        timeBreak: 每次等待时间，单位：秒。
        timeLimit: 等待时间上限，单位：秒。设置为 0 即无限制（不建议）。
                   NOTE: 由于 UpdateMessages() 的原因，实际等待时间可能超出 timeLimit 的值。
        """

        self.UpdateMessages()
        originalMessageCount = self.CountMessages()
        
        startTime = time.time()
        while True:
            curTime = time.time()
            if timeLimit != 0 and curTime - startTime >= timeLimit:
                return None
            self.UpdateMessages()
            if (self.CountMessages() > originalMessageCount):
                return self.messages[originalMessageCount:]

            sleep(timeBreak)

class ChatRobot(Robot):
    """
    聊天机器人。

    启动方法：
    1. 初始化 ChatRobot 实例。
    2. 调用 StartDriver() 方法开启浏览器。
    3. 使用 GoToPage() 方法进入聊天面板。
    4. 调用 InitOnPage() 方法。
    """

    def __init__(self, email, password):
        super().__init__(email, password)
        self.chatPanel = ChatPanel(self.driver)
        self.availableFunctions = {}

    def StartDriver(self):
        """
        启动浏览器。
        """
        super().StartDriver()
        self.chatPanel.driver = self.driver

    def InitOnPage(self):
        """
        初始化 ChatPanel。
        NOTE: 在调用此函数之前，请确保已经初始化 Driver（通过 StartDrvier() 方法），且已经登录并进入聊天页面。
        """
        
        self.chatPanel.InitElements()

    def RunCommand(self, command: str, frontArgs: list = [], backArgs: list = [], runInThreads: bool = False) -> int:
        """
        运行命令。仅有被 @Command 装饰的函数才能被调用。
        传入用户输入的命令，不带有命令前缀符号。

        当执行成功，返回 0。当命令为非法命令，返回 -1。此函数不处理内部异常。

        frontArgs, backArgs: 若输入参数为 iArgs，则实际函数调用为 func(*frontArgs, *iArgs, *backArgs)。
        runInThreads: 是否在子线程中运行。默认为 False。
        """

        struct = SplitAsCommand(command)
        funcName = struct[0]
        args = []
        if len(struct) > 1:
            args = struct[1:]

        if funcName not in self.availableFunctions:
            return -1

        if runInThreads:
            threading.Thread(target=self.availableFunctions[funcName], args= frontArgs + args + backArgs).start()
        else:
            self.availableFunctions[funcName](*frontArgs, *args, *backArgs)

        return 0

    def Command(self, func: callable):
        """
        此装饰器可以将此函数标识为机器人可用函数。
        注意：凡是被该装饰器装饰的函数，第一个参数必须是 userName！
        """

        self.availableFunctions[func.__name__] = func
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper