import time
import smbus
import os
from datetime import datetime
import numpy as np

HOUR_READINGS = 720
DAY_READINGS = 17280

def write_header(file):
    file.write("Data\t\tHora\t\tTemp_atual\tTemp_med\tTemp_min\tTemp_max\tUmi_atual\tUmi_med\t\tUmi_min\t\tUmi_max\n")

def main():
    def is_file_empty(file_sec):
        return os.stat(file_sec).st_size == 0
    def is_file_empty(file_hour):
        return os.stat(file_hour).st_size == 0
    def is_file_empty(file_day):
        return os.stat(file_day).st_size == 0
    file_sec = '/home/tecnico/agsolve/temp_umi_sensor/sec_backup.txt'
    file_hour = '/home/tecnico/agsolve/temp_umi_sensor/hour_backup.txt'
    file_day = '/home/tecnico/agsolve/temp_umi_sensor/day_backup.txt'
    
    bus = smbus.SMBus(1)
    address = 0x44

    tempC_min, tempC_max = float('inf'), float('-inf')
    humi_min, humi_max = float('inf'), float('-inf')

    totalTempSum = totalTempHum = totalReadingCount = 0
    tempReadingsC_hour, humidityReadings_hour = [], []
    tempReadingsC_day, humidityReadings_day = [], []
    
    print ("Data\t\tHora\t\tTemp_atual\tTemp_med\tTemp_min\tTemp_max\tUmi_atual\tUmi_med\t\tUmi_min\t\tUmi_max\n")
    
    try: 
        with open("/home/tecnico/agsolve/temp_umi_sensor/sec_backup.txt", "a") as secBackup, \
             open("/home/tecnico/agsolve/temp_umi_sensor/hour_backup.txt", "a") as hourBackup, \
             open("/home/tecnico/agsolve/temp_umi_sensor/day_backup.txt", "a") as dayBackup:
            
            if is_file_empty(file_sec):
                write_header(secBackup)
            if is_file_empty(file_sec):
                write_header(hourBackup)
            if is_file_empty(file_sec):
                write_header(dayBackup) 

            while True:
                bus.write_i2c_block_data(address, 0x2C, [0x06])
                time.sleep(1)
                data = bus.read_i2c_block_data(address, 0x00, 6)

                cTemp = (((data[0] << 8) + data[1]) * 175.0) / 65535.0 - 45.0
                humidity = (((data[3] << 8) + data[4])) * 100.0 / 65535.0

                # Atualiza min/max
                tempC_min = min(tempC_min, cTemp)
                tempC_max = max(tempC_max, cTemp)
                humi_min = min(humi_min, humidity)
                humi_max = max(humi_max, humidity)

                totalTempSum += cTemp
                totalTempHum += humidity
                totalReadingCount += 1
                
                average_temp = totalTempSum / totalReadingCount
                average_humi = totalTempHum / totalReadingCount
                
                now = datetime.now()
                date = now.strftime("%d/%m/%Y")
                time_str = now.strftime("%H:%M:%S")

                print(f"{date}\t{time_str}\t{cTemp:.2f} °C\t{average_temp:.2f} °C\t{tempC_min:.2f} °C\t{tempC_max:.2f} °C\t{humidity:.2f} RH\t{average_humi:.2f} RH\t{humi_min:.2f} RH\t{humi_max:.2f} RH")
                
                secBackup.write(f"{date}\t{time_str}\t{cTemp:.2f} °C\t{average_temp:.2f} °C\t{tempC_min:.2f} °C\t{tempC_max:.2f} °C\t{humidity:.2f} RH\t{average_humi:.2f} RH\t{humi_min:.2f} RH\t{humi_max:.2f} RH\n")
                secBackup.flush()
                
                tempReadingsC_hour.append(cTemp)
                humidityReadings_hour.append(humidity)
                tempReadingsC_day.append(cTemp)
                humidityReadings_day.append(humidity)

                if len(tempReadingsC_hour) == HOUR_READINGS:
                    average_temp_hour = np.mean(tempReadingsC_hour)
                    average_humi_hour = np.mean(humidityReadings_hour)
                    hourBackup.write(f"{date}\t{time_str}\t{cTemp:.2f} °C\t{average_temp_hour:.2f} °C\t{tempC_min:.2f} °C\t{tempC_max:.2f} °C\t{humidity:.2f} RH\t{average_humi_hour:.2f} RH\t{humi_min:.2f} RH\t{humi_max:.2f} RH\n")
                    hourBackup.flush()
                    tempReadingsC_hour.clear()
                    humidityReadings_hour.clear()

                if len(tempReadingsC_day) == DAY_READINGS:
                    average_temp_day = np.mean(tempReadingsC_day)
                    average_humi_day = np.mean(humidityReadings_day)
                    dayBackup.write(f"{date}\t{time_str}\t{cTemp:.2f} °C\t{average_temp_day:.2f} °C\t{tempC_min:.2f} °C\t{tempC_max:.2f} °C\t{humidity:.2f} RH\t{average_humi_day:.2f} RH\t{humi_min:.2f} RH\t{humi_max:.2f} RH\n")
                    dayBackup.flush()
                    tempReadingsC_day.clear()
                    humidityReadings_day.clear()

                time.sleep(5)

    except Exception as e:
        print(f"Erro ao abrir ou escrever em arquivos: {e}")

if __name__ == "__main__":
    main()
