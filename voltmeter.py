import board
import busio
from adafruit_bus_device.i2c_device import I2CDevice
import struct

""" třída slouží pro čtení napětí z voltmetru pomocí sběrnice I2C """


# nastavení adres I2C sběrnice pro čtení dat z voltmetru

I2C_ADDRESS = 0x40
REGISTER_BUS_VOLTAGE = 0x02

i2c = busio.I2C(board.SCL, board.SDA)
device = I2CDevice(i2c, I2C_ADDRESS)


class Voltmeter:

    # přečrtení napětí
    def read_voltage(self):
        with device:
            device.write(bytes([REGISTER_BUS_VOLTAGE]))
            voltage_data = bytearray(2)
            device.readinto(voltage_data)
            voltage_raw = struct.unpack(">H", voltage_data)[0]
            voltage = voltage_raw * 1.25 / 1000.0
            return voltage

    # výpočet nabití baterie v procnetech podle naměřeného napětí
    def get_battery_percent(self, min=9, max=11.5):
        voltage = self.read_voltage()

        result = 0

        if voltage < min:
            result = 0
        elif voltage > max:
            result = 100
        else:
            result = ((voltage - min) / (max - min)) * (100)
        return result
