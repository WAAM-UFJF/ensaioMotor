import serial
from time import sleep, time
import sys
import json
import pandas as pd
from plotTempoReal import plotTempoReal


COM = 'COM6'# /dev/ttyACM0 (Linux)
BAUD = 115200

ser = serial.Serial(COM, BAUD, timeout = .1)

print('Waiting for device');
sleep(3)
print(ser.name)

#check args
if("-m" in sys.argv or "--monitor" in sys.argv):
	monitor = True
else:
	monitor= False

start = time()
graficos = plotTempoReal()
while True:
    text = ser.readline().decode("utf-8")
    if(text != ""):
        data = json.loads(text)
        data["Tempo"] = time() - start
        print(data)
        print(type(data["Corrente"]))
        graficos.plot(data)
        graficos.ani.resume()