import displayio
from gui.Page import Page
from gui.Widgets import ImageButton

class ModeSelectPage(Page):
    def __init__(self, state, glyphs_img, glyphs_palette):
        super().__init__()
        self.x = 48 # center on screen
        self.manualButton = ImageButton(0,128,1,1,35, glyphs_img, glyphs_palette)
        self.cycleButton = ImageButton(80,128,1,1,36, glyphs_img, glyphs_palette)

        self.append(self.manualButton)
        self.append(self.cycleButton)

    def destroy():
        self.remove(self.manualButton)
        self.remove(self.cycleButton)

    def updateMotors(self, motors):
        for ch in range(0,7):
            motors.setMotor(ch, 0)
        return

    def handleTouch( self, touch, drag ):
        if drag: return 1 # we don't handle drags
        tx = touch[0] - self.x
        ty = touch[1]
        print(f"Handle Mode Select Touches => X: {tx}, Y: {ty}")
        # Return index of state.modes[mode] + 2 (because we use 0,1 here)
        if self.manualButton.isTouched(tx,ty):
            return 2
        if self.cycleButton.isTouched(tx,ty):
            return 3

        # print("Returning 0")
        return 0

