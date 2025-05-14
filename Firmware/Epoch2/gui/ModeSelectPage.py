import displayio
from gui.Page import Page
from gui.Widgets import ImageButton

class ModeSelectPage(Page):
    def __init__(self, state, glyphs_img, glyphs_palette):
        super().__init__()
        self.x = 48 # center on screen
        self.manualButton = ImageButton(0,128,1,35, glyphs_img, glyphs_palette)
        self.cycleButton = ImageButton(80,128,1,36, glyphs_img, glyphs_palette)
        self.pendulumButton = ImageButton(160,128,1,37, glyphs_img, glyphs_palette)
        self.plungeButton = ImageButton(240,128,1,38, glyphs_img, glyphs_palette)
        self.pullButton = ImageButton(320,128,1,39, glyphs_img, glyphs_palette)

        self.append(self.manualButton)
        self.append(self.cycleButton)
        self.append(self.pendulumButton)
        self.append(self.plungeButton)
        self.append(self.pullButton)

    def destroy():
        self.remove(self.manualButton)
        self.remove(self.cycleButton)
        self.remove(self.pendulumButton)
        self.remove(self.plungeButton)
        self.remove(self.pullButton)

    def updateMotors(self, motors):
        for ch in range(0,7):
            motors.setMotor(ch, 0)
        return

    def handleTouch( self, touch, drag ):
        if drag > 0: return 1 # we don't handle drags
        tx = touch[0] - self.x
        ty = touch[1]
        print(f"Handle Mode Select Touches => X: {tx}, Y: {ty}")
        # Return index of state.modes[mode] + 2 (because we use 0,1 here)
        if  ty >=128 and ty < 192:
            if tx > self.manualButton.x and tx < self.manualButton.x+64:
                return 2
            elif tx > self.cycleButton.x and tx < self.cycleButton.x+64:
                return 3
            elif tx > self.pendulumButton.x and tx < self.pendulumButton.x+64:
                return 4
            elif tx > self.plungeButton.x and tx < self.plungeButton.x+64:
                return 5
            elif tx > self.pullButton.x and tx < self.pullButton.x+64:
                return 6
        # print("Returning 0")
        return 0

