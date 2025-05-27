import displayio
from gui.Page import Page
from gui.Widgets import Slider
from gui.Widgets import Indicator
from gui.Widgets import ImageButton
from gui.Widgets import TextButton

class ManualPage(Page):
    def __init__(self, state, glyphs_img, glyphs_palette, font):
        super().__init__()
        self.state = state
        self.dragChannel = 0
        self.state.pause = True
        self.slider_group = 0 # 0:1..4, 1: 5..8, 2:9..12,  3:12..16

        self.sliders = [
            Slider( 64, 64, glyphs_img, glyphs_palette, 1, font ),
            Slider( 128, 64, glyphs_img, glyphs_palette, 2, font ),
            Slider( 192, 64, glyphs_img, glyphs_palette, 3, font ),
            Slider( 256, 64, glyphs_img, glyphs_palette, 4, font ),
        ]

        for i, e in enumerate(self.sliders):
            e.set_slider_value(state.mode_manual_slider[i])
            self.append(e)

        self.indicator = Indicator( 402, 64, glyphs_img, glyphs_palette, 33, font )
        self.pauseButton = ImageButton(0,416,4,41, glyphs_img, glyphs_palette)
        self.returnButton = ImageButton(416,0,1,6, glyphs_img, glyphs_palette)
        self.append(self.indicator.group)
        self.append(self.pauseButton)
        self.append(self.returnButton)

        # Left/Right Buttons
        self.leftButton = TextButton(0,64,1,"<", glyphs_img, glyphs_palette,font)
        self.rightButton = TextButton(320,64,1,">", glyphs_img, glyphs_palette,font)
        self.append(self.leftButton)
        self.append(self.rightButton)
        self.updateLeftRight()


    def destroy(self):
        for i, e in enumerate(self.sliders):
            e.set_slider_value(state.mode_manual_slider[i])
            self.remove(e)
        self.remove(self.indicator.group)
        self.remove(self.pauseButton)
        self.remove(self.returnButton)


    def updateGUI(self, sensor):
        # print("Update GUI")
        # Update sensor value ==> indicator
        self.indicator.set_value(sensor)

        # Update motor output values. ==> sliders
        return

    def updateMotors(self, motors):
        if self.state.pause:
            for ch in range(16):
                motors.setMotor(ch, 0)
        else:
            for ch in range(16):
                motors.setMotor(ch, self.state.mode_manual_slider[ch])
                #motors.setMotor(self.slider_group*4+ch, self.state.mode_manual_slider[ch]) # 0-99

        return

    def updateLeftRight(self):
                if self.slider_group < 1:
                    self.leftButton.hidden = True
                else:
                    self.leftButton.hidden = False

                if self.slider_group > 3:
                    self.rightButton.hidden = True
                else:
                    self.rightButton.hidden = False

    def togglePause(self):
        self.state.pause = not self.state.pause
        if self.state.pause:
            self.pauseButton.glyph[0] = 41
        else:
            self.pauseButton.glyph[0] = 40
        print(f"Pause Toggled: {str(self.state.pause)}")

    def clearTouch( self ):
        if self.dragChannel > 0:
            print( f"Touch ended on channel: {self.dragChannel}" )
            self.dragChannel = 0

    def handleTouch( self, touch, drag ):
        if drag and self.dragChannel == 0:
            print("Nothing to drag")
            return 1 # nothing to drag
        txO = touch[0]
        tx = touch[0] - self.x
        ty = touch[1]
        print(f"Handle ManualMode Touches => X: {tx}, Y: {ty}")
        # Return index of state.modes[mode] + 2 (because we use 0,1 here)
        if  ty >=0 and ty < 64:
            if tx > self.returnButton.x and tx < self.returnButton.x+64:
                self.state.pause = True
                return 2
        if ty > 416 and ty < 480:
            if tx > self.pauseButton.x and tx < self.pauseButton.x+(4*64):
                self.togglePause()
                return 1 # Handled and now its a drag.
        if ty > self.leftButton.y and ty < self.leftButton.y+64:
            if txO > self.leftButton.x and txO < self.leftButton.x+64:
                print("Touch Left")
                self.slider_group -= 1
                if self.slider_group < 0:
                    self.slider_group = 0
                if self.slider_group > 3:
                    self.slider_group = 3
                for i in range(4):
                    sliderIndex = self.slider_group*4+i
                    self.sliders[i].set_label(sliderIndex + 1)
                    self.sliders[i].set_slider_value(self.state.mode_manual_slider[sliderIndex])

                self.updateLeftRight()

                return 1 # Handled and now its a drag.

        if ty > self.rightButton.y and ty < self.rightButton.y+64:
            if txO > self.rightButton.x and txO < self.rightButton.x+64:
                print("Touch Right")
                self.slider_group += 1
                if self.slider_group < 0:
                    self.slider_group = 0
                if self.slider_group > 3:
                    self.slider_group = 3
                for i in range(4):
                    sliderIndex = self.slider_group*4+i
                    self.sliders[i].set_label(sliderIndex + 1)
                    self.sliders[i].set_slider_value(self.state.mode_manual_slider[sliderIndex])

                self.updateLeftRight()

                return 1 # Handled and now its a drag.


        if (self.dragChannel == 0 or self.dragChannel == 1) and self.sliders[0].handleTouch(touch, drag) > 0:
            self.dragChannel = 1
            stateSlider = self.slider_group * 4 + 0
            self.state.mode_manual_slider[stateSlider] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 2) and self.sliders[1].handleTouch(touch, drag) > 0:
            self.dragChannel = 2
            stateSlider = self.slider_group * 4 + 1
            self.state.mode_manual_slider[stateSlider] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 3) and self.sliders[2].handleTouch(touch, drag) > 0:
            self.dragChannel = 3
            stateSlider = self.slider_group * 4 + 2
            self.state.mode_manual_slider[stateSlider] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 4) and self.sliders[3].handleTouch(touch, drag) > 0:
            self.dragChannel = 4
            stateSlider = self.slider_group * 4 + 3
            self.state.mode_manual_slider[stateSlider] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1

        self.dragChannel = 0 # clear drag
        return 0

