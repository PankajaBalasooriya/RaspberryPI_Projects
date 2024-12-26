import smbus
import time

# MPU6050 Registers
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

# Initialize I2C bus
bus = smbus.SMBus(1)

def read_word(register):
    high = bus.read_byte_data(MPU6050_ADDR, register)
    low = bus.read_byte_data(MPU6050_ADDR, register + 1)
    value = (high << 8) | low
    if value > 32767:  # Convert to signed
        value -= 65536
    return value

def get_accel_gyro():
    accel_x = read_word(ACCEL_XOUT_H)
    accel_y = read_word(ACCEL_XOUT_H + 2)
    accel_z = read_word(ACCEL_XOUT_H + 4)

    gyro_x = read_word(GYRO_XOUT_H)
    gyro_y = read_word(GYRO_XOUT_H + 2)
    gyro_z = read_word(GYRO_XOUT_H + 4)

    return {
        "accel": {"x": accel_x, "y": accel_y, "z": accel_z},
        "gyro": {"x": gyro_x, "y": gyro_y, "z": gyro_z},
    }

# Initialize MPU6050
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

try:
    while True:
        data = get_accel_gyro()
        print(f"Accelerometer: {data['accel']}, Gyroscope: {data['gyro']}")
        time.sleep(0.5)
except KeyboardInterrupt:
    print("Terminated by User")
