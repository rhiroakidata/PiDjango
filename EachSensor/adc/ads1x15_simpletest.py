import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)

# Create single-ended input on channel 0
chan = AnalogIn(ads, ADS.P0)

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

while True:
    if chan.value > 15000:
        print("Ambiente escuro")
        print("Valor: {:5d}\tVoltagem: {:5.3f}".format(chan.value, chan.voltage))

    elif chan.value < 15000 and chan.value >= 10000:
        print("Ambiente pouco iluminado")
        print("Valor: {:5d}\tVoltagem: {:5.3f}".format(chan.value, chan.voltage))

    else:
        print("Ambiente muito iluminado")
        print("Valor: {:5d}\tVoltagem: {:5.3f}".format(chan.value, chan.voltage))

    time.sleep(0.5)
