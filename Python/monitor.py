import serial
from time import sleep
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x = []
y = []
erros = [0]

# def animate(i):
#     text = ser.readline().decode("utf-8")
#     print(text)
#     if(text != ""):
#         try:
#             data = eval(text)
#             print(data)
#             x.append(data["Tempo"])
#             y.append(data["Corrente"])
#             plt.cla()
#             plt.plot(x, y, label = 'Corrente')
#             plt.legend(loc='upper right', fontsize = 20)
#             plt.tight_layout()
#         except:
#             data = text.split('}')
#             data.pop()
#             data = [data[i] + '}' for i in range(len(data))]
#             for dicts in data:
#                 dicts = eval(dicts)
#                 x.append(dicts["Tempo"])
#                 y.append(dicts["Corrente"])
#                 plt.cla()
#                 plt.plot(x, y, label = 'Corrente')
#                 plt.legend(loc='upper right', fontsize = 20)
#                 plt.tight_layout()

def animate(i):
    text = ser.readline().decode("utf-8")
    if text != "":
        try:
            print(text)
            text= text.split('\r\n')
            tempo, corrente = text[0].split(';')
            x.append(float(tempo))
            y.append(float(corrente))
            plt.cla()
            plt.plot(x, y, label = 'Corrente')
            plt.legend(loc='upper right', fontsize = 20)
            plt.tight_layout()
        except:
            print(f'Erro ao tentar atualizar dados.')
            erros[0] += 1
            print(f'Numero de erros: {erros}')

        
        
        

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


plt.figure(figsize = (2560/96, 1080/96))
plt.style.use('fivethirtyeight')
ani = FuncAnimation(plt.gcf(), animate, interval = 2)
plt.show()
# plt.figure(figsize = (2560/96, 1080/96))
# while True:
#     text = ser.readline().decode("utf-8")
#     print(text)
#     text= text.split('\r\n')
#     print(text)
#     tempo, corrente = text[0].split(';')
#     print(tempo)
#     print(corrente)
#     x.append(float(tempo))
#     print(x)
#     y.append(float(corrente))    
#     print(y)
#     plt.cla()
#     plt.plot(x,y, color = 'tab:blue', linewidth = 3, label = 'Corrente')
#     plt.show()
