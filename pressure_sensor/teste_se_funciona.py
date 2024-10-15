import smbus
import time

bus = smbus.SMBus(1)

address = 0x76

try:
    bus.write_byte(address, 0)
    print("Sensor detectado!!")
except IOError:
    print("Sensor não detectado!!")
