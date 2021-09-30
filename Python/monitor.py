# import serial as sr
# import matplotlib.pyplot as plt
# import numpy as np

# COM = 'COM6'# /dev/ttyACM0 (Linux)
# BAUD = 115200

# ser = sr.Serial(COM, BAUD, timeout = .1)
# # plt.close("all")
# # plt.figure()
# # plt.ion()
# # plt.show()

# data = np.array([])

# while True:
#     print("Entrei no While!")
#     msg = ser.readline().decode("utf-8")
#     print("Recebi a mensage,!")
#     data = np.append(data, msg)
#     print(data)
#     # plt.cla()
#     # plt.plot(data)
#     # plt.pause(0.01)


import serial
from time import sleep, time
import sys
import json
import pandas as pd
from plotTempoReal import plotTempoReal
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x = []
y = []

def animate(i):
    text = ser.readline().decode("utf-8")
    print(text)
    if(text != ""):
        try:
            data = eval(text)
            data["Tempo"] = time() - start
            print(data)
            x.append(data["Tempo"])
            y.append(data["Corrente"])
            plt.cla()
            plt.plot(x, y, label = 'Corrente')
            plt.legend(loc='upper right', fontsize = 20)
            # tfinal = time()
            # print(f'Tempo total {tfinal - tstart}')
            plt.tight_layout()
        except:
            print("Erro")
        
        
        

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
# graficos = plotTempoReal()



plt.figure(figsize = (2560/96, 1080/96))
plt.style.use('fivethirtyeight')
ani = FuncAnimation(plt.gcf(), animate, interval = 1000)
plt.show()