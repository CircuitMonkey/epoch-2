#   Cycle Mode for Epoch 2 Vibrator Controller
#   https://github.com/CircuitMonkey/epoch-2
#
#   by Mark J. Koch (@maehem on GitHub) - c2025
#
#   Provided under MIT license.
#
#   This mode activates each vibrator briefly in a
#   cyclic pattern.  The sensation would be that of
#   a "swirl" going up the left side and then continuing
#   down the right side until all motors have been activated.
#   After some delay, using a slider, the cycle repeats.
#   The cycle speed also has some control using a slider.
#


import displayio
from gui.Page import Page
from gui.Widgets import Slider
from gui.Widgets import Indicator
from gui.Widgets import ImageButton

class CyclePage(Page):
    def __init__(self, state, glyphs_img, glyphs_palette, font):
        super().__init__()
        self.state = state
        self.dragChannel = 0
        self.state.pause = True

        self.tick = 0
        self.tickMax = 20
        self.envelope = [ 60,99,80,25 ]
        self.envLen = len(self.envelope)
        self.tickOffset = [0,18,3,15,5,13,8,10] # negative envelope offset of 8 channels

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

        self.sliders[0].showMotIndicators(True)
        self.sliders[1].showMotIndicators(True)
        self.sliders[2].showMotIndicators(True)
        self.sliders[3].showMotIndicators(True)

        self.indicator = Indicator( 402, 64, glyphs_img, glyphs_palette, 33, font )
        self.pauseButton = ImageButton(0,416,4,41, glyphs_img, glyphs_palette)
        self.returnButton = ImageButton(416,0,1,6, glyphs_img, glyphs_palette)
        self.append(self.indicator.group)
        self.append(self.pauseButton)
        self.append(self.returnButton)

    def destroy(self):
        self.remove(self.sliders[0])
        self.remove(self.sliders[1])
        self.remove(self.sliders[2])
        self.remove(self.sliders[3])
        self.remove(self.sliders[4])
        self.remove(self.sliders[5])
        self.remove(self.indicator.group)
        self.remove(self.pauseButton)
        self.remove(self.returnButton)


    def updateGUI(self):
        # print("Update GUI")
        # Update sensor value ==> indicator

        # Calculate state.motor values
        # Update Tick
        if not self.state.pause:
            self.tick += 1
        if self.tick > self.tickMax:
            self.tick = 0

        for ch in range(8):
            idx = self.tick - self.tickOffset[ch]
            if idx < 0:
                idx += 64

            if idx < self.envLen:
                motVal = self.envelope[idx]
            else:
                motVal = 0

            self.state.mode_cycle_motors[ch] = motVal


        # Update slider motor indicator based on slider settings and tick.
        self.sliders[0].set_channel_a_value(self.state.mode_cycle_motors[0])
        self.sliders[0].set_channel_b_value(self.state.mode_cycle_motors[1])
        self.sliders[1].set_channel_a_value(self.state.mode_cycle_motors[2])
        self.sliders[1].set_channel_b_value(self.state.mode_cycle_motors[3])
        self.sliders[2].set_channel_a_value(self.state.mode_cycle_motors[4])
        self.sliders[2].set_channel_b_value(self.state.mode_cycle_motors[5])

        # Wand
        self.sliders[3].set_channel_a_value(self.state.mode_cycle_motors[6])
        self.sliders[3].set_channel_b_value(self.state.mode_cycle_motors[7])

        return

    def updateMotors(self, motors):
        if self.state.pause:
            for ch in range(16):
                motors.setMotor(ch, 0)
        else:
            for ch in range(16):
                motors.setMotor(ch, self.state.mode_cycle_motors[ch])

        return

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
        if drag > 0 and self.dragChannel == 0:
            print("Nothing to drag")
            return 1 # nothing to drag
        tx = touch[0] - self.x
        ty = touch[1]
        print(f"Handle ManualMode Touches => X: {tx}, Y: {ty}")
        # Return index of state.modes[mode] + 2 (because we use 0,1 here)
        if  ty >=0 and ty < 64:
            if tx > self.returnButton.x and tx < self.returnButton.x+64:
                self.state.pause = True
                return 2
        elif ty > 416 and ty < 480:
            if tx > self.pauseButton.x and tx < self.pauseButton.x+(4*64):
                self.togglePause()
                return 1 # Handled and now its a drag.
        if (self.dragChannel == 0 or self.dragChannel == 1) and self.sliders[0].handleTouch(touch, drag) > 0:
            self.dragChannel = 1
            self.state.mode_cycle_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 2) and self.sliders[1].handleTouch(touch, drag) > 0:
            self.dragChannel = 2
            self.state.mode_cycle_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 3) and self.sliders[2].handleTouch(touch, drag) > 0:
            self.dragChannel = 3
            self.state.mode_cycle_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 4) and self.sliders[3].handleTouch(touch, drag) > 0:
            self.dragChannel = 4
            self.state.mode_cycle_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 5) and self.sliders[4].handleTouch(touch, drag) > 0:
            self.dragChannel = 5
            # TODO: there are actually 10 sliders ch 1-4 and ch5-8 and then delay and speed.
            self.state.mode_cycle_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 6) and self.sliders[5].handleTouch(touch, drag) > 0:
            self.dragChannel = 6
            self.state.mode_cycle_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1

        self.dragChannel = 0 # clear drag
        return 0

