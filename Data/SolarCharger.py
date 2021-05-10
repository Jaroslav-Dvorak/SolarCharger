#!/usr/bin/env python3
from time import sleep
from datetime import datetime
from CsvWriter import CsvWriter
from SqlWriter import SqlWriter
import MPPTcom
import RaspIO


def vars_2_console(data):
    sep = "=" * 50
    print(sep)
    for key, value in data.items():
        key = key.lower()
        if "voltage" in key:
            unit = "V"
        elif "current" in key:
            unit = "A"
        elif "power" in key:
            unit = "W"
        elif "energy" in key:
            unit = "kWh"
        elif "temperature" in key:
            unit = "°C"
        elif "carbon" in key:
            unit = "Ton"
        else:
            unit = ""
        if key == "time":
            continue
        print('{:<38} {:>6} {:<8}'.format(key + ":", str(value / 100), unit))
    print(sep)


def csv_writer(file):
    while True:
        try:
            data = MPPT.read_all(unit=1)
            data["time"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            writer = CsvWriter(file=file, data=data)
        except Exception as e:
            print("error in csv_writer function:")
            print(e)
            sleep(2)
        else:
            print(datetime.now().strftime("%d.%m.%Y %H:%M"))
            vars_2_console(data)
            sleep(60)
            return writer


def main():
    read_err_count = 0
    realtime_data = {}
    while True:
        print(datetime.now().strftime("%d.%m.%Y %H:%M"))

        try:
            realtime_data = MPPT.read_all(unit=1)
            if datetime.now().minute == 0:
                MPPT.write_time(datetime.now(), unit=1)
        except Exception as E:
            print("MPPT communication error!")
            print(E)
            sleep(2)
            read_err_count += 1
            continue
        else:
            vars_2_console(realtime_data)
            realtime_data["time"] = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            CSV.write_line(realtime_data)
            realtime_data.pop("time")
            SQL.write_values(realtime_data)
        finally:
            print("MPPT Errors: " + str(read_err_count))

        if realtime_data["Charging_equipment_output_voltage"] < 2300:
            RaspIO.out_off(switchpin)
        if realtime_data["Charging_equipment_output_voltage"] > 2500:
            RaspIO.out_on(switchpin)

        print("CHARGING ACTIVE" if RaspIO.pin_state(switchpin) else "CHARGING INACTIVE")

        print("")
        sleep(60)


CONN_DATA = {
"user": "Script",
"password": "fJR88I#XtGs2",
"host": "192.168.1.111",
"port": "5432",
"database": "charger_develop"
}


if __name__ == '__main__':
    MPPT = MPPTcom.EPever()
    CSV = csv_writer("SolarData")
    SQL = SqlWriter(CONN_DATA)
    switchpin = 6

    main()
