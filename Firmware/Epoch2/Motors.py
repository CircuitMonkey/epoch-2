# Motor control
from adafruit_pca9685 import PCA9685

class Motors():
    def __init__(self, i2c):
        super().__init__()
        self.pca = PCA9685(i2c)
        # pca.frequency = 24  # 24 is lowest. What do motors need for rumble?
        self.pca.frequency = 24

        # Set the PWM duty cycle for channel zero to 50%.
        # duty_cycle is 16 bits to match other PWM objects
        # but the PCA9685 will only actually give 12 bits of resolution.
        # self.pca.channels[0].duty_cycle = 0x7FFF

    # while the PCA9685 takes values up to 12-bits, our range is 0-99
    # so we scale the value such that 99 is close to 12-bit max of 0xFFFF
    def setMotor( self, channel, value ):
        self.pca.channels[channel].duty_cycle = int(value * 0x1AC)   #0x7FFF ~= 50%

    def destroy(self):
        return

