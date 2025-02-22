# 消息循环

> ![IMPORTANT]
> 
> 此页面需要完善。

本页面将会提供一个消息循环示例，机器人将会逐个等待并处理 10 条用户消息，然后退出。

```python
from tcbot import *
from tcbot.basic import UserMessage
from time import sleep
...

def Main(robot: ChatRobot):
    # 先获取所有聊天信息，否则机器人启动前的旧消息也会被识别
    robot.chatPanel.UpdateMessages()

    # 计数器，记录我们处理了多少消息
    msgCnt = 1
    # 当前消息数量，方便我们比较
    originalMsgCnt = len(robot.chatPanel.messages)

    # 一直等待新消息
    while msgCnt <= 10:
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

            # 打印消息
            print(f"{msg.user.name} 在 {msg.time} 说：{msg.content}")


    robot.chatPanel.UpdateMessages()
...
```

在 `Main` 中，我们先获取了一次消息，如果不在函数开头获取一次消息，则在等待新消息时，会一次性获取面板上所有消息，这显然不是我们希望的——获取机器人启动后的消息。接下来的循环体中，机器人每隔 2 秒检查一次新消息，检查到新消息即遍历并打印所有新的来自用户的消息。
