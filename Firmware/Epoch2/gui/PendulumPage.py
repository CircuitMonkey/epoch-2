#   Pendulum Mode for Epoch 2 Vibrator Controller
#   https://github.com/CircuitMonkey/epoch-2
#
#   by Mark J. Koch (@maehem on GitHub) - c2025
#
#   Provided under MIT license.
#
#   This mode activates pairs of vibrators briefly in a
#   pendulum pattern.  The sensation would be that of
#   a plunge and then pull until all motors have been activated.
#   After some delay/dwell, using a slider, the pendulum repeats.
#   The pendulum speed/rate is controlled using a slider.
#


import displayio
from gui.Page import Page
from gui.Widgets import Slider
from gui.Widgets import Indicator
from gui.Widgets import ImageButton

class PendulumPage(Page):
    def __init__(self, state, glyphs_img, glyphs_palette, font):
        super().__init__()
        self.state = state
        self.dragChannel = 0
        self.state.pause = True

        self.tick = 0
        self.tickDir = 1
        self.tickMax = 12
        self.dwell = 0
        self.dwellMult = 0.5
        self.envelope = [ 10, 20,60,99,99,60,20, 10 ]
        self.envLen = len(self.envelope)
        self.tickOffset = [-3,-3,1,1,5,5,9,9]

        self.sliders = [
            Slider( 0, 64, glyphs_img, glyphs_palette, 28, font ),
            Slider( 64, 64, glyphs_img, glyphs_palette, 29, font ),
            Slider( 128, 64, glyphs_img, glyphs_palette, 30, font ),
            Slider( 192, 64, glyphs_img, glyphs_palette, 31, font ),
            Slider( 256, 64, glyphs_img, glyphs_palette, 34, font ),
            Slider( 320, 64, glyphs_img, glyphs_palette, 47, font ),
        ]

        for i, e in enumerate(self.sliders):
            e.set_slider_value(state.mode_pendulum_slider[i])
            self.append(e)

        # Epoch Button
        self.epochButton = ImageButton(416,352,1,1,48, glyphs_img, glyphs_palette, canToggle=True)
        self.append(self.epochButton)

        # Hammer Button
        self.hammerButton = ImageButton(416,416,1,1,42, glyphs_img, glyphs_palette, canToggle=True)
        self.append(self.hammerButton)

        self.indicator = Indicator( 402, 64, glyphs_img, glyphs_palette, 33, font )
        self.pauseButton = ImageButton(0,352,2,2,41, glyphs_img, glyphs_palette)
        self.returnButton = ImageButton(416,0,1,1,6, glyphs_img, glyphs_palette)
        self.append(self.indicator.group)
        self.append(self.pauseButton)
        self.append(self.returnButton)

        self.indicator.set_value(0)

        # Modes
        self.cycleButton = ImageButton(128,384,1,1,36, glyphs_img, glyphs_palette, canToggle=True)
        self.pendulumButton = ImageButton(192,384,1,1,37, glyphs_img, glyphs_palette, canToggle=True)
        self.plungeButton = ImageButton(256,384,1,1,38, glyphs_img, glyphs_palette, canToggle=True)
        self.pullButton = ImageButton(320,384,1,1,39, glyphs_img, glyphs_palette, canToggle=True)
        self.append(self.cycleButton)
        self.append(self.pendulumButton)
        self.append(self.plungeButton)
        self.append(self.pullButton)

        self.cycleButton.setToggled(True)
        # TODO: Set the mode settings.



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
            if self.dwell > 0:
                self.dwell -= 1
            else:
                self.tick += self.sliders[4].value/99.0 * self.tickDir
                self.dwell = 0

        if self.tick > self.tickMax:
            self.tick = self.tickMax
            self.tickDir = -self.tickDir
            self.dwell = self.sliders[5].value * self.dwellMult
        elif self.tick < 0:
            self.tick = 0
            self.tickDir = -self.tickDir
            self.dwell = self.sliders[5].value * self.dwellMult

        for ch in range(8):
            idx = int(self.tick) - self.tickOffset[ch]
            if idx < 0:
                idx += 64

            if idx < self.envLen:
                motVal = self.envelope[idx]
            else:
                motVal = 0

            self.state.mode_pendulum_motors[ch] = motVal

        for sld in range(4):
            mtr = sld*2
            self.state.mode_pendulum_motors[sld*2] = int(self.sliders[sld].value * self.state.mode_pendulum_motors[sld*2] / 99)
            self.state.mode_pendulum_motors[sld*2+1] = int(self.sliders[sld].value * self.state.mode_pendulum_motors[sld*2+1] / 99)

        # todo: Move into loop above
        # Update slider motor indicator based on slider settings and tick.
        self.sliders[0].set_channel_a_value(self.state.mode_pendulum_motors[0])
        self.sliders[0].set_channel_b_value(self.state.mode_pendulum_motors[1])
        self.sliders[1].set_channel_a_value(self.state.mode_pendulum_motors[2])
        self.sliders[1].set_channel_b_value(self.state.mode_pendulum_motors[3])
        self.sliders[2].set_channel_a_value(self.state.mode_pendulum_motors[4])
        self.sliders[2].set_channel_b_value(self.state.mode_pendulum_motors[5])

        # Wand
        self.sliders[3].set_channel_a_value(self.state.mode_pendulum_motors[6])
        self.sliders[3].set_channel_b_value(self.state.mode_pendulum_motors[7])

        return

    def updateMotors(self, motors):
        if self.state.pause:
            for ch in range(16):
                motors.setMotor(ch, 0)
        else:
            for ch in range(16):
                motors.setMotor(ch, self.state.mode_pendulum_motors[ch])

        return

    def togglePause(self):
        self.state.pause = not self.state.pause
        if self.state.pause:
            self.pauseButton.glyph[0] = 41
        else:
            self.pauseButton.glyph[0] = 40
        print(f"Pause Toggled: {str(self.state.pause)}")

    def setModeCycle(self):
            self.cycleButton.setToggled(True)
            self.pendulumButton.setToggled(False)
            self.plungeButton.setToggled(False)
            self.pullButton.setToggled(False)
            # TODO: Set Mode settings.

    def setModePendulum(self):
            self.cycleButton.setToggled(False)
            self.pendulumButton.setToggled(True)
            self.plungeButton.setToggled(False)
            self.pullButton.setToggled(False)
            # TODO: Set Mode settings.

    def setModePlunge(self):
            self.cycleButton.setToggled(False)
            self.pendulumButton.setToggled(False)
            self.plungeButton.setToggled(True)
            self.pullButton.setToggled(False)
            # TODO: Set Mode settings.

    def setModePull(self):
            self.cycleButton.setToggled(False)
            self.pendulumButton.setToggled(False)
            self.plungeButton.setToggled(False)
            self.pullButton.setToggled(True)
            # TODO: Set Mode settings.

    def clearTouch( self ):
        if self.dragChannel > 0:
            print( f"Touch ended on channel: {self.dragChannel}" )
            self.dragChannel = 0

    def handleTouch( self, touch, drag ):
        if drag and self.dragChannel == 0:
            print("Nothing to drag")
            return 1 # nothing to drag
        tx = touch[0] - self.x
        ty = touch[1]
        print(f"Handle ManualMode Touches => X: {tx}, Y: {ty}")
        # Return index of state.modes[mode] + 2 (because we use 0,1 here)
        if self.returnButton.isTouched(tx,ty):
                self.state.pause = True
                return 2
        if self.pauseButton.isTouched(tx,ty):
                self.togglePause()
                return 1 # Handled and now its a drag.
        if self.epochButton.isTouched(tx,ty):
            # print("epoch touched")
            self.epochButton.setToggled(not self.epochButton.isToggled())
            #self.epochButton.hidden = not self.epochButton.hidden
            return 1
        if self.hammerButton.isTouched(tx,ty):
            # print("epoch touched")
            self.hammerButton.setToggled(not self.hammerButton.isToggled())
            #self.hammerButton.hidden = not self.hammerButton.hidden
            return 1
        if self.cycleButton.isTouched(tx,ty):
            if self.cycleButton.isToggled():
                return 1
            self.setModeCycle()
            return 1
        if self.pendulumButton.isTouched(tx,ty):
            if self.pendulumButton.isToggled():
                return 1
            self.setModePendulum()
            return 1
        if self.plungeButton.isTouched(tx,ty):
            if self.plungeButton.isToggled():
                return 1
            self.setModePlunge()
            return 1
        if self.pullButton.isTouched(tx,ty):
            if self.pullButton.isToggled():
                return 1
            self.setModePull()
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 1) and self.sliders[0].handleTouch(touch, drag) > 0:
            self.dragChannel = 1
            self.state.mode_pendulum_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 2) and self.sliders[1].handleTouch(touch, drag) > 0:
            self.dragChannel = 2
            self.state.mode_pendulum_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 3) and self.sliders[2].handleTouch(touch, drag) > 0:
            self.dragChannel = 3
            self.state.mode_pendulum_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 4) and self.sliders[3].handleTouch(touch, drag) > 0:
            self.dragChannel = 4
            self.state.mode_pendulum_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 5) and self.sliders[4].handleTouch(touch, drag) > 0:
            self.dragChannel = 5
            # TODO: there are actually 10 sliders ch 1-4 and ch5-8 and then delay and speed.
            self.state.mode_pendulum_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1
        if (self.dragChannel == 0 or self.dragChannel == 6) and self.sliders[5].handleTouch(touch, drag) > 0:
            self.dragChannel = 6
            self.state.mode_pendulum_slider[self.dragChannel-1] = self.sliders[self.dragChannel-1].value
            # print( f"drag slider {self.dragChannel}" )
            return 1

        self.dragChannel = 0 # clear drag
        return 0

