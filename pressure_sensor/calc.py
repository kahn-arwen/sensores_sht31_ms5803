
import smbus
import time
from datetime import datetime
import array, fcntl, struct, termios, os 

HOUR_READINGS = 720 
DAY_READINGS  = 17280 

secBackup  = '/home/tecnico/agsolve/pressure_sensor/sec_backup.txt'
hourBackup = '/home/tecnico/agsolve/pressure_sensor/hour_backup.txt'
dayBackup  = '/home/tecnico/agsolve/pressure_sensor/day_backup.txt'

# open the file in read mode
def initialize_file(filepath):
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        with open(filepath, 'w') as file:
            file.write("Data\t\tHora\t\tTemp_atual\tTemp_med\tTemp_min\tTemp_max\tPress_atual\tPress_med\tPress_min\tPress_max\tUmi_atual\tUmi_med\tUmi_min\tUmi_max\n")

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

tempC_min_hour = float('inf')
tempC_max_hour = float('-inf')
press_min_hour = float('inf')
press_max_hour = float('-inf')
humi_min_hour = float('inf')
humi_max_hour = float('-inf')

# Accumulators
tempSumC_day = 0
pressSum_day = 0
humiditySum_day = 0;

tempSumC_hour = 0
pressSum_hour = 0
humiditySum_hour = 0;

totalTempSum = 0
totalPressSum = 0
totalHumSum = 0;

totalReadingCount = 0
readingCount_hour = 0
readingCount_day = 0
readingCount_delete_file = 0
average_press = float('-inf')
average_temp = float('-inf')
average_humi = float('-inf')


# Output data to screen
print("Data\tHora\tTemp_atual\tTemp_med\tTemp_min\tTemp_max\tPress_atual\tPress_med\tPress_min\tPress_max\tUmi_atual\tUmi_med\tUmi_min\tUmi_max\n")

while True:
    # Read calibration data
    data = bus.read_i2c_block_data(0x76, 0xA2, 2)
    C1 = data[0] * 256 + data[1]
    data = bus.read_i2c_block_data(0x76, 0xA4, 2)
    C2 = data[0] * 256 + data[1]
    data = bus.read_i2c_block_data(0x76, 0xA6, 2)
    C3 = data[0] * 256 + data[1]
    data = bus.read_i2c_block_data(0x76, 0xA8, 2)
    C4 = data[0] * 256 + data[1]
    data = bus.read_i2c_block_data(0x76, 0xAA, 2)
    C5 = data[0] * 256 + data[1]
    data = bus.read_i2c_block_data(0x76, 0xAC, 2)
    C6 = data[0] * 256 + data[1]
	
    # Pressure conversion command
    bus.write_byte(0x76, 0x40)
    time.sleep(0.5)

    # Read digital pressure value
    value = bus.read_i2c_block_data(0x76, 0x00, 3)
    D1 = value[0] * 65536 + value[1] * 256 + value[2]

    # Temperature conversion command
    bus.write_byte(0x76, 0x50)
    time.sleep(0.5)

    # Read digital temperature value
    value = bus.read_i2c_block_data(0x76, 0x00, 3)
    D2 = value[0] * 65536 + value[1] * 256 + value[2]

    dT = D2 - C5 * 256
    TEMP = 2000 + dT * C6 / 8388608
    OFF = C2 * 65536 + (C4 * dT) / 128
    SENS = C1 * 32768 + (C3 * dT) / 256
    T2 = 0
    OFF2 = 0
    SENS2 = 0

    if TEMP > 2000:
        T2 = 7 * (dT * dT) / 137438953472
        OFF2 = ((TEMP - 2000) * (TEMP - 2000)) / 16
    elif TEMP < 2000:
        T2 = 3 * (dT * dT) / 8589934592
        OFF2 = 3 * ((TEMP - 2000) * (TEMP - 2000)) / 8
        SENS2 = 5 * ((TEMP - 2000) * (TEMP - 2000)) / 8
        if TEMP < -1500:
            OFF2 += 7 * ((TEMP + 1500) * (TEMP + 1500))
            SENS2 += 4 * ((TEMP + 1500) * (TEMP + 1500))

    TEMP -= T2
    OFF -= OFF2
    SENS -= SENS2
    pressure = ((((D1 * SENS) / 2097152) - OFF) / 32768.0) / 100.0
    cTemp = TEMP / 100.0
    
    file = int
    buss = "/dev/i2c-1";
    ioctl = (file, I2C_SLAVE, 0x44)

    config[2] = { 0 };
    config[0] = 0x2C;
    config[1] = 0x06;
    write(file, config, 2)
    dados[6] = { 0 }
        
    humidity = (((dados[3] * 256) + dados[4])) * 100.0 / 65535.0;
    

    now = datetime.now()
    date = now.date()
    current_time = f"{now.hour}:{now.minute}:{now.second}"
    
    #max/min temp/umi/press
    if(cTemp > tempC_max):
        tempC_max = cTemp
    if (cTemp < tempC_min):
        tempC_min = cTemp
    if(pressure > press_max):
        press_max = pressure
    if(pressure < press_min):
        press_min = pressure
    if(humidity > humi_max):
        humi_max = humidity
    if(humidity < humi_min):
        humi_min = humidity
    
    # # # # # # # # # # # # #   
    if(cTemp > tempC_max_hour):
        tempC_max_hour = cTemp
    if (cTemp < tempC_min_hour):
        tempC_min_hour = cTemp;
    if(pressure > press_max_hour):
        humi_max_hour = pressure
    if(pressure < press_min_hour):
        umi_min_hour = pressure
    if(humidity > humi_max_hour):
        humi_max_hour = humidity
    if(humidity < humi_min_hour):
        humi_min_hour = humidity
		
    # acumulador p calcular a media
    totalTempSum  += cTemp;
    tempSumC_hour += cTemp;
    tempSumC_day  += cTemp;
    totalPressSum += pressure;
    pressSum_hour += pressure;
    pressSum_day  += pressure;
    totalHumSum    += humidity;
    humidityHum_hour += humidity;
    humidityHum_day  += humidity;
		
    totalReadingCount = totalReadingCount+1
		
    if(totalReadingCount > 0): 
        average_temp = totalTempSum / totalReadingCount  
        average_press = totalPressSum / totalReadingCount
        average_humi =totalTempHum / totalReadingCount
   
    print(f"{date}\t{current_time}\t{cTemp:.2f}°C\t\t{average_temp:.2f}°C\t\t{tempC_min:.2f}°C\t\t{tempC_max:.2f}°C\t\t{pressure:.2f}mbar\t{average_press:.2f}mbar\t{press_min:.2f}mbar\t{press_max:.2f}mbar")
    #secBackup.writelines(f"{date}\t{current_time}\t{cTemp:.2f}°C\t\t{average_temp:.2f}°C\t\t{tempC_min:.2f}°C\t\t{tempC_max:.2f}°C\t\t{pressure:.2f}mbar\t{average_press:.2f}mbar\t{press_min:.2f}mbar\t{press_max:.2f}mbar\t{humidity:.2f}RH\t{average_humi:.2f}RH\t{humi_min:.2f}RH\t{humi_max:.2f}RH")
    time.sleep(5)
