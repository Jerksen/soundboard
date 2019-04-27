from ext_interfaces import i2c_interface
#import i2c_interface

class Amp(i2c_interface.I2cInterface):
    def __init__(self):
        super().__init__(0x58)
        self.regs = {'setup':    0x01,
                    'attack':   0x02,
                    'release':  0x03,
                    'hold':     0x04,
                    'gain':     0x05,
                    'limiter':  0x06,
                    'agc':      0x07}

    def set_gain(self, gain):
        if -26 > gain > 30:
            return
        
        self.write8('gain', gain, 0x3F)

    def enable_speakers(self, l=True, r=True):
        data = self.i2c.read8('setup')

        if l:
            data |= 0x40
        else:
            data &= (0xFF - 0x40)

        if r:
            data |= 0x80
        else:
            data &= (0xFF - 0x80)

        self.write8('setup', data)
