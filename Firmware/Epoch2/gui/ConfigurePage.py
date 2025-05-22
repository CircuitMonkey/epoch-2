from gui.Page import Page
from gui.Widgets import Configurator
from gui.Widgets import ImageButton
from gui.Widgets import TextButton

class ConfigurePage(Page):
    def __init__(self, state, glyphs_img, glyphs_palette, font):
        super().__init__()

        self.configurators = [
            Configurator( 400, 64, 0, state, glyphs_img, glyphs_palette, 33, font ),
            Configurator( 64, 64, 1, state, glyphs_img, glyphs_palette, 28, font ),
            Configurator( 128, 64, 2, state, glyphs_img, glyphs_palette, 29, font ),
            Configurator( 192, 64, 3, state, glyphs_img, glyphs_palette, 30, font ),
            Configurator( 256, 64, 4, state, glyphs_img, glyphs_palette, 31, font )
            # TODO: Four more for ch 5-8
        ]

        for i, e in enumerate(self.configurators):
            self.append(e)

        self.savFavButton = ImageButton(0, 400, 2, 12, glyphs_img, glyphs_palette)
        self.okButton = TextButton(196, 400, 2, "OK", glyphs_img, glyphs_palette, font)
        self.favButton = ImageButton(400, 400, 1, 13, glyphs_img, glyphs_palette)

        self.append(self.savFavButton)
        self.append(self.okButton)
        self.append(self.favButton)

    def destroy():
        for e in enumerate(self.configurators):
            self.remove(e)
        self.remove(self.savFavButton)
        self.remove(self.okButton)
        self.remove(self.favButton)

    def handleTouch(self, touch, drag):
        if drag: return 1 # we don't handle drags, yet
        tx = touch[0] - self.x
        ty = touch[1]
        print(f"Handle Config Touches => X: {tx}, Y: {ty}")
        # Return index of state.modes[mode] + 2 (because we use 0,1 here)
        if self.okButton.isTouched(tx,ty):
            print("OK Pressed")
            return 2 + 0 # Handled and now its a drag.
        if self.savFavButton.isTouched(tx,ty):
            print("Save to Faves Pressed")
            return 2 + 1 # Handled and now its a drag.
        if self.favButton.isTouched(tx,ty):
            print("Select Faves Pressed")
            return 2 + 2 # Handled and now its a drag.

        if self.configurators[1].handleTouch( touch, drag ) > 1:
            # handle settings request ch. 1
            print ("Handle Ch. 1 Settings")
            return 2 + 3
        if self.configurators[2].handleTouch( touch, drag ) > 1:
            # handle settings request ch. 1
            print ("Handle Ch. 2 Settings")
            return 2 + 4
        if self.configurators[3].handleTouch( touch, drag ) > 1:
            # handle settings request ch. 1
            print ("Handle Ch. 3 Settings")
            return 2 + 5
        if self.configurators[4].handleTouch( touch, drag ) > 1:
            # handle settings request ch. 1
            print ("Handle Ch. 4 Settings")
            return 2 + 6
        if self.configurators[0].handleTouch( touch, drag ) > 1:
            # handle settings request ch. 1
            print ("Handle Sensor Settings")
            return 2 + 7

        return 0

