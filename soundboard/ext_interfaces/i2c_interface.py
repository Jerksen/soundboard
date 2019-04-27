import smbus

bus = smbus.SMBus(1)

class I2cInterface():
    """this is a low level i2c interface"""
    def __init__(self, address):
        self.address = address
        self.regs = {}

    def add_reg(self, regname, regnum):
        self.regs[regname] = regnum

    def add_regs(self, regs):
        self.regs = regs

    def get_reg(self, reg):
        if type(reg) is str and reg in self.regs:
            return self.regs[reg]
        
        return reg

    def read8(self, reg):
        reg = self.get_reg(reg)
        ret = bus.read_byte_data(self.address, reg)
        return ret

    def write8(self, reg, data, mask=0xFF):
        reg = self.get_reg(reg)
        data &= mask
        bus.write_byte_data(self.address, reg, data)
