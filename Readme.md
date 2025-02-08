# 残疾 Tailchat Bot

> 你若三东来，换我一城雪白，想吃广东菜，轻轻摇曳在天边的精彩，化作眼泪哭着醒来

这是一个正在进行的、基于模拟用户网页操作的 Tailchat 机器人。目前只会发送文本信息。

## 依赖

- Selenium
- *Edge Driver: 对于复现，请将 Driver 修改为本地 Driver。在 `robot.py` 的第 17 行修改 `WEB_DRIVER` 的值。

## 构建

```bash
git clone https://github.com/Takanawa-door/canji-tcbot
python ./robot.py
```