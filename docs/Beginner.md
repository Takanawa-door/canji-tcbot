# 起步指南

欢迎使用 Canji-TCBot，接下来我们将开始配置并运行一个聊天机器人。

## 配置环境变量

为了账号安全，通常在环境变量中存储账号密码；除此之外，我们还可以使用环境变量存储聊天页面方便机器人操作。以下是一个设置环境变量的 Powershell 脚本。

```powershell
$env:BotEmail = "xxx"
$env:BotPassword = "xxx"
# 设置登录需要的界面
$env:LoginPage = "https://nightly.paw.msgbyte.com"
# 设置机器人要操控的聊天界面
$env:ChatPage = "https://nightly.paw.msgbyte.com/xxx"
```

每次运行机器人之前都在终端运行该脚本，即可设置环境变量。

## 创建机器人

创建一个新的文件，此处命名为 `demobot.py`，写入以下内容：

```python
from os import getenv
from tcbot.robot import *
from tcbot.chatbot import *

robot = ChatRobot(getenv("BotEmail"), getenv("BotPassword"))

if __name__ == "__main__":
    # 打开浏览器
    robot.StartDriver()
    # 打开登录页面
    robot.GoToPage(getenv("LoginPage"))
    # 登录机器人
    robot.SignIn()
    # （可选）跳过 Tailchat 默认教程
    robot.PassTutorial()
    # 打开聊天页面
    robot.GoToPage(getenv("ChatPage"))
    # 初始化聊天面板
    robot.InitOnPage()
    # 发送消息
    robot.chatPanel.SendMessage("Hello World!")
    input("Press Enter to exit")
    # 退出浏览器与机器人
    robot.Quit()
```

运行这段代码，你应该会看到浏览器打开，并自动登录到 Tailchat，然后发送一条消息，并等待你按下回车键退出。恭喜，你已经成功创建了一个机器人！

## 获取信息

在聊天机器人中，我们通常需要获取一些信息，比如聊天记录、用户信息等。需要注意的是，机器人并不会主动索取信息，你需要自己创建一个循环持续获取并处理消息。以下是一个获取消息的例子：

```python
```