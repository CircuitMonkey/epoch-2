#   Epoch 2 Pressure Sensor
#   https://github.com/CircuitMonkey/epoch-2
#
#   by Mark J. Koch (@maehem on GitHub) - c2025
#
#   Provided under MIT license.
#
#   Uses GPIO Pins A0 and A1 on Qualia ESP32

import digitalio

class Hx710b():
    def __init__(self, clk, dat): # Qualia: A1, A0

        self.sensClk = digitalio.DigitalInOut(clk)
        self.sensDat = digitalio.DigitalInOut(dat)

        # Set the pin directions
        self.sensClk.direction = digitalio.Direction.OUTPUT
        self.sensDat.direction = digitalio.Direction.INPUT

    def read(self):
        reading = 0;

        # Wait for the HX710B to finish the current reading
        while self.sensDat.value:
            pass

        self.sensClk.value = False
        # Read the 24 bits of data
        for i in range(24):
            # digitalWrite(SCK, HIGH);
            # digitalWrite(SCK, LOW);
            self.sensClk.value = True
            self.sensClk.value = False
            reading *= 2 # Shift the value left by 1 bit
            #if (digitalRead(DOUT) == HIGH) {
            if self.sensDat.value:
                reading += 1   # Set the least significant bit if DOUT is HIGH

        # 25th Pulse sets Dat pin back to high
        self.sensClk.value = True
        self.sensClk.value = False


        # Invert the sign bit (24th bit)
        reading ^= 0x800000

        # Normal air pressure, blowing into tube range. 10M - 16M
        if ( reading < 10000000 ):
            reading = 10000000
        if ( reading > 16000000 ):
            reading = 16000000

        reading -= 10000000
        reading *= 0.000017  # 1/6M
        return int(reading)
