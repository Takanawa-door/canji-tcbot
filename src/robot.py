# 机器人
from basic import *

class Robot:
    def __init__(self, email: str, password: str, tailchat: Tailchat): 
        """
        机器人父类。
        """
        self.tailchat = tailchat
        self.driver = WEB_DRIVER()
        self.email = email
        self.password = password

    def GoToPage(self, url: str):
        """
        跳转到指定页面。
        """
        self.driver.get(url)

    def SignIn(self):
        """
        登录 Tailchat。
        """
        emailInput = waitUntilElementFound(self.driver, By.NAME, "login-email")
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
