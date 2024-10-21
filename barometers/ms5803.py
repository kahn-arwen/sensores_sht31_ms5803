import smbus
import time
import os
from datetime import datetime

bar1 = 0x77 #Nacional (pequeno)
bar2 = 0x76 #Internacional (grande)

day_reading = 17280
hour_reading = 720

tempC_min_bar1 = float('inf')              
tempC_min_bar2 = float('inf')
tempC_max_bar1 = float('-inf')
tempC_max_bar2 = float('-inf')
press_min_bar1 = float('inf')
press_min_bar2 = float('inf')
press_max_bar1 = float('-inf')
press_max_bar2 = float('-inf')  

tempC_min_hour_bar1 = float('inf')
tempC_min_hour_bar2 = float('inf')
tempC_max_hour_bar1 = float('-inf')
tempC_max_hour_bar2 = float('-inf')
press_min_hour_bar1 = float('inf')
press_min_hour_bar2 = float('inf')
press_max_hour_bar1 = float('-inf')
press_max_hour_bar2 = float('-inf')

# Acumuladores
tempSumC_day_bar1 = 0
tempSumC_day_bar2 = 0
pressSum_day_bar1 = 0
pressSum_day_bar2 = 0
##                ##
tempSumC_hour_bar1 = 0
tempSumC_hour_bar2 = 0
pressSum_hour_bar1 = 0
pressSum_hour_bar2 = 0
#
totalTempSum_bar1  = 0
totalTempSum_bar2  = 0
totalPressSum_bar1 = 0
totalPressSum_bar2 = 0
#
totalReadingCount = 0	
readingCount_hour = 0
readingCount_day  = 0
#
average_press_bar1 = 0
average_press_bar2 = 0 
average_temp_bar1  = 0
average_temp_bar2  = 0
average_press_hour_bar1 = 0
average_press_hour_bar2 = 0
average_temp_hour_bar1  = 0
average_temp_hour_bar2  = 0
average_press_day_bar1  = 0
average_press_day_bar2  = 0
average_temp_day_bar1   = 0
average_temp_day_bar2   = 0

secBackup_bar1 = "/home/tecnico/agsolve/barometers/sec_Backup_bar1.txt"
hourBackup_bar1 = "/home/tecnico/agsolve/barometers/hour_Backup_bar1.txt"
dayBackup_bar1  = "/home/tecnico/agsolve/barometers/day_Backup_bar1.txt"

secBackup_bar2 = "/home/tecnico/agsolve/barometers/sec_Backup_bar2.txt"
hourBackup_bar2 = "/home/tecnico/agsolve/barometers/hour_Backup_bar2.txt"
dayBackup_bar2 = "/home/tecnico/agsolve/barometers/day_Backup_bar2.txt"

backupSec_existe_bar1 = os.path.isfile(secBackup_bar1) and os.path.getsize(secBackup_bar1) > 0
backupHour_existe_bar1 = os.path.isfile(hourBackup_bar1) and os.path.getsize(hourBackup_bar1) > 0
backupDay_existe_bar1 = os.path.isfile(dayBackup_bar1) and os.path.getsize(dayBackup_bar1) > 0

backupSec_existe_bar2 = os.path.isfile(secBackup_bar2) and os.path.getsize(secBackup_bar2) > 0
backupHour_existe_bar2 = os.path.isfile(hourBackup_bar2) and os.path.getsize(hourBackup_bar2) > 0
backupDay_existe_bar2 = os.path.isfile(dayBackup_bar2) and os.path.getsize(dayBackup_bar2) > 0


write_header = "Data          Hora     Bar    Temp_atual   Temp_med   Temp_min   Temp_max   Press_atual   Press_med    Press_min   Press_max\n"


with open(secBackup_bar1, "a") as file:
    # Escreve o cabeçalho apenas se o arquivo estiver vazio
    if not backupSec_existe_bar1:
        file.write(write_header)
        
with open(secBackup_bar2, "a") as file:
    # Escreve o cabeçalho apenas se o arquivo estiver vazio
    if not backupSec_existe_bar2:
        file.write(write_header)
        
