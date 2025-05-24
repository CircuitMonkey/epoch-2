# Slider
import displayio
from adafruit_display_text.label import Label

class TextButton(displayio.Group):
    def __init__(self, x, y, w, h, text, img, img_palette, font):
        super().__init__()
        self.x = x
        self.y = y

        self.background = displayio.TileGrid(
            img, pixel_shader=img_palette,
            width=w, height=1,
            tile_width=64, tile_height=64
        )
        if w == 1:
            self.background[0] = 1
        else:
            self.background[0] = 2
            if w > 2:
                for i in range(w-2):
                    self.background[i+1] = 3
            self.background[w-1] = 4

        self.number_text = Label(font, text=text, color=0xEEEEEE)
        self.number_text.anchor_point = (0.5, 0.5)
        self.number_text.anchored_position = (w*32, 32)

        self.append(self.background)
        self.append(self.number_text)

    def isTouched( self, tx,ty ):
        if  ty >=self.y and ty < self.y + 64:
            if tx > self.x and tx < self.x+self.background.width*64:
                return True

        return False


class ImageButton(displayio.Group):
    def __init__(self, x, y, w, h, glyph, img, img_palette, canToggle=False):
        super().__init__()
        self.x = x
        self.y = y
        self.background = displayio.TileGrid(
            img, pixel_shader=img_palette,
            width=w, height=h,
            tile_width=64, tile_height=64
        )
        self.canToggle = canToggle

        if w == 1 and h == 1:
            self.background[0] = 1
        elif h == 1:  # single row button
            self.background[0] = 2
            if w > 2:
                for i in range(w-2):
                    self.background[i+1] = 3
            self.background[w-1] = 4
        else: # multi row button ( 2 or more wide )
            self.background[0] = 9
            # Top row of large button
            if w > 2:
                for i in range(w-2):
                    self.background[i+1] = 10
            self.background[w-1] = 11
            '''
            # middle rows of large button
            if w > 2 and h > 2:
                for row in range(1,h-2,1):
                    self.background[row*w] = 16
                    for i in range(w-2):
                        self.background[(row*w)+i+1] = 17
                    self.background[(row*w)+ w] = 18
            '''
            # bottom row of large button
            self.background[w*(h-1)] = 23
            if w > 2:
                for i in range(w-2):
                    self.background[i+1] = 24
            self.background[w*h - 1] = 25

        self.glyph = displayio.TileGrid(
            img, pixel_shader=img_palette,
            width=1, height=1,
            tile_width=64, tile_height=64
        )
        # Glyph for moveable element
        self.glyph[0] = glyph
        self.glyph.x = w*32 - 32
        self.glyph.y = h*32 - 32


        self.append(self.background)
        self.append(self.glyph)
        # always on if can't toggle.
        # shows as not-toggled (off) default when toggle is allowed.
        self.setToggled(not canToggle)

    def isTouched( self, tx,ty ):
        if  ty >=self.y and ty < self.y + 64:
            if tx > self.x and tx < self.x+self.background.width*64:
                return True

        return False

    def setToggled( self, visible ):
        if self.canToggle:
            self.background.hidden = not visible
        else:
            print("WARN: Tried to toggle non-toggleble button.")

    def isToggled(self):
        return not self.background.hidden

class Indicator:
    def __init__(self, gx, gy, img, img_palette, glyph, font):
        self.value = 0
        self.background = displayio.TileGrid(
            img, pixel_shader=img_palette,
            width=1, height=5,
            tile_width=64, tile_height=64
        )
        self.background[0] = glyph
        self.background[1] = 7
        self.background[2] = 14
        self.background[3] = 21
        self.pointer = displayio.TileGrid(
            img, pixel_shader=img_palette,
            width=1, height=1,
            tile_width=64, tile_height=64
        )
        # Glyph for moveable element
        self.pointer[0] = 26
        self.pointer.x = 16
        self.pointer.y = 204


        self.group = displayio.Group()
        self.group.x = gx
        self.group.y = gy

        self.group.append(self.background)
        self.group.append(self.pointer)
        # TODO: Number
        self.number_text = Label(font, text="99", color=0x77EE77)
        self.number_text.anchor_point = (0.5, 0.5)
        self.number_text.anchored_position = (32, 270)
        self.group.append(self.number_text)
        # TODO: Channel Values

    def set_value(self, value):
        self.value = value
        self.pointer.y = 204 - value
        self.number_text.text = str( int(value) )


    def set_location( self, x, y):
        self.group.x = x
        self.group.y = y


