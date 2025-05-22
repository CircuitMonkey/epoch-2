# Uses some 'displayio' code from AdaFruit Qualia ESP32-S3 examples.
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
"""
    Epoch 2 Vibrator Controller using the Adafruit Qualia ESP32-S3 RGB666
    with the 4.0" square display and GT911 captouch driver

    by Mark J. Koch - c2025

    Provided under MIT license.
"""
import board
import displayio
import busio
import dotclockframebuffer
from framebufferio import FramebufferDisplay
import gt911
import adafruit_imageload
import time
from adafruit_display_shapes.rect import Rect
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text.label import Label
from gui.ManualPage import *
from gui.CyclePage import *
from gui.PendulumPage import *
from gui.ModeSelectPage import ModeSelectPage
from gui.ConfigurePage import ConfigurePage
from gui.ChannelSettingsPage import ChannelSettingsPage
from gui.FavesPage import *
from Motors import *
import framebuffer
import state
import time

# import supervisor
# supervisor.runtime.autoreload = False

def switchPage( st, img, img_palette, fontS, fontL ):
    print (f"Switch to Mode: {st.mode}")
    # see state.modes for list of possible modes
    if ( st.mode == 0 ): # Configure
        pg = ConfigurePage(state, img, img_palette, fontL)
    elif ( st.mode == 1 ):
        pg = ModeSelectPage(state, img, img_palette)
    elif ( st.mode == 2 ):
        pg = ManualPage(state, img, img_palette, fontS)
    elif ( st.mode == 3 ):
        pg = CyclePage(state, img, img_palette, fontS)
    elif ( st.mode == 4 ):
        pg = PendulumPage(state, img, img_palette, fontS)
    # elif ( st.mode == 5 ):
    #     pg = PlungeMode(state, img, img_palette, fontS)
    # elif ( st.mode == 6 ):
    #    pg = PullMode(state, img, img_palette, fontS)
    elif ( st.mode == 20 ):
        pg = ChannelSettingsPage( state, img, img_palette, fontS)
    elif ( st.mode == 30 ):
        pg = Save2FavesPage(state, img, img_palette, fontS)
    elif ( st.mode == 31 ):
        pg = LoadFromFavesPage(state, img, img_palette, fontS)
    else: # 99 Error Page?
        pg = ConfigurePage(state, img, img_palette, fontL)


    # Note: You should call display.refresh() after calling this.
    return pg


displayio.release_displays()

# Initialize the Display
tft_pins = dict(board.TFT_PINS)

board.I2C().deinit()
i2c = busio.I2C(board.SCL, board.SDA, frequency=400_000)
tft_io_expander = dict(board.TFT_IO_EXPANDER)
dotclockframebuffer.ioexpander_send_init_sequence(
    i2c, framebuffer.init_sequence_4x4_480, **tft_io_expander
)

# Vibe motors
motors = Motors(i2c)
# Clear motor state right away if a reset happened.
for ch in range(16):
    motors.setMotor(ch, 0)

fb = dotclockframebuffer.DotClockFramebuffer(**tft_pins, **framebuffer.tft_timings)
display = FramebufferDisplay(fb, auto_refresh=False)
# display.auto_refresh = True

#
# Setup GUI

# State machine 0=configure (see state.py)
group = displayio.Group()
display.root_group = group
state.mode = 0

# Create a Group to hold the UI Root
bg_group = displayio.Group(scale=2)  # Scale the group by 2
group.append(bg_group)

# Splash Screen
splash_img, splash_palette = adafruit_imageload.load("gui/splash-8.png")
splash_grid = displayio.TileGrid(splash_img, pixel_shader=splash_palette)
bg_group.append(splash_grid)
display.refresh()

# Fonts
font = bitmap_font.load_font("/fonts/spleen-32x64.bdf")
sm_font = bitmap_font.load_font("/fonts/spleen-16x32.bdf")

# Screen Title
upper_label = Label(font, text="EPOCH 2", color=0x555555)
upper_label.anchor_point = (0.0, 1.0)
upper_label.anchored_position = (24, 64)
group.append(upper_label)

# Add the TileGrid to the Group
rect = Rect(0, 0, 240, 240, fill=0x222222)
bg_group.append(rect)

# call configure menu
glyphs_img, glyphs_palette = adafruit_imageload.load("gui/glyphs-8.png")

upper_label.text = state.title[state.mode]
page = ConfigurePage(state, glyphs_img, glyphs_palette, font)
group.append(page)

bg_group.remove(splash_grid)
display.refresh()

# GT911 Touch - On 4x4x480 Display
gt = gt911.GT911(i2c)


# Main Loop
drag = False

while True:

    try:
        touches = gt.touches
        if len(touches) < 1:
            #print("No touches")
            drag = False
            page.clearTouch()
        else:
            for touch in touches:
                #x = touch[0]
                #y = touch[1]

                #TODO:  Add try-catch and turn off motors if exception
                tStat = page.handleTouch( touch, drag)
                if ( tStat == 0 ):
                    print("Touch handled.")
                    pass
                elif( tStat == 1): # touch is drag
                    print("Touch is drag")
                    pass
                else: # touch is exit. tStat is code.
                    print(f"Mode returned exit page state. tstat={tStat}")
                    page.updateMotors(motors)

                    # tStat-2 is state.modes[x][ ?, ?, ?, ...] index
                    # which is the actual number for the mode to switch to
                    state.mode = state.modes[state.mode][tStat-2]
                    group.remove(page)
                    display.refresh()
                    upper_label.text = state.title[state.mode]
                    page = switchPage( state, glyphs_img, glyphs_palette, sm_font, font )
                    group.append(page)

                display.refresh()
                drag = True
                time.sleep(0.05)


        if not drag:
            page.updateGUI()

        #start_time = time.monotonic()
        display.refresh()
        #end_time = time.monotonic()
        #elapsed_time = end_time - start_time
        #print("Elapsed time: ", elapsed_time, "seconds")

        page.updateMotors(motors)

    except RuntimeError:
        print("pass")
        pass

