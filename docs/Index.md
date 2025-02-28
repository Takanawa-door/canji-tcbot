# 手册目录

这是 Canji-TCBot 的目录。

## 起步

> **NOTE**　如果需要阅读《起步》一节，建议将所有内容按照目录编排顺序阅读一遍。

- [起步指南](./Beginner/Beginner.md)

  简要介绍了配置机器人、发送消息、获取消息的方法。
- [消息循环](./Beginner/MessageLoop.md)

  提供了一个消息循环示例，机器人将会逐个等待并处理 10 条用户消息，然后退出。
- [机器人命令](./Beginner/RobotCommand.md)

  本节中，我们将简要了解如何让机器人一直识别新消息并且解析命令。

## 所有内容

此节根据文件树列出所有内容。

### basic.py

- class `UserInformation`：用户信息类。
- class `UserMessage`：存储用户发送的消息的类。
- class `MessageType`：聚合体，表示所有消息类型。

### robot.py

- class `Robot`

### chatbot.py

- class `ChatPanel`
- class `ChatRobot` 继承自 `Robot`
