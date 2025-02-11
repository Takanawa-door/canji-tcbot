from .chatbot import *
from shlex import split as SplitAsCommand
from msvcrt import kbhit

helpText = r"""人机帮助：
BotSay(msg): 让入机说话。
Error()：查看报错信息。"""

global robotErrorMessage

robot = None
robotErrorMessage = ""
availableFunctions = {}

robot = ChatRobot(getenv("botEmail"), getenv("botPassword"))
BotCommand = robot.Command

def WriteOutput(user, *args):
    msg = " ".join(args)
    decoded_string = bytes(msg, "utf-8").decode("unicode_escape")
    robot.chatPanel.SendMessage(decoded_string)

@BotCommand
def BotSay(user, *args):
    msg = " ".join(args)
    for i in msg.split("\n"):
        robot.chatPanel.SendMessage(i)

@BotCommand
def Error(user):
    robot.chatPanel.SendMessage(robotErrorMessage)

@BotCommand
def Repeat(user):
    robot.chatPanel.UpdateMessages()
    robot.chatPanel.SendMessage(robot.chatPanel.messages[-2].content)

@BotCommand
def EditTimeout(user, time: float):
    if user in ["ajydwysj?这不是:三元运算符"]:
        robot.chatPanel.SendMessage(f"设置超时时间为 {time} 秒。")
    else:
        robot.chatPanel.SendMessage("你妹石粒")

@BotCommand
def Help(user):
    robot.chatPanel.SendMessage(helpText)

@BotCommand
def Aa654321(user):
    robot.chatPanel.SendMessage("尝试召唤 @Aa\n\n")

@BotCommand
def Fess(user):
    robot.chatPanel.SendMessage("这里没有菜单。")

@BotCommand
def Noob(user):
    robot.chatPanel.SendMessage("你猜。")

@BotCommand
def 道德与法治(user):
    robot.chatPanel.SendMessage("呵呵。[url=https://www.youtube.com/watch?v=bBqHu2yvDe4&list=PLzoSZZQ3vCx9zqz1S_cZMximAsGU5co5H]只是道法罢了[/url]")


def commandAnalize(msg: str, user: str):
    try:
        print(f"{msg} < {user}")
        msg = " ".join(msg.splitlines())
        robot.RunCommand(msg, [user], [], True)
    except:
        err = traceback.format_exc()
        print(f"{user}'s command goes wrong:\n{err}")
        robotErrorMessage = err.splitlines()[-1]
        robot.chatPanel.SendMessage(f"命令 {msg} 解析失败。")

def BotLoop(bot: ChatRobot):
    while True:
        msg = robot.chatPanel.WaitForNewMessage(True)
        if msg == None or type(msg) != UserMessage:
            print(f"Continued with {msg}")
            continue
        print(f"{msg.userName} at {msg.time}: {msg.content}")
        if msg.content == "BotGoAway":
            if msg.userName in ["ajydwysj?这不是:三元运算符"]:
                robot.chatPanel.SendMessage("人机将退出。")
                break
            else:
                robot.chatPanel.SendMessage("拒绝访问:rage:")
        if msg.content.startswith("/"):
            print("Command Analize.")
            threading.Thread(target=commandAnalize, args=[msg.content[1:], msg.userName]).start()
            print("Done")
        if kbhit():
            print("Python commands. (`>q` for quit, `>c` for clear)")
            buf = ""
            while True:
                new = input(">> ")
                if new == ">q":
                    break
                elif new == ">c":
                    buf = ""
                else:
                    buf += new + '\n'
            exec(buf)

def BotBehavior(bot: ChatRobot):
    robot.GoToPage(getenv("tailchatUrl"))
    robot.SignIn()
    robot.PassTutorial()
    robot.GoToPage(getenv("controlPanel"))
    robot.InitOnPage()
    NextStep("Start?")
    print("Start.")
    BotLoop(bot)

if __name__ == "__main__":
    color.init(wrap = True)

    robot.StartDriver()
    try:
        BotBehavior(robot)
    except:
        traceback.print_exc()

    robot.Quit()

    robot.chatPanel.messages = ""
    robot.chatPanel.UpdateMessages()