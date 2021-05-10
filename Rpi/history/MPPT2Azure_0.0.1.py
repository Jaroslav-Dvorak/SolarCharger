from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time
import pymssql
from datetime import datetime



stationID = "1"

MPPTdata = {}
client = ModbusClient(method = 'rtu', port = '/dev/ttyUSB0', baudrate = 115200)

SQLserver = "Server80" #nastavení v souborech /etc/odbc.ini, /etc/odbcinst.ini, /etc/freetds/freetds.conf
username = "supercharger@lizard" #format: username@domain (domain.database.windows.net)
password = "fJR88I#XtGs2"
dbname = "charger_develop"

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
	MPPTdata["Battery_Temperature"] = result.registers[4] 
	MPPTdata["Temperature_inside_equipment"] = result.registers[5] #Temperature inside case
	
	result = client.read_input_registers(0x311B,1,unit=1) #read value 311B
	MPPTdata["Remote_baterry_temperature"] = result.registers[0]
	
	result = client.read_input_registers(0x3304,2,unit=1) #read value 3304-3305
	MPPTdata["Consumed_energy_today"] = mergeLH(result.registers[0], result.registers[1])  #Clear every day
	
	result = client.read_input_registers(0x330A,4,unit=1) #read value 330A-330D
	MPPTdata["Total_consumed_energy"] = mergeLH(result.registers[0], result.registers[1])
	MPPTdata["Generated_energy_today"] = mergeLH(result.registers[2], result.registers[3])
	
	
	result = client.read_input_registers(0x3312,4,unit=1) #read value 3312-3315
	MPPTdata["Total_generated_energy"] = mergeLH(result.registers[0], result.registers[1])
	MPPTdata["Carbon_dioxide_reduction"] = mergeLH(result.registers[2], result.registers[3])
	
	result = client.read_input_registers(0x331B,2,unit=1) #read value 3312-3315
	MPPTdata["Battery_Current"] = Uint2Int(mergeLH(result.registers[0], result.registers[1]))
	
	client.close()

	
while True:
	ReadFromMPPT()
	azure = pymssql.connect(SQLserver, username, password, dbname)
	cursor = azure.cursor()
	
	print(datetime.now())
	for key, value in MPPTdata.items() :
		print ('{:<40} {:<8}'.format(key, value/100))
		subQ_IdParam = "(SELECT Id FROM StationParameters WHERE Name = '"+key+"')"
		Query = "INSERT INTO StationData (StationId, Parameter, Value) VALUES ("+stationID+","+subQ_IdParam+","+str(value)+")"
		cursor.execute(Query)
		#print(Query)

	azure.commit()
	azure.close()
	print("")
	time.sleep(300)



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
