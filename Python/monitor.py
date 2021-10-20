import serial
from time import sleep
import sys
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

x = []
y = []
erros = [0]

def animate(i):
    # TrataDados(ser)

    try:
        text = ser.read(ser.inWaiting())
        print(text)
        if text != "":
            try:
                #print(text)
                text= text.split('\r\n')
                tempo, corrente = text[0].split(';')
                x.append(float(tempo))
                y.append(float(corrente))
                plt.cla()
                plt.plot(x, y, label = 'Corrente')
                plt.legend(loc='upper right', fontsize = 20)
                plt.tight_layout()
            except:
                #print(text)
                print(f'Erro ao tentar atualizar dados.')
                erros[0] += 1
                print(f'Numero de erros: {erros}')
    except:
        print("Erro ao receber dados!")

        
        
        

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
ani = FuncAnimation(plt.gcf(), animate, interval = .01)
plt.show()

