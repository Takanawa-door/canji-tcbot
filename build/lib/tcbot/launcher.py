from robot import *
from chatbot import *

# Deafult Behavior: Test Messages.
if __name__ == '__main__':
    color.init(wrap = True)

    robot = ChatRobot(getenv("botEmail"), getenv("botPassword"))
    try:
        pass
    except:
        traceback.print_exc()

    robot.Quit()