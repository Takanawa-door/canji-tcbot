# 起步指南

欢迎使用 Canji-TCBot，接下来我们将开始配置并运行一个聊天机器人。

本教程中，我们将会让机器人操控已经创建的浏览器窗口，并且让它说话、获取聊天消息。

## 配置环境变量

通常为了方便，我们使用环境变量存储一些必要的信息，方便机器人操作。以下是一个设置环境变量的 Powershell 脚本。

```powershell
# 设置 WebDriver 调试端口
# 该端口用于浏览器调试，请确保该端口未被占用
$env:debugPort=9625
# 你机器人的用户 ID，此处保留，可以不填
$env:botID="..."
```

每次运行机器人之前都在终端运行该脚本，即可设置环境变量。

## 启动浏览器

对于 Microsoft Edge 用户，请使用如下命令行启动 Edge：

```powershell
& "msedge.exe" --remote-debugging-port=$env:debugPort --user-data-dir="<在此处填写浏览器用户文件储存位置>"
```

其中，`--user-data-dir` 参数应该改为你希望储存浏览器用户文件的路径，例如 `F:\MSEdgeDir`，当然，如果你希望使用现有的浏览器用户配置，可以将此参数删除。

运行此代码，浏览器将会启动。其他浏览器设置调试端口的方法请自行查阅相关文档。

## 创建机器人

创建一个新的文件，此处命名为 `demobot.py`，写入以下内容：

```python
from os import getenv
from tcbot import *

# 从环境变量中获取机器人配置
debugPort = getenv("debugPort", "9625")
botID = getenv("botID", "Bot")
robot = ChatRobot()

if __name__ == "__main__":
    # 设置浏览器调试端口
    robot.SetDebugAddress(f"127.0.0.1:{debugPort}")
    # 打开浏览器
    robot.StartDriver()
    input("Press <Enter> if the page is ready.")
    # 让机器人在聊天界面初始化
    robot.InitOnPage()
    # 让机器人发送一条消息
    robot.chatPanel.SendMessage("Hello World!\n")
    # 退出机器人（不会关闭浏览器）
    robot.Quit()
```

运行这段代码，你应该会看到，浏览器窗口被程序识别，然后控制台出现按下回车继续的提示，按下回车后，机器人向聊天窗口发送了一句“Hello World!”。恭喜，你已经成功创建了一个机器人！

---

如果你遇到元素找不到、窗口找不到、元素寻找超时的错误，这可能是由于 Driver 没有找到指定窗口，请你编辑 `demobot.py`，加入以下内容：

```python
def SelectWindow(robot: ChatRobot):
    windowHandles = robot.driver.window_handles
    for handle in windowHandles:
        # 输出窗口标题与下标
        robot.driver.switch_to.window(handle)
        print(f"Window Title: {robot.driver.title}, Index: {windowHandles.index(handle)}")
    print("Please select the window you want to use.")
    windowIndex = int(input("Window Index: "))
    robot.driver.switch_to.window(windowHandles[windowIndex])
```

然后在 `input("Press if the page is ready.")` 的上一行添加：

```python
SelectWindow(robot)
```

再次运行 `demobot.py`，此时程序就会在控制台列出所有可用窗口的索引、标题，根据标题选择合适的窗口，然后填入对应索引即可。以下是一个示例：

```
Window Title: Tailchat Nightly, Index: 0
Window Title: 新建标签页, Index: 1
Window Title: , Index: 2
Window Title: , Index: 3
Please select the window you want to use.
Window Index: 0
```

## 获取信息

在聊天机器人中，我们通常需要获取一些信息，比如聊天记录、用户信息等。`ChatRobot.chatPanel` 提供了一些有关消息面板的操作，此处我们先来了解 `UpdateMessages` 方法。

为了方便，我们将机器人的主要行为操作与机器人初始化、关闭的操作分开，在 `demobot.py` 中：

```python
from tcbot.basic import UserMessage
...

def Main():
    pass

if __name__ == "__main__":
    # 设置浏览器调试端口
    robot.SetDebugAddress(f"127.0.0.1:{debugPort}")
    # 打开浏览器
    robot.StartDriver()
    SelectWindow(robot)
    input("Press <Enter> if the page is ready.")
    # 让机器人在聊天界面初始化
    robot.InitOnPage()
    # 机器人主要逻辑
    Main()
    # 退出机器人（不会关闭浏览器）
    robot.Quit()
```

将 `Main` 函数定义为：

```python
def Main():
    msgs = robot.chatPanel.UpdateMessages()
    for msg in msgs:
        if type(msg) is not UserMessage:
            continue
        print(f"{msg.user.name}(ID 为 {msg.user.id}) 在 {msg.time} 发送了消息：\n{msg.content}\n-----")
```

以下是某个输出样例：

```
Window Title: Tailchat Nightly, Index: 0
Window Title: , Index: 1
Window Title: 新建标签页, Index: 2
Window Title: , Index: 3
Please select the window you want to use.
Window Index: 0
Press <Enter> if the page is ready.
BOT(ID 为 XXX) 在 18:48 发送了消息：
消息呵呵
-----
BOT(ID 为 XXX) 在 18:48 发送了消息：
Canji-TCBot 示例
-----
BOT(ID 为 XXX) 在 18:49 发送了消息：
Developing
```

在这个示例中，我们使用 `UpdateMessages()` 从聊天面板上获取了所有信息，该方法返回一个包含所有聊天信息的列表。随后，我们解析了每一条消息：我们通过 `if` 语句筛选了所有 `UserMessage` 类型的消息，即用户发送的消息，接着，我们在控制台打印了消息的发送者名称与 ID、消息发送时间以及消息内容。这样，我们就成功地获取到了消息。

---

下一节：[消息循环](./MessageLoop.md)