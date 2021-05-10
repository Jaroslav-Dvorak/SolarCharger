from pymodbus.client.sync import ModbusSerialClient as ModbusClient
from datetime import datetime


def uint2int(uint):
    if uint > 2147483647:
        return uint - 4294967295
    else:
        return uint


def merge_ints(low, high):
    res = (high << 16) | low
    return res


def split_16bit_to_8bit(x):
    high = (x >> 8) & 0xff
    low = x & 0xff
    return low, high


def merge_8bit_to_16bit(low, high):
    res = (high << 8) | low
    return res


class EPever:
    """http://www.solar-elektro.cz/data/dokumenty/1733_modbus_protocol.pdf"""
    def __init__(self):
        self.client = ModbusClient(method='rtu',
                                   port='/dev/ttyUSB0',
                                   baudrate=115200,
                                   timeout=1,
                                   stopbits=1,
                                   bytesize=8,
                                   handshaking='N',
                                   parity='N',
                                   strict=False)

    def read_all(self, unit):
        with self.client as client:
            mppt_data = {}

            result = client.read_input_registers(address=0x3100, count=8, unit=unit)
            mppt_data["Charging_equipment_input_voltage"] = result.registers[0]
            mppt_data["Charging_equipment_input_current"] = result.registers[1]
            mppt_data["Charging_equipment_output_voltage"] = result.registers[4]
            mppt_data["Charging_equipment_output_current"] = result.registers[5]
            mppt_data["Charging_equipment_output_power"] = merge_ints(result.registers[6], result.registers[7])

            result = client.read_input_registers(address=0x310C, count=6, unit=unit)
            mppt_data["Discharging_equipment_output_current"] = result.registers[1]
            mppt_data["Discharging_equipment_output_power"] = merge_ints(result.registers[2], result.registers[3])
            mppt_data["Temperature_inside_equipment"] = result.registers[5]

            result = client.read_input_registers(address=0x311B, count=1, unit=unit)
            mppt_data["Remote_battery_temperature"] = result.registers[0]

            result = client.read_input_registers(address=0x3304, count=2, unit=unit)
            mppt_data["Consumed_energy_today"] = merge_ints(result.registers[0], result.registers[1])

            result = client.read_input_registers(address=0x330A, count=4, unit=unit)
            mppt_data["Total_consumed_energy"] = merge_ints(result.registers[0], result.registers[1])
            mppt_data["Generated_energy_today"] = merge_ints(result.registers[2], result.registers[3])

            result = client.read_input_registers(address=0x3312, count=4, unit=unit)
            mppt_data["Total_generated_energy"] = merge_ints(result.registers[0], result.registers[1])
            mppt_data["Carbon_dioxide_reduction"] = merge_ints(result.registers[2], result.registers[3])

            result = client.read_input_registers(address=0x331B, count=2, unit=unit)
            mppt_data["Battery_current"] = uint2int(merge_ints(result.registers[0], result.registers[1]))

        return mppt_data

    def read_time(self, unit):
        with self.client as client:
            result = client.read_holding_registers(address=0x9013, count=3, unit=unit)
            second, minute = split_16bit_to_8bit(result.registers[0])
            hour, day = split_16bit_to_8bit(result.registers[1])
            month, year = split_16bit_to_8bit(result.registers[2])
            year += 2000
            print("čas: " + str(hour) + ":" + str(minute) + ":" + str(second))
            print("datum:" + str(day) + "." + str(month) + "." + str(year))
            return datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    def write_time(self, dt, unit):
        registers = [
                    merge_8bit_to_16bit(dt.second, dt.minute),
                    merge_8bit_to_16bit(dt.hour, dt.day),
                    merge_8bit_to_16bit(dt.month, dt.year - 2000)
                    ]

        with self.client as client:
            client.write_registers(address=0x9013, values=registers, unit=unit)
