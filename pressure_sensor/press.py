Sure! Here’s a cleaned-up version of your code with the necessary corrections and optimizations:

python
Copiar código
import smbus
import time
from datetime import datetime
import os 

HOUR_READINGS = 720 
DAY_READINGS  = 17280 

secBackup  = '/home/tecnico/agsolve/pressure_sensor/sec_backup.txt'
hourBackup = '/home/tecnico/agsolve/pressure_sensor/hour_backup.txt'
dayBackup  = '/home/tecnico/agsolve/pressure_sensor/day_backup.txt'

# Initialize backup files
def initialize_file(filepath):
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        with open(filepath, 'w') as file:
            file.write("Data\tHora\tTemp_atual\tTemp_med\tTemp_min\tTemp_max\tPress_atual\tPress_med\tPress_min\tPress_max\tUmi_atual\tUmi_med\tUmi_min\tUmi_max\n")

initialize_file(secBackup)
initialize_file(hourBackup)
initialize_file(dayBackup)

# Get I2C bus
bus = smbus.SMBus(1)
bus.write_byte(0x76, 0x1E)
time.sleep(0.5)

# Initialize variables
tempC_min = float('inf')
tempC_max = float('-inf')
press_min = float('inf')
press_max = float('-inf')
humi_min = float('inf')
humi_max = float('-inf')

# Accumulators
totalTempSum = totalPressSum = totalHumSum = 0
totalReadingCount = 0

# Output data header
print("Data\tHora\tTemp_atual\tTemp_med\tTemp_min\tTemp_max\tPress_atual\tPress_med\tPress_min\tPress_max\tUmi_atual\tUmi_med\tUmi_min\tUmi_max")

while True:
    try:
        # Read calibration data
        C1 = int.from_bytes(bus.read_i2c_block_data(0x76, 0xA2, 2), 'big')
        C2 = int.from_bytes(bus.read_i2c_block_data(0x76, 0xA4, 2), 'big')
        C3 = int.from_bytes(bus.read_i2c_block_data(0x76, 0xA6, 2), 'big')
        C4 = int.from_bytes(bus.read_i2c_block_data(0x76, 0xA8, 2), 'big')
        C5 = int.from_bytes(bus.read_i2c_block_data(0x76, 0xAA, 2), 'big')
        C6 = int.from_bytes(bus.read_i2c_block_data(0x76, 0xAC, 2), 'big')

        # Pressure conversion
        bus.write_byte(0x76, 0x40)
        time.sleep(0.5)
        D1 = sum(val << (8 * i) for i, val in enumerate(bus.read_i2c_block_data(0x76, 0x00, 3)))

        # Temperature conversion
        bus.write_byte(0x76, 0x50)
        time.sleep(0.5)
        D2 = sum(val << (8 * i) for i, val in enumerate(bus.read_i2c_block_data(0x76, 0x00, 3)))

        # Calculate temperature and pressure
        dT = D2 - C5 * 256
        TEMP = 2000 + dT * C6 / 8388608
        OFF = C2 * 65536 + (C4 * dT) / 128
        SENS = C1 * 32768 + (C3 * dT) / 256
        
        if TEMP > 2000:
            T2 = 7 * (dT * dT) / 137438953472
            OFF2 = ((TEMP - 2000) ** 2) / 16
        else:
            T2 = 3 * (dT * dT) / 8589934592
            OFF2 = 3 * ((TEMP - 2000) ** 2) / 8
            if TEMP < -1500:
                OFF2 += 7 * ((TEMP + 1500) ** 2)
        
        TEMP -= T2
        OFF -= OFF2
        pressure = ((((D1 * SENS) / 2097152) - OFF) / 32768.0) / 100.0
        cTemp = TEMP / 100.0
        
        # Dummy humidity reading
        humidity = 50.0  # Replace with actual humidity reading if available
        
        now = datetime.now()
        date = now.date()
        current_time = f"{now.hour}:{now.minute}:{now.second}"

        # Update min/max values
        tempC_min = min(tempC_min, cTemp)
        tempC_max = max(tempC_max, cTemp)
        press_min = min(press_min, pressure)
        press_max = max(press_max, pressure)
        humi_min = min(humi_min, humidity)
        humi_max = max(humi_max, humidity)

        # Accumulate for averages
        totalTempSum += cTemp
        totalPressSum += pressure
        totalHumSum += humidity
        totalReadingCount += 1

        # Calculate averages
        average_temp = totalTempSum / totalReadingCount
        average_press = totalPressSum / totalReadingCount
        average_humi = totalHumSum / totalReadingCount

        # Output data
        print(f"{date}\t{current_time}\t{cTemp:.2f}°C\t{average_temp:.2f}°C\t{tempC_min:.2f}°C\t{tempC_max:.2f}°C\t{pressure:.2f}mbar\t{average_press:.2f}mbar\t{press_min:.2f}mbar\t{press_max:.2f}mbar\t{humidity:.2f}RH\t{average_humi:.2f}RH\t{humi_min:.2f}RH\t{humi_max:.2f}RH")

        # Write to backup file
        with open(secBackup, 'a') as file:
            file.write(f"{date}\t{current_time}\t{cTemp:.2f}°C\t{average_temp:.2f}°C\t{tempC_min:.2f}°C\t{tempC_max:.2f}°C\t{pressure:.2f}mbar\t{average_press:.2f}mbar\t{press_min:.2f}mbar\t{press_max:.2f}mbar\t{humidity:.2f}RH\t{average_humi:.2f}RH\t{humi_min:.2f}RH\t{humi_max:.2f}RH\n")

        time.sleep(5)
    except Exception as e:
        print(f"An error occurred: {e}")
Key Changes:
Used Python’s file handling for reading and writing.
Improved exception handling for I2C operations.
Removed unnecessary variables and focused on the core logic.
The humidity reading is currently a placeholder. Replace it with actual readings if available.
Let me know if you need any more adjustments!



