import smbus2
import bme280

port = 1
address = 0x76
bus = smbus2.SMBus(port)
calibration_params = bme280.load_calibration_params(bus, address)

def sample_temp():
    data = bme280.sample(bus, address, calibration_params)
    return data