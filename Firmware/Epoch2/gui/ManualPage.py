import displayio
from gui.Page import Page
from gui.Widgets import Slider
from gui.Widgets import Indicator
from gui.Widgets import ImageButton

class ManualPage(Page):
    def __init__(self, state, glyphs_img, glyphs_palette, font):
        super().__init__()
        self.state = state
        self.dragChannel = 0
        self.sliders = [
            Slider( 0, 64, glyphs_img, glyphs_palette, 28, font ),
            Slider( 64, 64, glyphs_img, glyphs_palette, 29, font ),
            Slider( 128, 64, glyphs_img, glyphs_palette, 30, font ),
            Slider( 196, 64, glyphs_img, glyphs_palette, 31, font ),
            Slider( 256, 64, glyphs_img, glyphs_palette, 34, font ),
            Slider( 320, 64, glyphs_img, glyphs_palette, 47, font ),
        ]

        for i, e in enumerate(self.sliders):
            e.set_slider_value(state.mode_manual_slider[i])
            self.append(e)

        self.indicator = Indicator( 402, 64, glyphs_img, glyphs_palette, 33, font )
        self.pauseButton = ImageButton(0,416,4,40, glyphs_img, glyphs_palette)
        self.returnButton = ImageButton(416,0,1,6, glyphs_img, glyphs_palette)
        self.append(self.indicator.group)
        self.append(self.pauseButton)
        self.append(self.returnButton)

    def destroy():
        self.remove(self.sliders[0])
        self.remove(self.sliders[1])
        self.remove(self.sliders[2])
        self.remove(self.sliders[3])
        self.remove(self.sliders[4])
        self.remove(self.sliders[5])
        self.remove(self.indicator.group)
        self.remove(self.pauseButton)
        self.remove(self.returnButton)


    def clearTouch( self ):
        if self.dragChannel > 0:
            print( f"Touch ended on channel: {self.dragChannel}" )
            self.dragChannel = 0

    def handleTouch( self, touch, drag ):
        if drag > 0 and self.dragChannel == 0:
            print("Nothing to drag")
            return 1 # nothing to drag
        tx = touch[0] - self.x
        ty = touch[1]
        print(f"Handle ManualMode Touches => X: {tx}, Y: {ty}")
        # Return index of state.modes[mode] + 2 (because we use 0,1 here)
        if  ty >=0 and ty < 64:
            if tx > self.returnButton.x and tx < self.returnButton.x+64:
                return 2
        elif ty > 416 and ty < 480:
            if tx > self.pauseButton.x and tx < self.pauseButton.x+(4*64):
                print("Pause Pressed")
                return 1 # Handled and now its a drag.
        if (self.dragChannel == 0 or self.dragChannel == 1) and self.sliders[0].handleTouch(touch, drag) > 0:
            self.dragChannel = 1
            self.state.mode_manual_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 2) and self.sliders[1].handleTouch(touch, drag) > 0:
            self.dragChannel = 2
            self.state.mode_manual_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 3) and self.sliders[2].handleTouch(touch, drag) > 0:
            self.dragChannel = 3
            self.state.mode_manual_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 4) and self.sliders[3].handleTouch(touch, drag) > 0:
            self.dragChannel = 4
            self.state.mode_manual_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 5) and self.sliders[4].handleTouch(touch, drag) > 0:
            self.dragChannel = 5
            # TODO: there are actually 10 sliders ch 1-4 and ch5-8 and then delay and speed.
            self.state.mode_manual_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 6) and self.sliders[5].handleTouch(touch, drag) > 0:
            self.dragChannel = 6
            self.state.mode_manual_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            print( f"drag slider {self.dragChannel}" )
            return 1

        self.dragChannel = 0 # clear drag
        return 0

