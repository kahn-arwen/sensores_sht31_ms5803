import adafruit_sht31d
import board
import ms5803py
import time
from datetime import datetime
import smbus
import os

# Definições de constantes
day_reading = 17280
hour_reading = 720

# Inicializações de variáveis
tempC_min = float('inf')
tempC_max = float('-inf')
press_min = float('inf')
press_max = float('-inf')
humi_min = float('inf')
humi_max = float('-inf')

# Acumuladores
tempSumC_day = 0
humiditySum_day = 0
pressSum_day = 0

tempSumC_hour = 0
humiditySum_hour = 0
pressSum_hour = 0

totalTempSum = 0
totalPressSum = 0
totalHumSum = 0

totalReadingCount = 0	
readingCount_hour = 0
readingCount_day = 0

average_press = 0
average_temp = 0
average_humi = 0
average_press_hour = 0
average_temp_hour = 0
average_humi_hour = 0
average_press_day = 0
average_temp_day = 0
average_humi_day = 0

# Caminhos dos arquivos de backup
secBackup = "/home/tecnico/agsolve/pressure_sensor/sec_Backup.txt"
hourBackup = "/home/tecnico/agsolve/pressure_sensor/hour_Backup.txt"
dayBackup = "/home/tecnico/agsolve/pressure_sensor/day_Backup.txt"

# Verifica se os arquivos existem e cria cabeçalhos se necessário
writesht = "Data          Hora     Temp_atual   Temp_med   Temp_min   Temp_max   Umi_atual   Umi_med   Umi_min   Umi_max   Press_atual   Press_med   Press_min   Press_max\n"

for backup_file in [secBackup, hourBackup, dayBackup]:
    if not os.path.isfile(backup_file) or os.path.getsize(backup_file) == 0:
        with open(backup_file, "a") as file:
            file.write(writesht)

print(writesht)

while True:
    time.sleep(1)
    i2c = board.I2C()
    
    try:
        # Tenta ler do SHT31
        sensor = adafruit_sht31d.SHT31D(i2c)
        humidity = sensor.relative_humidity
        temp = sensor.temperature
        
        # Tenta ler do MS5803
        s = ms5803py.MS5803()
        press, _ = s.read(pressure_osr=512)  # Leitura do barômetro
        
        # Atualiza min/max de temperatura e umidade
        tempC_max = max(temp, tempC_max)
        tempC_min = min(temp, tempC_min)
        humi_max = max(humidity, humi_max)
        humi_min = min(humidity, humi_min)

        # Acumula as leituras
        totalTempSum += temp
        totalHumSum += humidity
        totalReadingCount += 1

        if totalReadingCount > 0: 
            average_temp = totalTempSum / totalReadingCount  
            average_humi = totalHumSum / totalReadingCount
            
        now = datetime.now()
        date = now.date()
        current_time = f"{now.hour:02}:{now.minute:02}:{now.second:02}"

        print(f"{date}   {current_time}   {temp:.2f}°C   {average_temp:.2f}°C   {tempC_min:.2f}°C   {tempC_max:.2f}°C   {humidity:.2f}RH   {average_humi:.2f}RH   {humi_min:.2f}RH   {humi_max:.2f}RH   {press:.2f}mbar")

        with open(secBackup, "a") as file_append:
            file_append.write(f"{date}   {current_time}   {temp:.2f}°C   {average_temp:.2f}°C   {tempC_min:.2f}°C   {tempC_max:.2f}°C   {humidity:.2f}RH   {average_humi:.2f}RH   {humi_min:.2f}RH   {humi_max:.2f}RH   {press:.2f}mbar\n")

        # Gerenciamento de leituras horárias e diárias
        if readingCount_hour < hour_reading:
            readingCount_hour += 1

        if readingCount_hour == hour_reading:
            average_temp_hour = tempSumC_hour / readingCount_hour
            average_humi_hour = humiditySum_hour / readingCount_hour
            with open(hourBackup, "a") as file_append:
                file_append.write(f"{date}   {current_time}   {temp:.2f}°C   {average_temp_hour:.2f}°C   {tempC_min:.2f}°C   {tempC_max:.2f}°C   {humidity:.2f}RH   {average_humi_hour:.2f}RH   {humi_min:.2f}RH   {humi_max:.2f}RH   {press:.2f}mbar\n")
            readingCount_hour = 0

        if readingCount_day < day_reading:
            readingCount_day += 1

        if readingCount_day == day_reading:
            average_temp_day = tempSumC_day / day_reading
            average_humi_day = humiditySum_day / day_reading
            with open(dayBackup, "a") as file_append:
                file_append.write(f"{date}   {current_time}   {temp:.2f}°C   {average_temp_day:.2f}°C   {tempC_min:.2f}°C   {tempC_max:.2f}°C   {humidity:.2f}RH   {average_humi_day:.2f}RH   {humi_min:.2f}RH   {humi_max:.2f}RH   {press:.2f}mbar\n")
            readingCount_day = 0

    except Exception as e:
        now = datetime.now()
        date = now.date()
        current_time = f"{now.hour:02}:{now.minute:02}:{now.second:02}"
        error_message = f"{date} {current_time} Erro ao ler do sensor: {e}. Tentando novamente em 5 segundos...\n"
        print(error_message)

        with open(secBackup, "a") as file_append:
            file_append.write(error_message)

        time.sleep(5)

