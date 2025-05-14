import displayio

class Page(displayio.Group):
    def __init__(self):
        super().__init__()

    def destroy(self):
        return

    def handleTouch( self, touch, drag ):
        print("Page Touches")

        return 1

    def updateGUI(self):
        return

    def updateMotors(self, motors):
        return

    def clearTouch( self ):
        # print("Touch ended")
        return

