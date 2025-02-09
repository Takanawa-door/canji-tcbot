# 残疾 Tailchat Bot

> 你若三东来，换我一城雪白，想吃广东菜，轻轻摇曳在天边的精彩，化作眼泪哭着醒来

这是一个正在进行的、基于模拟用户网页操作的 Tailchat 机器人。目前只会发送文本信息。

## 依赖

- Selenium
- *Edge Driver: 对于复现，请将 Driver 修改为本地 Driver。在 `robot.py` 的第 17 行修改 `WEB_DRIVER` 的值。

## 启动

克隆以后，在项目根目录下新建一个脚本文件，以下以 Powershell 为例。由于 robot.py 需要环境变量获取到账户密码，所以：

```powershell
$env:botEmail = "..."
$env:botPassword = "..."
$env:chatPanelTestPage = "file://项目根目录/mhtml/ChatPanelDemon.mhtml"

python robot.py
```

由于目前仍然在测试获取消息功能，所以在 robot.py 末尾中，大约第 252 行，将代码从 `robot.TestGetMessages()` 修改为

```python
robot.Run()
```

才会真正与 Tailchat 交互。默认与 `mhtml/ChatPanelDemo.mhtml` 进行信息获取测试交互，该功能正在完善。