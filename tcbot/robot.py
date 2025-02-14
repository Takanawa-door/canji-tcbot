# 机器人
from .basic import *
from selenium.webdriver.common.action_chains import ActionChains

class Robot:
    def __init__(self, email: str = "", password: str = "", driverOptions: DRIVER_OPTIONS = DRIVER_OPTIONS(),
                 robotName: str = "Bot"): 
        """
        机器人父类。
        启动浏览器需要用 StartDriver 方法！
        """

        self.driver = None
        self.email = email
        self.password = password
        self.actionChains = ActionChains(self.driver)
        self.driverOptions = driverOptions
        self.robotName = robotName

    def SetDebugAddress(self, debugAddress: str):
        """
        设置调试地址，即浏览器 Driver 使用的端口。
        """

        self.driverOptions.add_experimental_option("debuggerAddress", f"{debugAddress}")

    def StartDriver(self):
        """
        启动浏览器。 
        """
        
        self.driver = WEB_DRIVER(options=self.driverOptions)

    def GoToPage(self, url: str):
        """
        跳转到指定页面。
        """

        self.driver.get(url)

    def SignIn(self):
        """
        登录 Tailchat。
        """

        emailInput = waitUntilElementFound(self.driver, By.NAME, "login-email", 10)
        passwordInput = self.driver.find_element(By.NAME, "login-password")
        loginButton = self.driver.find_element(By.XPATH, '//*[@id="tailchat-app"]/div/div[1]/div/div[2]/button[1]')
        emailInput.send_keys(self.email)
        passwordInput.send_keys(self.password)
        loginButton.click()

    def PassTutorial(self):
        """
        跳过 Tailchat 默认教程。
        """

        closeButton = waitUntilElementFound(self.driver, By.CLASS_NAME, "shepherd-button-secondary")
        closeButton.click()

    def Quit(self):
        """
        结束机器人。
        """

        self.driver.quit()

    def ClickOn(self, element: WebElement):
        """
        左键点击元素。
        """

        element.click()

    def RightClickOn(self, element: WebElement):
        """
        右键点击元素。
        """

        self.actionChains.context_click(element).perform()