from robot import *
from chatbot import *

# Deafult Behavior: Test Messages.
if __name__ == '__main__':
    color.init(wrap = True)

    tailchat = Tailchat(getenv("tailchatUrl"))
    robot = ChatRobot(getenv("botEmail"), getenv("botPassword"), tailchat)

    try:
        robot.GoToPage(getenv("chatPanelTestPage"))
        robot.InitOnPage()
        robot.TestGetMessages()
    except SystemExit:
        pass
    except:
        traceback.print_exc()

    robot.Quit()