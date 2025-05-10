from gui.Page import Page
from gui.Widgets import Configurator
from gui.Widgets import ImageButton
from gui.Widgets import TextButton

class ConfigurePage(Page):
    def __init__(self, glyphs_img, glyphs_palette, font):
        super().__init__()

        self.conf1 = Configurator( 64, 64, 1, glyphs_img, glyphs_palette, 28, font )
        self.conf2 = Configurator( 128, 64, 2, glyphs_img, glyphs_palette, 29, font )
        self.conf3 = Configurator( 192, 64, 3, glyphs_img, glyphs_palette, 30, font )
        self.conf4 = Configurator( 256, 64, 4, glyphs_img, glyphs_palette, 31, font )
        self.conf5 = Configurator( 400, 64, "s", glyphs_img, glyphs_palette, 33, font )

        self.savFavButton = ImageButton(0, 400, 2, 12, glyphs_img, glyphs_palette)
        self.okButton = TextButton(196, 400, 2, "OK", glyphs_img, glyphs_palette, font)
        self.favButton = ImageButton(400, 400, 1, 13, glyphs_img, glyphs_palette)

        self.append(self.conf1)
        self.append(self.conf2)
        self.append(self.conf3)
        self.append(self.conf4)
        self.append(self.conf5)
        self.append(self.savFavButton)
        self.append(self.okButton)
        self.append(self.favButton)

    def destroy():
        self.remove(self.conf1)
        self.remove(self.conf2)
        self.remove(self.conf3)
        self.remove(self.conf4)
        self.remove(self.conf5)
        self.remove(self.savFavButton)
        self.remove(self.okButton)
        self.remove(self.favButton)

    def handleTouch(self, touch, drag):
        if drag > 0: return 1 # we don't handle drags, yet
        tx = touch[0] - self.x
        ty = touch[1]
        print(f"Handle Config Touches => X: {tx}, Y: {ty}")
        # Return index of state.modes[mode] + 2 (because we use 0,1 here)
        if ty > 416 and ty < 480:
            if tx > self.savFavButton.x and tx < self.savFavButton.x+(2*64):
                print("Save to Faves Pressed")
                return 2 + 1 # Handled and now its a drag.
            if tx > self.okButton.x and tx < self.okButton.x+(2*64):
                print("OK Pressed")
                return 2 + 0 # Handled and now its a drag.
            if tx > self.favButton.x and tx < self.favButton.x+64:
                print("Select Faves Pressed")
                return 2 + 2 # Handled and now its a drag.

        if self.conf1.handleTouch( touch, drag ) > 1:
            # handle settings request ch. 1
            print ("Handle Ch. 1 Settings")
            return 2 + 3
        if self.conf2.handleTouch( touch, drag ) > 1:
            # handle settings request ch. 1
            print ("Handle Ch. 2 Settings")
            return 2 + 4
        if self.conf3.handleTouch( touch, drag ) > 1:
            # handle settings request ch. 1
            print ("Handle Ch. 3 Settings")
            return 2 + 5
        if self.conf4.handleTouch( touch, drag ) > 1:
            # handle settings request ch. 1
            print ("Handle Ch. 4 Settings")
            return 2 + 6
        if self.conf5.handleTouch( touch, drag ) > 1:
            # handle settings request ch. 1
            print ("Handle Ch. 5 Settings")
            return 2 + 7

        return 0