with open(hourBackup_bar1, "a") as file:
    if not backupHour_existe_bar1:
        file.write(write_header)
        
with open(hourBackup_bar2, "a") as file:
    if not backupHour_existe_bar2:
        file.write(write_header)
        
with open(dayBackup_bar1, "a") as file:
    if not backupDay_existe_bar1:
        file.write(write_header)

with open(dayBackup_bar2, "a") as file:
    if not backupDay_existe_bar2:
        file.write(write_header)


		
print (write_header)

def readBarometer(address):
    bus = smbus.SMBus(1)
    bus.write_byte(address, 0x1E)
    time.sleep(0.5)

    # calibration data
    data = bus.read_i2c_block_data(address, 0xA2, 2)
    C1 = data[0] * 256 + data[1]
    data = bus.read_i2c_block_data(address, 0xA4, 2)
    C2 = data[0] * 256 + data[1]
    data = bus.read_i2c_block_data(address, 0xA6, 2)
    C3 = data[0] * 256 + data[1]
    data = bus.read_i2c_block_data(address, 0xA8, 2)
    C4 = data[0] * 256 + data[1]
    data = bus.read_i2c_block_data(address, 0xAA, 2)
    C5 = data[0] * 256 + data[1]
    data = bus.read_i2c_block_data(address, 0xAC, 2)
    C6 = data[0] * 256 + data[1]

    # Pressure conversion(OSR = 256) command
    bus.write_byte(address, 0x40)
    time.sleep(0.5)
    # Read digital pressure value
    value = bus.read_i2c_block_data(address, 0x00, 3)
    D1 = value[0] * 65536 + value[1] * 256 + value[2]
    # Temperature conversion(OSR = 256) command
    bus.write_byte(address, 0x50)
    time.sleep(0.5)

    # Read digital temperature value
    value = bus.read_i2c_block_data(address, 0x00, 3)
    D2 = value[0] * 65536 + value[1] * 256 + value[2]

    dT = D2 - C5 * 256
    TEMP = 2000 + dT * C6 / 8388608
    OFF = C2 * 65536 + (C4 * dT) / 128
    SENS = C1 * 32768 + (C3 * dT ) / 256
    T2 = 0
    OFF2 = 0
    SENS2 = 0

    if TEMP > 2000 :
        T2 = 7 * (dT * dT)/ 137438953472
        OFF2 = ((TEMP - 2000) * (TEMP - 2000)) / 16
        SENS2= 0
    elif TEMP < 2000 :
        T2 = 3 * (dT * dT) / 8589934592
        OFF2 = 3 * ((TEMP - 2000) * (TEMP - 2000)) / 8
        SENS2 = 5 * ((TEMP - 2000) * (TEMP - 2000)) / 8
        if TEMP < -1500:
            OFF2 = OFF2 + 7 * ((TEMP + 1500) * (TEMP + 1500))
            SENS2 = SENS2 + 4 * ((TEMP + 1500) * (TEMP + 1500))

    TEMP = TEMP - T2
    OFF = OFF - OFF2
    SENS = SENS - SENS2
    cTemp = TEMP / 100.0
    pressure = ((((D1 * SENS) / 2097152) - OFF) / 32768.0) / 100.0
    
    
    return cTemp, pressure

