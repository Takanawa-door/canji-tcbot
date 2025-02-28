# 机器人命令

在本节中，我们将学习如何使得机器人读取聊天消息、解析命令并反馈。

## 搭建机器人框架

基于 [消息循环](./MessageLoop.md) 中的示例代码，我们创建并向 `demobot.py` 中写入以下内容：

```python
from os import getenv
from time import sleep
from tcbot import *

# 从环境变量中获取机器人配置
debugPort = getenv("debugPort", "9625")
botID = getenv("botID", "Bot")
robot = ChatRobot()

def HandleMessage(msg: UserMessage):
    pass

def Main(robot: ChatRobot):
    # 先获取所有聊天信息，否则机器人启动前的旧消息也会被识别
    robot.chatPanel.UpdateMessages()

    # 计数器，记录我们处理了多少消息
    msgCnt = 1
    # 当前消息数量，方便我们比较
    originalMsgCnt = len(robot.chatPanel.messages)

    # 一直等待新消息
    while True:
        # 更新消息并获得现在总共的消息数量
        currentMsgCnt = len(robot.chatPanel.UpdateMessages())
        # 如果消息数量增加了，说明有新消息
        if currentMsgCnt <= originalMsgCnt:
            # 每隔两秒抓取一次新消息
            sleep(2)
            continue

        # 获取新消息
        newMsgs = robot.chatPanel.messages[originalMsgCnt:]
        originalMsgCnt = currentMsgCnt

        # 遍历新消息
        for msg in newMsgs:
            # 如果消息是用户消息
            if not isinstance(msg, UserMessage): continue
            msgCnt += 1

            # 处理消息
            HandleMessage(msg)


    robot.chatPanel.UpdateMessages()

def SelectWindow(robot: ChatRobot):
    """
    本函数实现与功能请参阅 [消息循环](./MessageLoop.md)。
    如果不需要，可以直接写 pass。
    """
    ...

if __name__ == "__main__":
    # 设置浏览器调试端口
    robot.SetDebugAddress(f"127.0.0.1:{debugPort}")
    # 打开浏览器
    robot.StartDriver()
    SelectWindow(robot) # 可选的：选择浏览器窗口
    input("Press <Enter> if the page is ready.")
    # 让机器人在聊天界面初始化
    robot.InitOnPage()
    # 机器人主要逻辑
    Main()
    # 退出机器人（不会关闭浏览器）
    robot.Quit()
```

其中消息处理主要逻辑在 `HandleMessage` 函数完成。

当需要退出机器人，按下 `<Ctrl+C>` 即可，当然，你也可以自行实现退出方式。

## 处理用户消息

我们主要处理用户消息，先来看看用户消息类 `UserMessage`。一个 `UserMessage` 实例具有如下成员：

- `content`：一个字符串，用户消息。
  **重要**：当前版本尚不支持解析图片、链接、At 等内容。
- `user`：一个 `UserInformation` 实例，消息发送者。
  - `name`：一个字符串，发送者的名字。
  - `id`：一个字符串，发送者的 ID。该值可能为空。

- `time`：一个字符串，发送时间（格式为 `XX:YY`）。

我们希望机器人只对以正斜杠“/”开头的消息——即表示调用机器人命令的消息——有所回应，并且，我们希望机器人不对自己的消息有所反应，对于单个正斜杠的消息也不予反应，因此我们在 `HandleMessage` 中修改它：

```python
def HandleMessage(msg: UserMessage) -> int:
    if not msg.content.startswith("/") or \
           len(msg.content) <= 1 or \
           msg.user.id == botID: return -3
    return 0
```

## 响应用户命令

我们期望用户的命令调用类 Unix Shell，例如：

```
/echo "A Message"
```

Canji-TCBot 在 `ChatRobot` 类中提供了 `RunCommand` 方法用于解析并执行机器人命令，该函数要求我们传入不带命令前缀的字符串，例如 `echo "A Message"`。我们修改：

```python
def HandleMessage(msg: UserMessage) -> int:
    if not msg.content.startswith("/") or \
           len(msg.content) <= 1 or \
           msg.user.id == botID: return -3
    return robot.RunCommand(msg.content[1:])
```

这样子，当消息接收到时，机器人就会解析该命令了。

另外，`RunCommand` 函数默认不以多线程执行命令，如果希望使用多线程执行，请在调用时将 `runInThreads` 参数设置为 True。

> **注意**　如果函数调用时发生错误，`RunCommand` 不会处理异常！

## 添加用户命令

既然可以执行命令了，那命令从何而来呢？`ChatRobot` 类中提供了 `Command` 装饰器，被该装饰器装饰的函数都会成为机器人可以执行的命令，该装饰器具有如下参数：

- `isPublicToEveryone`（保留）：指定是否对所有人公开可见，默认为 True。

例如，我们添加一个函数 `Foo`：

```python
@robot.Command(True)
def Foo():
    print("'Foo' 函数被调用了！")
```

启动机器人，并使用其它账号对机器人所在面板发送 `/Foo`，终端上就会输出 `'Foo' 函数被调用了！`。当用户消息有参数时，参数也会一一转发给命令函数。

## 向命令传递参数

一般而言，执行命令时，我们希望知道命令的发送者是谁，因此，我们可以在调用 `RunCommand` 方法时加上命令发送者的信息，并在命令中处理它：

```python
# 在 HandleMessage(...) 中：
return robot.RunCommand(msg.content[1:], [msg.user])
```

在以上代码中，我们指定了第二个参数 `frontArgs`，代表用户的命令的参数之前的参数，与之对应的还有 `backArgs`。简单而言，若用户传入的参数为 `userArgs`，当我们调用命令 `Foo` 时，实际上有：

```python
Foo(*frontArgs, *userArgs, *backArgs)
```

而对于所有命令，其第一个参数也都应该用户接受用户信息，例如：

```python
@robot.Command(True)
def Foo(user: UserMessage, *args):
    print(f"用户 {user.user.name} 调用了命令，参数：{args}")
```

这样，我们就设置好了一个命令。