from gui.Page import Page
from gui.Widgets import ImageButton

class LoadFromFavesPage(Page):
    def __init__(self, state, glyphs_img, glyphs_palette, font):
        super().__init__()
        self.x = 0
        self.backButton = ImageButton(416,0,1,6, glyphs_img, glyphs_palette)

        self.append(self.backButton)

    def destroy():
        self.remove(self.backButton)

    def handleTouch( self, touch, drag ):
        if drag > 0: return 1 # we don't handle drags
        tx = touch[0] - self.x
        ty = touch[1]
        print(f"Handle Load from Faves Touches => X: {tx}, Y: {ty}")
        # Return index of state.modes[mode] + 2 (because we use 0,1 here)
        if  ty >=0 and ty < 64:
            if tx > self.backButton.x and tx < self.backButton.x+64:
                return 2
        return 0

class Save2FavesPage(Page):
    def __init__(self, glyphs_img, glyphs_palette, font):
        super().__init__()
        self.x = 0
        self.backButton = ImageButton(416,0,1,6, glyphs_img, glyphs_palette)

        self.append(self.backButton)

    def destroy():
        self.remove(self.backButton)

    def handleTouch( self, touch, drag ):
        if drag > 0: return 1 # we don't handle drags
        tx = touch[0] - self.x
        ty = touch[1]
        print(f"Handle Save 2 Faves Touches => X: {tx}, Y: {ty}")
        # Return index of state.modes[mode] + 2 (because we use 0,1 here)
        if  ty >=0 and ty < 64:
            if tx > self.backButton.x and tx < self.backButton.x+64:
                return 2
        return 0

