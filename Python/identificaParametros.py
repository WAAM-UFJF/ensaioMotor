import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
import control as ctl
from control.matlab import *



class identificaParametros():
    def __init__(self, dados):
        data = pd.read_csv(f'Python\\Dados\\{dados}.csv', sep=';')

        valor_inicial = sum(data['Velocidade'][:int(len(data['Velocidade'])/2)])/len(data['Velocidade'][:int(len(data['Velocidade'])/2)])
        valor_final = sum(data['Velocidade'][int(4*len(data['Velocidade'])/5):])/len(data['Velocidade'][int(4*len(data['Velocidade'])/5):])
        print(f'Valor final: {valor_final}')

        for i in range(len(data['Velocidade'])):
            if data['Velocidade'][len(data['Velocidade']) - i - 1] > valor_final*1.02 or data['Velocidade'][len(data['Velocidade']) - i - 1] < valor_final*0.98:
                print(len(data['Velocidade']) - i - 1)
                tempo_acomodacao = len(data['Velocidade']) - i - 1   # Tempo de acomodação para 2%
                print(f'tempo_acomodacao: {tempo_acomodacao}')
                tau = (tempo_acomodacao/1000 - 5)/4
                break

        print(tau) 


        K = (valor_final - valor_inicial)/(11.04*(180/255) - 11.04*(154/255))
        sigma = 1/tau
        Mp  = (data['Velocidade'][int(data['Velocidade'][5000:tempo_acomodacao].argmax())]  - valor_final) / valor_final
        print(Mp)
        #print(f"Mp: {data['Velocidade'][5000 + int(data['Velocidade'][5000:tempo_acomodacao].argmax())] }")
        #qsi = abs(np.log(Mp) / sqrt(np.log(Mp)**2 + np.pi**2))
        qsi = 1

        print(Mp)
        print(f'Qsi: {qsi}')
        Wn = sigma/qsi
        print(Wn)


        t_aux = [0, 5]
        v_aux = [0, 0]
        u = (11.04*(180/255) - 11.04*(154/255)) * np.ones(5000)
        fig_width_cm = 24
        fig_height_cm = 18



        G_teste = tf([K*Wn**2], [1, 2*qsi*Wn, Wn**2])
        t_teste, yout_teste = ctl.forced_response(G_teste, np.linspace(0,5,5000), u)
        t_teste = t_teste + 5
        t_teste = np.array([*t_aux, *t_teste])
        print(t_teste)
        yout_teste = np.array([*v_aux, *yout_teste])
        plt.figure(figsize =  (fig_width_cm /2.54 , fig_height_cm /2.54))
        plt.subplot(2, 1, 1)
        plt.plot(data['Tempo'], data['Velocidade'], color = 'tab:blue', label = 'Ensaio')
        plt.plot(t_teste,valor_inicial + yout_teste, color = 'tab:orange', label = 'Identificado')
        plt.grid()
        plt.legend(loc = 'upper left')
        plt.xlim([4, 6])
        plt.ylabel('Velocidade [rad/s]')
        # plt.xticks(fontsize = 14)
        # plt.yticks(fontsize = 14)
        plt.title('Modelagem de segunda ordem')

        plt.subplot(2,1, 2)
        tensao_inicial = 11.04*(154/255) * np.ones(5001)
        tensao_final = 11.04*(180/255) * np.ones(5000)
        tensao = [*tensao_inicial, *tensao_final]
        plt.plot(data['Tempo'], tensao, color = 'tab:green', label = 'Tensão de Entrada')
        plt.xlim([4, 6])
        plt.xlabel('Tempo [s]')
        plt.ylabel('Tensão [V]')
        plt.legend(loc = 'upper left')
        plt.grid()

        plt.savefig('Python\\Dados\\modelagem2ordem.pdf', bbox_inches = 'tight')
        plt.show()

        print(G_teste)








        

if __name__ == '__main__':
    data = 'dados'
    teste = identificaParametros(data)