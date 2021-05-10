variables = \
{
    "rated data":
    {
        "charging equipment rated input voltage": {"address": [0x3000], "description": "PV array rated voltage", "unit": "V", "times": 100},
        "charging equipment rated input current": {"address": [0x3001], "description": "PV array rated current", "unit": "A", "times": 100},
        "charging equipment rated input power": {"address": [0x3002, 0x3003], "description": "PV array rated power", "unit": "W", "times": 100},
        "charging equipment rated output voltage": {"address": [0x3004], "description": "battery's voltage", "unit": "V", "times": 100},
        "charging equipment rated output current": {"address": 0x3005, "description": "rated charging current to battery", "unit": "A", "times": 100},
        "charging equipment rated output power": {"address": [0x3006, 0x3007], "description": "rated charging power to battery", "unit": "W", "times": 100},
        "charging mode": {"address": 0x3008, "description": "0001H-PWM", "unit": "", "times": 1},
        "rated output current of load": {"address": 0x300E, "description": "", "unit": "A", "times": 100}
    },
    "real-time data":
    {
        "charging equipment input voltage": {"address": [0x3100], "description": "PV array voltage", "unit": "V", "times": 100},
        "charging equipment input current": {"address": [0x3101], "description": "PV array current", "unit": "A", "times": 100},
        "charging equipment input power": {"address": [0x3102, 0x3103], "description": "PV array power", "unit": "W", "times": 100},
        "charging equipment output voltage": {"address": [0x3104], "description": "battery voltage", "unit": "V", "times": 100},
        "charging equipment output current": {"address": [0x3105], "description": "battery charging current", "unit": "A", "times": 100},
        "charging equipment output power": {"address": [0x3106, 0x3107], "description": "battery charging power", "unit": "W", "times": 100},
        "discharging equipment output voltage": {"address": [0x310C], "description": "load voltage", "unit": "V", "times": 100},
        "discharging equipment output current": {"address": [0x310D], "description": "load current", "unit": "A", "times": 100},
        "battery temperature": {"address": [0x3110], "description": "battery temperature", "unit": "°C", "times": 100},
        "temperature inside equipment": {"address": [0x3111], "description": "temperature inside case", "unit": "°C", "times": 100},
        "power components temperature ": {"address": [0x3112], "description": "heat sink surface temperature", "unit": "°C", "times": 100},
        "battery SOC": {"address": [0x311A], "description": "the percentage of battery's remaining capacity", "unit": "%", "times": 100},
        "remote battery temperature": {"address": [0x311B], "description": "The battery temperature measured by remote temperature sensor", "unit": "°C", "times": 100},
        "battery's real rated power": {"address": [0x311D], "description": "current system rated voltage. 1200, 2400 represent 12V, 24V ", "unit": "V", "times": 100}
    },
    "real-time status":
    {
        "battery status": {"address": [0x3200], "description": "D3-D0: 01H over voltage, 00H normal, 02H under voltage, 03H Low Volt Disconnect, 04H Fault"
                                                               "D7-D4: 00H Normal, 01H Over Temperature,  02H Under Temperature,"
                                                               "D8: Battery internal resistance abnormal 1, normal 0"
                                                               "D15: 1-Wrong identification for rated voltage"},
        "charging equipment status": {"address": [0x3201], "description": "D15-D14: Input volt status. 00 normal, 01 no power connected, 02H Higher volt input, 03H Input volt error"
                                                                          "D13: Charging MOSFET is short."
                                                                          "D12: Charging or Anti-reverse MOSFET is short"
                                                                          "D11: Anti-reverse MOSFET is short."
                                                                          "D10: Input is over current."
                                                                          "D9: The load is Over current."
                                                                          "D8: The load is short."
                                                                          "D7: Load MOSFET is short."
                                                                          "D4: PV Input is short."
                                                                          "D3-2: Charging status. 00 No charging,01 Float,02 Boost,03 Equalization."
                                                                          "D1: 0 Normal, 1 Fault."
                                                                          "D0: 1 Running, 0 Standby."}
    },
    "statistical parameter":
    {
        "maximum input volt (PV) today": {"address": [0x3300], "description": "00: 00 Refresh every day", "unit": "V", "times": 100},
        "minimum input volt (PV) today": {"address": [0x3301], "description": "00: 00 Refresh every day", "unit": "V", "times": 100},
        "maximum battery volt today": {"address": [0x3302], "description": "00: 00 Refresh every day", "unit": "V", "times": 100},
        "minimum battery volt today": {"address": [0x3303], "description": "00: 00 Refresh every day", "unit": "V", "times": 100},
        "consumed energy today": {"address": [0x3304, 0x3305], "description": "00: 00 Clear every day", "unit": "kWh", "times": 100},
        "consumed energy this month": {"address": [0x3306, 0x3307], "description": "00: 00 Clear on the first day of month", "unit": "kWh", "times": 100},
        "consumed energy this year": {"address": [0x3308, 0x3309], "description": "00: 00 Clear on 1, Jan", "unit": "kWh", "times": 100},
        "total consumed energy": {"address": [0x330A, 0x330B], "description": "", "unit": "kWh", "times": 100},
        "generated energy today": {"address": [0x330C, 0x330D], "description": "00: 00 Clear every day", "unit": "kWh", "times": 100},
        "generated energy this month": {"address": [0x330E, 0x330F], "description": "00: 00 Clear on the first day of month", "unit": "kWh", "times": 100},
        "generated energy this year": {"address": [0x3310, 0x3311], "description": "00: 00 Clear on 1, Jan", "unit": "kWh", "times": 100},
        "total generated energy": {"address": [0x3312, 0x3313], "description": "", "unit": "kWh", "times": 100},
        "carbon dioxide reduction": {"address": [0x3314, 0x3315], "description": "Saving 1 Kilowatt=Reduction 0.997kg", "unit": "Ton", "times": 100},
        "battery current": {"address": [0x331B, 0x331C], "description": "The positive value represents charging and negative discharging", "unit": "Ton", "times": 100},
        "battery temperature": {"address": [0x331D], "description": "", "unit": "°C", "times": 100},
        "ambient temperature": {"address": [0x331E], "description": "", "unit": "°C", "times": 100}
    },
    "setting parameter":
    {
        "battery type": {"address": [0x9000], "description": "0001H- Sealed , 0002H- GEL, 0003H- Flooded, 0000H- User defined"},
        "battery capacity": {"address": [0x9001], "description": "rated capacity of the battery ", "unit": "AH", "times": 1},
        "Temperature compensation coefficient": {"address": [0x9002], "description": "range 0-9", "unit": "mV/°C/2V", "times": 100},
        "high voltage disconnect": {"address": [0x9003], "description": "", "unit": "V", "times": 100},
        "charging limit voltage": {"address": [0x9004], "description": "", "unit": "V", "times": 100},
        "over voltage reconnect": {"address": [0x9005], "description": "", "unit": "V", "times": 100},
        "equalization voltage": {"address": [0x9006], "description": "", "unit": "V", "times": 100},
        "boost voltage": {"address": [0x9007], "description": "", "unit": "V", "times": 100},
        "float voltage ": {"address": [0x9008], "description": "", "unit": "V", "times": 100},
        "boost reconnect voltage ": {"address": [0x9009], "description": "", "unit": "V", "times": 100},
        "low voltage reconnect": {"address": [0x900A], "description": "", "unit": "V", "times": 100},
        "under voltage recover": {"address": [0x900B], "description": "", "unit": "V", "times": 100},
        "under voltage warning": {"address": [0x900C], "description": "", "unit": "V", "times": 100},
        "low voltage disconnect": {"address": [0x900D], "description": "", "unit": "V", "times": 100},
        "discharging limit voltage": {"address": [0x900E], "description": "", "unit": "V", "times": 100},
        "real time clock": {"address": [0x9013, 0x9014, 0x9015], "description": "(D7-0 sec, D15-8 min), (D7-0 Hour, D15-8 Day), (D7-0 Month, D15-8 Year)", "unit": "S:M H:D M/Y", "times": 1},
        "equalization charging cycle": {"address": [0x9013, 0x9014, 0x9015], "description": "Interval days of auto equalization charging in cycle", "unit": "day", "times": 1},
        "battery temperature warning upper limit": {"address": [0x9017], "description": "", "unit": "°C", "times": 100},
        "battery temperature warning lower limit": {"address": [0x9018], "description": "", "unit": "°C", "times": 100},
        "controller inner temperature upper limit": {"address": [0x9019], "description": "", "unit": "°C", "times": 100},
        "controller inner temperature upper limit recover": {"address": [0x901A], "description": "After OverTemp, recover when drop lower than this value", "unit": "°C", "times": 100},
        "Power component temperature upper limit": {"address": [0x901B], "description": "Surface temperature of power components, charging and discharging stop", "unit": "°C", "times": 100},
        "power component temperature upper limit recover": {"address": [0x901C], "description": "Recover once power components temperature lower", "unit": "°C", "times": 100},
        "line impedance": {"address": [0x901D], "description": "the resistance of the connected wires", "unit": "miliohm", "times": 100},
        "night time threshold voltage": {"address": [0x901E], "description": "PV voltage lower than this value, controller would detect it as sundown", "unit": "V", "times": 100},
        "light signal night delay time": {"address": [0x901F], "description": "night threshold voltage and duration exceeds delay time, detect as night time", "unit": "min", "times": 1},
        "day time threshold voltage": {"address": [0x9020], "description": "PV voltage higher than this value, controller would detect it as sunrise", "unit": "V", "times": 100},
        "light signal day delay time": {"address": [0x9021], "description": "day threshold voltage and duration exceeds delay time delay, detect as daytime", "unit": "min", "times": 1},
        "load controlling modes": {"address": [0x903D], "description": "0000H Manual Control, 0001H Light ON/OFF, 0002H Light ON+Timer, 0003H Time Control"},
        "working time length 1": {"address": [0x903E], "description": "the length of load output timer 1, D15-D8: hour, D7-D0: minute", "unit": "H:M", "times": 1},
        "working time length 2": {"address": [0x903F], "description": "the length of load output timer 2, D15-D8: hour, D7-D0: minute", "unit": "H:M", "times": 1},
        "turn on timing 1": {"address": [0x9042, 0x9043, 0x9044], "description": "turn on timing of load output (sec, min, hour)", "unit": "S:M:H", "times": 1},
        "turn off timing 1": {"address": [0x9045, 0x9046, 0x9047], "description": "turn off timing of load output (sec, min, hour)", "unit": "S:M:H", "times": 1},
        "turn on timing 2": {"address": [0x9048, 0x9049, 0x904A], "description": "turn on timing of load output (sec, min, hour)", "unit": "S:M:H", "times": 1},
        "turn off timing 2": {"address": [0x904B, 0x904C, 0x904D], "description": "turn off timing of load output (sec, min, hour)", "unit": "S:M:H", "times": 1},
        "length of night": {"address": [0x9065], "description": "set default values of the whole night length of time. D15-D8: hour, D7-D0: minute", "unit": "H:M", "times": 1},
        "battery rated voltage code": {"address": [0x9067], "description": "0: auto recognize, 1: 12V, 2: 24V", "unit": "", "times": 1},
        "load timing control selection": {"address": [0x9069], "description": "selected timing period of the load. 0: using one timer, 1: using two timer, likewise", "unit": "", "times": 1},
        "default load onoOff in manual mode": {"address": [0x906A], "description": "0: off, 1: on", "unit": "", "times": 1},
        "equalize duration": {"address": [0x906B], "description": "usually 60-120 minutes", "unit": "min", "times": 1},
        "boost duration": {"address": [0x906C], "description": "usually 60-120 minutes", "unit": "min", "times": 1},
        "discharging percentage": {"address": [0x906D], "description": "usually 20%-80%. the percentage of battery's remaining capacity when stop charging", "unit": "%", "times": 100},
        "charging percentage": {"address": [0x906E], "description": "depth of charge, 20%-100%", "unit": "%", "times": 100},
        "management modes of battery charging and discharging": {"address": [0x9070], "description": "voltage compensation: 0, SOC: 1", "unit": "%", "times": 100}
    },
    "coils":
    {
        "manual control the load": {"address": [0x2], "description": "when the load is manual mode，1: manual on, 0: manual off"},
        "enable load test mode": {"address": [0x5], "description": "1: enable, 0: disable (normal)"},
        "force the load on/off": {"address": [0x6], "description": "when the load is manual mode，1: manual on, 0: manual off"}
    },
    "discrete input":
    {
        "over temperature inside the device": {"address": [0x2000], "description": "1: temperature inside the controller is higher than over-temperature protection point, 0: Normal"},
        "day/night": {"address": [0x200C], "description": "1: night, 0: day"},
    }
}

# for k in variables:
#     print("="*100)
#     print(k+":")
#     for i in variables[k]:
#         if len(variables[k][i]['description']):
#             print(f"{' '*5}{i:.<60}{variables[k][i]['description']}")
#         else:
#             print(f"{' '*5}{i}")
