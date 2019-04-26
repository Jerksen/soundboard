import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import time

class OledMgr(object):
    FONT = "FreeMonoBold.ttf"
    SIZE = 12

    def __init__(self):
        self.rst = 23
        self.ssd = Adafruit_SSD1306.SSD1306_128_64(self.rst, i2c_address=0x3D)

        self.font = ImageFont.truetype(self.FONT, self.SIZE)
        
        self.image = Image.new('1', (self.ssd.width, self.ssd.height))
        self.draw = ImageDraw.Draw(self.image)

        self.top = -2
        self.draw.text((0, self.top), "test message", font=self.font, fill=255)
    
    def init(self):
        self.ssd.begin()
        self.ssd.clear()
        self.ssd.display()

    def write_screen(self, strs):
        """
        strs needs to be a 1 x 6 list
        """
        # clear the display
        self.draw.rectangle((0,0,self.ssd.width, self.ssd.height), outline=0, fill=0)

        # prep the image
        for i, r in enumerate(strs):
            c = "{}: {}".format(i, r)
            self.draw.text((0, self.top+i*10), c, font=self.font, fill=255)

        # draw the image
        self.ssd.image(self.image)
        self.ssd.display()

if __name__ == "__main__":
    o = OledMgr()
    strs = ["ZeldaChest", "Seinfeld", "Bowser", "Ohyea", "Huh", "Goober"]
    o.write_screen(strs)
