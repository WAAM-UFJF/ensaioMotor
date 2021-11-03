import serial
from time import time, sleep
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from plotTempoReal import plotTempoReal

a = [0]
atualizaGrafico = [0]


def animate(i):
    if a[0] == 0:
        a[0] = 1
        global velocidade
        global corrente
        velocidade = []
        corrente = []
    velocidade, corrente = graph.trataDados(ser, velocidade, corrente)
    graph.plot(velocidade,corrente)
      

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

# plt.figure(figsize = (1920/96, 1080/96))
# plt.xlabel("Tempo [ms]")
# plt.ylabel("Corrente [mA]")
# plt.style.use('fivethirtyeight')
fig, axs = plt.subplots(2, figsize = (2560/96, 1080/96))
fig.suptitle("Valores do motor")
graph = plotTempoReal(figura = fig, eixos = axs)
ani = FuncAnimation(plt.gcf(), animate, interval = 200)
plt.show()