import displayio
from gui.Page import Page
from gui.Widgets import Slider
from gui.Widgets import Indicator
from gui.Widgets import ImageButton

class ManualPage(Page):
    def __init__(self, glyphs_img, glyphs_palette, font):
        super().__init__()
        self.dragChannel = 0
        self.slider1 = Slider( 0, 64, glyphs_img, glyphs_palette, 42, font )
        self.slider2 = Slider( 64, 64, glyphs_img, glyphs_palette, 43, font )
        self.slider3 = Slider( 128, 64, glyphs_img, glyphs_palette, 44, font )
        self.slider4 = Slider( 196, 64, glyphs_img, glyphs_palette, 45, font )
        self.slider5 = Slider( 256, 64, glyphs_img, glyphs_palette, 34, font )
        self.slider6 = Slider( 320, 64, glyphs_img, glyphs_palette, 47, font )
        self.indicator = Indicator( 402, 64, glyphs_img, glyphs_palette, 33, font )
        self.pauseButton = ImageButton(0,416,4,40, glyphs_img, glyphs_palette)
        self.returnButton = ImageButton(416,0,1,6, glyphs_img, glyphs_palette)
        self.append(self.slider1)
        self.append(self.slider2)
        self.append(self.slider3)
        self.append(self.slider4)
        self.append(self.slider5)
        self.append(self.slider6)
        self.append(self.indicator.group)
        self.append(self.pauseButton)
        self.append(self.returnButton)

    def destroy():
        self.remove(self.slider1)
        self.remove(self.slider2)
        self.remove(self.slider3)
        self.remove(self.slider4)
        self.remove(self.slider5)
        self.remove(self.slider6)
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
        if (self.dragChannel == 0 or self.dragChannel == 1) and self.slider1.handleTouch(touch, drag) > 0:
            self.dragChannel = 1
            print( "drag slider 1" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 2) and self.slider2.handleTouch(touch, drag) > 0:
            self.dragChannel = 2
            print( "drag slider 2" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 3) and self.slider3.handleTouch(touch, drag) > 0:
            self.dragChannel = 3
            print( "drag slider 3" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 4) and self.slider4.handleTouch(touch, drag) > 0:
            self.dragChannel = 4
            print( "drag slider 4" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 5) and self.slider5.handleTouch(touch, drag) > 0:
            self.dragChannel = 5
            print( "drag slider 5" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 6) and self.slider6.handleTouch(touch, drag) > 0:
            self.dragChannel = 6
            print( "drag slider 6" )
            return 1

        self.dragChannel = 0 # clear drag
        return 0

