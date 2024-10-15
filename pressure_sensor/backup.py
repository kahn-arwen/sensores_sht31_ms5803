import adafruit_sht31d
import board
import time
from datetime import datetime
import smbus
import os

bus = smbus.SMBus(1)
time.sleep(1)

i2c = board.I2C()
sensor = adafruit_sht31d.SHT31D(i2c)

# Initialize variables
tempC_min = float('inf')
tempC_max = float('-inf')
humi_min = float('inf')
humi_max = float('-inf')

# Accumulators
totalTempSum = 0
totalHumSum = 0
totalReadingCount = 0
average_temp = 0
average_humi = 0

file_path = "dados_sensor.txt"

# Verifica se o arquivo existe e está vazio
file_exists = os.path.isfile(file_path) and os.path.getsize(file_path) > 0

# Abre o arquivo em modo de anexação
with open(file_path, "a") as file:
    # Escreve o cabeçalho apenas se o arquivo estiver vazio
    if not file_exists:
        file.write("Data          Hora     Temp_atual   Temp_med   Temp_min   Temp_max   Umi_atual   Umi_med   Umi_min   Umi_max\n")

    while True:
        humidity = sensor.relative_humidity
        temp = sensor.temperature
        
        # Min/Max updates
        if temp > tempC_max:
            tempC_max = temp
        if temp < tempC_min:
            tempC_min = temp
        if humidity > humi_max:
            humi_max = humidity
        if humidity < humi_min:
            humi_min = humidity
        
        # Accumulate averages
        totalTempSum += temp
        totalHumSum += humidity
        totalReadingCount += 1
        
        if totalReadingCount > 0: 
            average_temp = totalTempSum / totalReadingCount  
            average_humi = totalHumSum / totalReadingCount
        
        now = datetime.now()
        date = now.date()
        current_time = f"{now.hour}:{now.minute}:{now.second}"
        
        # Cria a linha de saída
        output_line = f"{date}   {current_time}   {temp:.2f}°C     {average_temp:.2f}°C     {tempC_min:.2f}°C   {tempC_max:.2f}°C    {humidity:.2f}RH    {average_humi:.2f}RH    {humi_min:.2f}RH   {humi_max:.2f}RH\n"
        
        # Grava a linha no arquivo
        with open(file_path, "a") as file_append:
            file_append.write(output_line)
        
        # Exibe os dados no console
        print(output_line.strip())

        time.sleep(5)
