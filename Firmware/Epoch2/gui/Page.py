import displayio

class Page(displayio.Group):
    def __init__(self):
        super().__init__()

    def destroy():
        return

    def handleTouch( self, touch, drag ):
        print("Page Touches")

        return 1

    def clearTouch( self ):
        # print("Touch ended")
        return

