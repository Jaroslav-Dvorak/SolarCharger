#!/usr/bin/env python3
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time
import pymssql
import RPi.GPIO as GPIO
from datetime import datetime

GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(26, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(20, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(16, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(19, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(13, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.IN, GPIO.PUD_DOWN)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(5, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

stationID = "1"

MPPTdata = {}
client = ModbusClient(method='rtu', port='/dev/ttyUSB0', baudrate=115200, timeout=10, stopbits =1, bytesize =8, handshaking ='N', parity ='N', debug = True)
#~ client = ModbusClient(method = 'rtu', port = '/dev/ttyUSB0', baudrate = 115200, timeout = 10)

SQLserver = "Server80" #nastavení v souborech /etc/odbc.ini, /etc/odbcinst.ini, /etc/freetds/freetds.conf
username = "supercharger@lizard" #format: username@domain (domain.database.windows.net)
password = "fJR88I#XtGs2"
dbname = "charger_develop"

mpptErr = 0
azureErr = 0

def mergeLH(L,H):
	res = (H<<16) | L
	return(res)
	
def Uint2Int(Uint):
	if Uint > 2147483647:
		return(Uint - 4294967295)
	else:
		return(Uint)

def ReadFromMPPT():			
	
	client.connect()
	
	result = client.read_input_registers(0x3100,8,unit=1) #read values 3100 - 3007
	MPPTdata["Charging_equipment_input_voltage"] = result.registers[0] #Solar charge controller -- PV array voltage
	MPPTdata["Charging_equipment_input_current"] = result.registers[1] #Solar charge controller -- PV array current
	MPPTdata["Charging_equipment_input_power"] = mergeLH(result.registers[2], result.registers[3]) #Solar charge controller -- PV array power
	MPPTdata["Charging_equipment_output_voltage"] = result.registers[4] #Battery voltage
	MPPTdata["Charging_equipment_output_current"] = result.registers[5] #Battery charging current
	MPPTdata["Charging_equipment_output_power"] = mergeLH(result.registers[6], result.registers[7])  #Battery charging power
	
	result = client.read_input_registers(0x310C,6,unit=1) #read values 310C - 3111
	MPPTdata["Discharging_equipment_output_voltage"] = result.registers[0] #Load voltage
	MPPTdata["Discharging_equipment_output_current"] = result.registers[1] #Load current
	MPPTdata["Discharging_equipment_output_power"] = mergeLH(result.registers[2], result.registers[3]) #Load voltage
	MPPTdata["Battery_temperature"] = result.registers[4] 
	MPPTdata["Temperature_inside_equipment"] = result.registers[5] #Temperature inside case
	
	result = client.read_input_registers(0x311B,1,unit=1) #read value 311B
	MPPTdata["Remote_battery_temperature"] = result.registers[0]
	
	result = client.read_input_registers(0x3304,2,unit=1) #read value 3304-3305
	MPPTdata["Consumed_energy_today"] = mergeLH(result.registers[0], result.registers[1])  #Clear every day
	
	result = client.read_input_registers(0x330A,4,unit=1) #read value 330A-330D
	MPPTdata["Total_consumed_energy"] = mergeLH(result.registers[0], result.registers[1])
	MPPTdata["Generated_energy_today"] = mergeLH(result.registers[2], result.registers[3])
	
	
	result = client.read_input_registers(0x3312,4,unit=1) #read value 3312-3315
	MPPTdata["Total_generated_energy"] = mergeLH(result.registers[0], result.registers[1])
	MPPTdata["Carbon_dioxide_reduction"] = mergeLH(result.registers[2], result.registers[3])
	
	result = client.read_input_registers(0x331B,2,unit=1) #read value 3312-3315
	MPPTdata["Battery_current"] = Uint2Int(mergeLH(result.registers[0], result.registers[1]))
	
	client.close()

def VarToConsole(key, value):
	keyLow = key.lower()
	if "voltage" in keyLow:
		unit = "V"
	elif "current" in keyLow:
		unit = "A"
	elif "power" in keyLow:
		unit = "W"
	elif "energy" in keyLow:
		unit = "kWh"
	elif "temperature" in keyLow:
		unit = "°C"
	elif "carbon" in keyLow:
		unit = "Ton"
	else:
		unit = ""
	print ('{:<38} {:>6} {:<8}'.format(key+":", str(value/100), unit))
	
while True:
	
	print(datetime.now())
	print("MPPT Errors: " + str(mpptErr))
	print("Azure Errors: " + str(azureErr))
	
	try:
		ReadFromMPPT()
	except:
		client.close()
		print("MPPT reading error!")
		time.sleep(10)
		mpptErr = mpptErr + 1
		continue
		
	try:
		azure = pymssql.connect(SQLserver, username, password, dbname)
	except:
		print("Connection to database error!")
		azureErr = azureErr + 1
		continue
	
	cursor = azure.cursor()
	
	for key, value in MPPTdata.items() :
		
		#~ subQ_IdParam = "(SELECT Id FROM StationParameters WHERE Name = '"+key+"')"
		#~ Query = "INSERT INTO StationData (StationId, Parameter, Value) VALUES ("+stationID+","+subQ_IdParam+","+str(value)+")"
		#~ try:
		cursor.callproc('SetStationData', (stationID, key, value))
		#~ except:
			#~ print("Read/Write database error!")
			#~ azureErr = azureErr + 1
			#~ continue
			
		VarToConsole(key, value)

	azure.commit()
	azure.close()
	
	if MPPTdata["Charging_equipment_output_voltage"] < 2300 and GPIO.input(6) == GPIO.HIGH:
		GPIO.output(6, False)
	if MPPTdata["Charging_equipment_output_voltage"] > 2500 and GPIO.input(6) == GPIO.LOW:
		GPIO.output(6, True)
		
	if GPIO.input(6) == GPIO.HIGH:
		print("vybíjení aktivní")
	else:
		print("vybíjení vypnuto")

	print("")
	time.sleep(60)
	
	

def infoAzureConfig():
	#autostart:
	#Python soubor-->vlastnosti-->práva-->spustit:kdokoliv
	#hashbang Python script: #!/bin/bash
	#do /home/pi vytvořit launcher.sh
	#launcher.sh:
	##!/bin/bash
	#echo "Starting MPPT2Azure.py"
	#python3 /home/pi/Desktop/MPPT2Azure.py
	#launcher.sh-->vlastnosti-->práva-->spustit:kdokoliv
	#sudo nano /etc/xdg/lxsession/LXDE-pi/autostart
	#přidat:
	#@lxterminal -e /home/pi/launcher.sh


	
	#Soubor: /etc/odbc.ini
	#[MSSQL8]
	#Driver = FreeTDS
	#Description = MSSQL Server
	#Trace = No
	#Servername = Server80
	#Server = lizard.database.windows.net      # IP or host name of the Sql Server
	#Database = charger_develop      # DataBase Name
	#Port = 1433           # This is default
	#TDS_Version = 8.0
	
	#Soubor: /etc/odbcinst.ini 
	#[FreeTDS]
	#Description = FreeTDS unixODBC Driver
	#Driver = /usr/lib/arm-linux-gnueabihf/odbc/libtdsodbc.so
	#Setup = /usr/lib/arm-linux-gnueabihf/odbc/libtdsodbc.so
	#UsageCount = 1
	
	#Soubor: /etc/freetds/freetds.conf
	##   $Id: freetds.conf,v 1.12 2007/12/25 06:02:36 jklowden Exp $
	##
	## This file is installed by FreeTDS if no file by the same 
	## name is found in the installation directory.  
	##
	## For information about the layout of this file and its settings, 
	## see the freetds.conf manpage "man freetds.conf".  
	
	## Global settings are overridden by those in a database
	## server specific section
	#[global]
	        ## TDS protocol version
	#;	tds version = 4.2
	
		## Whether to write a TDSDUMP file for diagnostic purposes
		## (setting this to /tmp is insecure on a multi-user system)
	#;	dump file = /tmp/freetds.log
	#;	debug flags = 0xffff
	
		## Command and connection timeouts
	#;	timeout = 10
	#;	connect timeout = 10
		
		## If you get out-of-memory errors, it may mean that your client
		## is trying to allocate a huge buffer for a TEXT field.  
		## Try setting 'text size' to a more reasonable limit 
		#text size = 64512
	
	## A typical Sybase server
	#[egServer50]
		#host = symachine.domain.com
		#port = 5000
		#tds version = 5.0
	
	## A typical Microsoft server
	#[egServer70]
		#host = ntmachine.domain.com
		#port = 1433
		#tds version = 7.0
	
	#[Server80]
	      #host = lizard.database.windows.net   # Remote Sql Server's IP addr
	      #port = 1433           # this is default
	      #tds version = 8.0     # this is by the time i post this
	      #client charset = UTF-8
	      ##instance = charger_develop     # your Database name 
	return(None)










#odpad:

#def StringDiv100(number):
	#return(str(float(number/100)))

#print("Battery_Current: "+StringDiv100(Battery_Current)+"A")
#print("Total_generated_energy: "+StringDiv100(Total_generated_energy)+"kWh")
#print("Carbon_dioxide_reduction: "+StringDiv100(Carbon_dioxide_reduction)+"Ton")
#print("Total_consumed_energy: "+StringDiv100(Total_consumed_energy)+"kWh")
#print("Generated_energy_today: "+StringDiv100(Generated_energy_today)+"kWh")
#print("Consumed_energy_today: "+StringDiv100(Consumed_energy_today)+"kWh")
#print("Remote_baterry_temperature: "+StringDiv100(Remote_baterry_temperature)+"°C")
#print("Discharging_equipment_output_voltage: "+StringDiv100(Discharging_equipment_output_voltage)+"V")
#print("Discharging_equipment_output_current: "+StringDiv100(Discharging_equipment_output_current)+"A")
#print("Discharging_equipment_output_power: "+StringDiv100(Discharging_equipment_output_power)+"W")
#print("Battery_Temperature: "+StringDiv100(Battery_Temperature)+"°C")
#print("Temperature_inside_equipment: "+StringDiv100(Temperature_inside_equipment)+"°C")
#print("Charging_equipment_input_voltage: "+StringDiv100(Charging_equipment_input_voltage)+"V")
#print("Charging_equipment_input_current: "+StringDiv100(Charging_equipment_input_current)+"A")
#print("Charging_equipment_input_power: "+StringDiv100(Charging_equipment_input_power)+"W")
#print("Charging_equipment_output_voltage: "+StringDiv100(Charging_equipment_output_voltage)+"V")
#print("Charging_equipment_output_current: "+StringDiv100(Charging_equipment_output_current)+"A")
#print("Charging_equipment_output_power: "+StringDiv100(Charging_equipment_output_power)+"W")

#cursor.execute("INSERT INTO StationData (StationId, Parameter, Value) VALUES ("+stationID+", (SELECT Id FROM StationParameters WHERE Name = 'Battery_Current'),"+ str(Battery_Current)+")")
#cursor.execute("INSERT INTO StationData (StationId, Parameter, Value) VALUES ("+stationID+", (SELECT Id FROM StationParameters WHERE Name = 'Charging_equipment_output_voltage'),"+ str(Charging_equipment_output_voltage)+")")