while True:
    
    
    try:
        now = datetime.now()
        date = now.date()
        current_time = f"{now.hour:02}:{now.minute:02}:{now.second:02}"
    
        #Barometer 1 = nacional
        cTemp_bar1, pressure_bar1 = readBarometer(bar1)
        #Barometer 2 = internacional
        cTemp_bar2, pressure_bar2 = readBarometer(bar2)
        
		#min/max temp/press BAR1
        if(cTemp_bar1 > tempC_max_bar1):
            tempC_max_bar1 = cTemp_bar1
        if (cTemp_bar1 < tempC_min_bar1):
            tempC_min_bar1 = cTemp_bar1
        if(cTemp_bar1 > tempC_max_hour_bar1):
            tempC_max_hour_bar1 = cTemp_bar1
        if (cTemp_bar1 < tempC_min_hour_bar1):
            tempC_min_hour_bar1 = cTemp_bar1
            		
        if(pressure_bar1 > press_max_bar1):
            press_max_bar1 = pressure_bar1
        if(pressure_bar1 < press_min_bar1):
            press_min_bar1 = pressure_bar1
        if(pressure_bar1 > press_max_hour_bar1):
            press_max_hour_bar1 = pressure_bar1
        if(pressure_bar1 < press_min_hour_bar1):
            press_min_hour_bar1 = pressure_bar1
            
        #min/max temp/press BAR2
        if(cTemp_bar2 > tempC_max_bar2):
            tempC_max_bar2 = cTemp_bar2
        if (cTemp_bar2 < tempC_min_bar2):
            tempC_min_bar2 = cTemp_bar2
        if(cTemp_bar2 > tempC_max_hour_bar2):
            tempC_max_hour_bar2 = cTemp_bar2
        if (cTemp_bar2 < tempC_min_hour_bar2):
            tempC_min_hour_bar2 = cTemp_bar2
            		
        if(pressure_bar2 > press_max_bar2):
            press_max_bar2 = pressure_bar2
        if(pressure_bar2 < press_min_bar2):
            press_min_bar2 = pressure_bar2
        if(pressure_bar2 > press_max_hour_bar2):
            press_max_hour_bar2 = pressure_bar2
        if(pressure_bar2 < press_min_hour_bar2):
            press_min_hour_bar2 = pressure_bar2
				
		#acum average
        totalTempSum_bar1  += cTemp_bar1
        totalTempSum_bar2  += cTemp_bar2
        tempSumC_hour_bar1 += cTemp_bar1
        tempSumC_hour_bar2 += cTemp_bar2
        tempSumC_day_bar1  += cTemp_bar1
        tempSumC_day_bar2  += cTemp_bar2
			
        totalPressSum_bar1 += pressure_bar1
        totalPressSum_bar2 += pressure_bar2
        pressSum_hour_bar1 += pressure_bar1
        pressSum_hour_bar2 += pressure_bar2
        pressSum_day_bar1  += pressure_bar1
        pressSum_day_bar2  += pressure_bar2
			
        totalReadingCount = totalReadingCount+1
			
        if(totalReadingCount > 0): 
            average_temp_bar1 = totalTempSum_bar1 / totalReadingCount  
            average_temp_bar2 = totalTempSum_bar2 / totalReadingCount  
            average_press_bar1 = totalPressSum_bar1 / totalReadingCount
            average_press_bar2 = totalPressSum_bar2 / totalReadingCount
            
        print(f"{date}   {current_time}   1     {cTemp_bar1:.2f}°C       {average_temp_bar1:.2f}°C    {tempC_min_bar1:.2f}°C   {tempC_max_bar1:.2f}°C    {pressure_bar1:.2f}mbar    {average_press_bar1:.2f}mbar   {press_min_bar1:.2f}mbar  {press_max_bar1:.2f}mbar\n")   
        print(f"                        2     {cTemp_bar2:.2f}°C       {average_temp_bar2:.2f}°C    {tempC_min_bar2:.2f}°C   {tempC_max_bar2:.2f}°C    {pressure_bar2:.2f}mbar    {average_press_bar2:.2f}mbar   {press_min_bar2:.2f}mbar  {press_max_bar2:.2f}mbar\n")
			
        with open(secBackup_bar1, "a") as file_append:
            file_append.write(f"{date}   {current_time}   1     {cTemp_bar1:.2f}°C      {average_temp_bar1:.2f}°C    {tempC_min_bar1:.2f}°C    {tempC_max_bar1:.2f}°C     {pressure_bar1:.2f}mbar   {average_press_bar1:.2f}mbar  {press_min_bar1:.2f}mbar  {press_max_bar1:.2f}mbar\n")
        with open(secBackup_bar2, "a") as file_append:
            file_append.write(f"{date}   {current_time}   2     {cTemp_bar2:.2f}°C      {average_temp_bar2:.2f}°C    {tempC_min_bar2:.2f}°C    {tempC_max_bar2:.2f}°C     {pressure_bar2:.2f}mbar   {average_press_bar2:.2f}mbar  {press_min_bar2:.2f}mbar  {press_max_bar2:.2f}mbar\n")
			
			
        if(readingCount_hour < hour_reading):
            readingCount_hour +=1
        if (readingCount_day < day_reading):
            readingCount_day +=1
			
				
        if(readingCount_hour == hour_reading):
            average_temp_hour_bar1 = tempSumC_hour_bar1  / readingCount_hour
            average_temp_hour_bar2 = tempSumC_hour_bar2  / readingCount_hour
            average_press_hour_bar1 = pressSum_hour_bar1 / readingCount_hour
            average_press_hour_bar2 = pressSum_hour_bar2 / readingCount_hour
            
            with open(hourBackup_bar1, "a") as file_append:
                file_append.write(f"{date}   {current_time}   1     {cTemp_bar1:.2f}°C      {average_temp_hour_bar1:.2f}°C    {tempC_min_bar1:.2f}°C    {tempC_max_bar1:.2f}°C     {pressure_bar1:.2f}mbar   {average_press_hour_bar1:.2f}mbar  {press_min_bar1:.2f}mbar  {press_max_bar1:.2f}mbar\n")
            with open(hourBackup_bar2, "a") as file_append:
                file_append.write(f"{date}   {current_time}   2     {cTemp_bar2:.2f}°C      {average_temp_hour_bar2:.2f}°C    {tempC_min_bar2:.2f}°C    {tempC_max_bar2:.2f}°C     {pressure_bar2:.2f}mbar   {average_press_hour_bar2:.2f}mbar  {press_min_bar2:.2f}mbar  {press_max_bar2:.2f}mbar\n")
				
            readingCount_hour  = 0
            tempSumC_hour_bar1 = 0
            tempSumC_hour_bar2 = 0
            pressSum_hour_bar1 = 0
            pressSum_hour_bar2 = 0
				
            tempC_min_hour_bar1 = float('-inf')
            tempC_min_hour_bar2 = float('inf')
            tempC_max_hour_bar1 = float('-inf')
            tempC_max_hour_bar2 = float('-inf')
            press_min_hour_bar1 = float('-inf')
            press_min_hour_bar2 = float('inf')
            press_max_hour_bar1 = float('-inf')
            press_max_hour_bar2 = float('-inf')
			
        if(readingCount_day == day_reading):
            average_temp_day_bar1 = tempSumC_day_bar1/day_reading
            average_temp_day_bar1 = tempSumC_day_bar2/day_reading
            average_press_day_bar1 = pressSum_day_bar1/day_reading
            average_press_day_bar2 = pressSum_day_bar2/day_reading
            
            with open(dayBackup_bar1, "a") as file_append:
                file_append.write(f"{date}   {current_time}   1     {cTemp_bar1:.2f}°C      {average_temp_day_bar1:.2f}°C    {tempC_min_bar1:.2f}°C    {tempC_max_bar1:.2f}°C     {pressure_bar1:.2f}mbar   {average_press_day_bar1:.2f}mbar  {press_min_bar1:.2f}mbar  {press_max_bar1:.2f}mbar\n")
            with open(dayBackup_bar2, "a") as file_append:
                file_append.write(f"{date}   {current_time}   2     {cTemp_bar2:.2f}°C      {average_temp_day_bar2:.2f}°C     {tempC_min_bar2:.2f}°C    {tempC_max_bar2:.2f}°C     {pressure_bar2:.2f}mbar   {average_press_day_bar2:.2f}mbar  {press_min_bar2:.2f}mbar  {press_max_bar2:.2f}mbar\n")
            
            readingCount_day  = 0
            tempSumC_day_bar1_bar1 = 0
            tempSumC_day_bar2 = 0
            pressSum_day_bar1 = 0
            pressSum_day_bar2 = 0
    
    except Exception as e:
        now = datetime.now()
        date = now.date()
        current_time = f"{now.hour:02}:{now.minute:02}:{now.second:02}"
    
        error_message = f"{date} {current_time} Erro: {e}. Tentando novamente...\n"
        print(error_message)
        
    time.sleep(3.5)
