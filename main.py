class SmartFoneState:
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    LEFT = "left"

class SmartPhone:
    def __init__(self, callBack = None):
        self.state = SmartFoneState.UP
        self.updateUi = callBack

    def updateState(self, newState):

        if(newState == self.state):
            return

        if(self.state == SmartFoneState.UP and newState == SmartFoneState.RIGHT) or \
            (self.state == SmartFoneState.UP and newState == SmartFoneState.LEFT):
            print(newState)
            self.state = newState
            self.updateUi()
            
        if(self.state == SmartFoneState.RIGHT and newState == SmartFoneState.UP) or \
            (self.state == SmartFoneState.RIGHT and newState == SmartFoneState.DOWN):
            print(newState)
            self.state = newState
            self.updateUi()
            
        if(self.state == SmartFoneState.DOWN and newState == SmartFoneState.RIGHT) or \
            (self.state == SmartFoneState.DOWN and newState == SmartFoneState.LEFT):
            print(newState)
            self.state = newState
            self.updateUi()
            
        if(self.state == SmartFoneState.LEFT and newState == SmartFoneState.UP) or \
            (self.state == SmartFoneState.LEFT and newState == SmartFoneState.DOWN):
            print(newState)
            self.state = newState
            self.updateUi()
            


def myCallBack():
    print("updated state !")

smartphone = SmartPhone(callBack=myCallBack)
smartphone.updateState(SmartFoneState.RIGHT)
smartphone.updateState(SmartFoneState.UP)
smartphone.updateState(SmartFoneState.LEFT)
smartphone.updateState(SmartFoneState.RIGHT)