class Slider(displayio.Group):

    def __init__(self, gx, gy, img, img_palette, glyph, font):
        super().__init__()
        self.x = gx
        self.y = gy
        # Constants
        self.THUMB_WS = 2 # nudge the thumb up/down by this much at the endpoints.
        self.SLIDER_TOP = int(64 - self.THUMB_WS)
        self.SLIDER_BOTTOM = int(192 + self.THUMB_WS )
        self.SLIDE_RANGE = self.SLIDER_BOTTOM - self.SLIDER_TOP

        self.MOT_TOP = self.SLIDER_TOP - 8
        self.MOT_RANGE = self.SLIDE_RANGE + 16

        self.background = displayio.TileGrid(
            img, pixel_shader=img_palette,
            width=1, height=5,
            tile_width=64, tile_height=64
        )
        self.append(self.background)

        if glyph > 16:
            self.background[0] = glyph
        else: # glyphs less than 16 are a number label
            self.background[0] = 0 # blank
            self.label = Label(font, text=str(glyph), color=0x77EE77)
            self.label.anchor_point = (0.5, 0.5)
            self.label.anchored_position = (32, 32)
            self.append(self.label)

        self.background[1] = 8
        self.background[2] = 15
        self.background[3] = 22
        self.slider = displayio.TileGrid(
            img, pixel_shader=img_palette,
            width=1, height=1,
            tile_width=64, tile_height=64
        )
        # Glyph for moveable element
        self.slider[0] = 27
        self.slider.y = self.SLIDER_BOTTOM

        self.append(self.slider)

        # Number
        self.number_text = Label(font, text="99", color=0x77EE77)
        self.number_text.anchor_point = (0.5, 0.5)
        self.number_text.anchored_position = (32, 270)
        self.append(self.number_text)

        # Channel Values
        self.motA = displayio.TileGrid(
            img, pixel_shader=img_palette,
            width=1, height=1,
            tile_width=64, tile_height=64
        )
        self.motA[0] = 46
        self.motA.x = -12
        self.set_channel_a_value(0)
        self.motA.y = self.MOT_TOP + self.MOT_RANGE
        self.append(self.motA)
        self.motA.hidden = True # hidden by default.

        self.motB = displayio.TileGrid(
            img, pixel_shader=img_palette,
            width=1, height=1,
            tile_width=64, tile_height=64
        )
        self.motB[0] = 46
        self.motB.x = 12
        self.set_channel_b_value(0)
        self.append(self.motB)
        self.motB.hidden = True # hidden by default.

        self.dragStart = 0
        self.sliderStart = 0
        self.set_slider_value(50)

    def showMotIndicators( self, show ):
            self.motA.hidden = not show
            self.motB.hidden = not show

    # If a number label(not glyph) was used, update it's displayed int value
    def set_label( self, intVal ):
        try:
            self.label # throws error if Widget uses Glyph
        except NameError:
            # print("well, it WASN'T defined after all!")
            return # do nothing
        else:
            self.label.text = str(intVal)

    def set_slider_value(self, value):
        # Range check 0-99
        if value < 0:
            value = 0
            print("Clamp to 0")
        if value > 99:
            value = 99
            print("Clamp to 99")

        self.value = int(value)
        print(f"New Value: {self.value}")
        self.slider.y = int(self.SLIDER_TOP + (99-value)/99 * (self.SLIDE_RANGE))
        self.number_text.text = str( int(value) )

    def set_channel_a_value(self, value):
        # Move the dot
        self.motA.y = int(self.MOT_TOP + (99-value)/99 * (self.MOT_RANGE))

    def set_channel_b_value(self, value):
        # Move the dot
        self.motB.y = int(self.MOT_TOP + (99-value)/99 * (self.MOT_RANGE))

    def handleTouch(self, touch, drag):
        tX = touch[0]
        tY = touch[1]
        # if no drag, save start point and begin drag
        if not drag: # new drag
            print( "New Drag")
            sX = self.x
            sY = self.y + self.slider.y - 32
            if tX >= sX and tX < (sX + 64):
                if tY >= sY and tY <= (sY + 64):
                    print( "Slider moving...")
                    self.dragStart = tY # Our start anchor
                    self.sliderStart = self.slider.y
                    return 1 # slide
            return 0
        else: # if drag, note delta
            dY = tY - self.dragStart
            # calc new slider position
            sliderY = self.sliderStart + dY

            newValue = 99 - 99*(sliderY - self.SLIDER_TOP)/self.SLIDE_RANGE
            self.set_slider_value(newValue)

            return 1 # continue dragging

        return 0

class Configurator(displayio.Group):
    def __init__(self, gx, gy, channel, state, img, img_palette, glyph, font):
        super().__init__()
        self.x = gx
        self.y = gy
        self.channel = channel
        self.state = state

        if channel == 0:
            label = str("s")
        else:
            label = str(channel)

        number_text = Label(font, text=label, color=0xEEEEEE)
        number_text.anchor_point = (0.5, 0.5)
        number_text.anchored_position = (32, 32)
        self.append(number_text)

        glyph_grid = displayio.TileGrid(
            img, pixel_shader=img_palette,
            width=1, height=1,
            tile_width=64, tile_height=64
        )
        glyph_grid[0] = glyph
        glyph_grid.y = 64
        self.append(glyph_grid)

        self.checkbox = displayio.TileGrid(
            img, pixel_shader=img_palette,
            width=1, height=1,
            tile_width=64, tile_height=64
        )
        self.checkbox[0] = 5
        self.checkbox.y = 128
        self.append(self.checkbox)

        self.gear = displayio.TileGrid(
            img, pixel_shader=img_palette,
            width=1, height=1,
            tile_width=64, tile_height=64
        )
        self.gear[0] = 20
        self.gear.y = 196
        self.append(self.gear)

        self.checkmark = displayio.TileGrid(
            img, pixel_shader=img_palette,
            width=1, height=1,
            tile_width=64, tile_height=64
        )
        self.checkmark[0] = 19
        self.checkmark.y = 128
        self.checkmark.hidden = not self.state.ch_en[channel]
        self.append(self.checkmark)

    def handleTouch(self, touch, drag):
        if drag > 0: return 1 # we don't handle drags, yet
        # is touch in our box coords?
        tX = touch[0]
        tY = touch[1]
        # Checkbox
        cX = self.x+self.checkbox.x
        cY = self.y + self.checkbox.y
        if tX >= cX and tX < (cX + 64):
            if tY >= cY and tY <= (cY + 64):
                print( "Checkbox pressed")
                self.checkmark.hidden = not self.checkmark.hidden
                self.state.ch_en[self.channel] = not self.checkmark.hidden
                return 0

        gX = self.x+self.gear.x
        gY = self.y + self.gear.y
        if tX >= gX and tX < (gX + 64):
            if tY >= gY and tY <= (gY + 64):
                print( "Gear pressed")
                return 2

        return 0

