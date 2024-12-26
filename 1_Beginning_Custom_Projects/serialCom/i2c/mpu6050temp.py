import smbus
import time

# MPU6050 Registers
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
TEMP_OUT_H = 0x41

# Initialize I2C bus
bus = smbus.SMBus(1)

def read_word(register):
    high = bus.read_byte_data(MPU6050_ADDR, register)
    low = bus.read_byte_data(MPU6050_ADDR, register + 1)
    value = (high << 8) | low
    if value > 32767:  # Convert to signed
        value -= 65536
    return value

def get_temperature():
    raw_temp = read_word(TEMP_OUT_H)
    temp_c = raw_temp / 340.0 + 36.53
    return temp_c

# Initialize MPU6050
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

try:
    while True:
        temperature = get_temperature()
        print(f"Temperature: {temperature:.2f} °C")
        time.sleep(1)
except KeyboardInterrupt:
    print("Terminated by User")
