import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from math import sqrt
import control as ctl
from control.matlab import *



class identificaParametros():
    def __init__(self, dados):
        self._t_aux = np.linspace(0,5,5001)
        self._v_aux = 0*np.linspace(0,5,5001)
        self._u = (180 - 154) * np.ones(5000)
        self._fig_width_cm = 24
        self._fig_height_cm = 18
        self._data = pd.read_csv(f'Python\\Dados\\{dados}.csv', sep=';')
        self._valor_inicial = sum(self._data['Velocidade'][:int(len(self._data['Velocidade'])/2)])/len(self._data['Velocidade'][:int(len(self._data['Velocidade'])/2)])
        self._valor_final = sum(self._data['Velocidade'][int(4*len(self._data['Velocidade'])/5):])/len(self._data['Velocidade'][int(4*len(self._data['Velocidade'])/5):])
        self._K = (self._valor_final - self._valor_inicial)/(180 - 154)
        self._calculaTempoAcomodacao()
        self._primeiraOrdem()
        self._segundaOrdem()
        

    def _calculaTempoAcomodacao(self):
        for i in range(len(self._data['Velocidade'])):
            if self._data['Velocidade'][len(self._data['Velocidade']) - i - 1] > self._valor_final*1.02 or self._data['Velocidade'][len(self._data['Velocidade']) - i - 1] < self._valor_final*0.98:
                self._tempo_acomodacao = len(self._data['Velocidade']) - i - 1   # Tempo de acomodação para 2%
                self._tau = (self._tempo_acomodacao/1000 - 5)/4
                break

    
    def _primeiraOrdem(self):
        self._G1 = tf([self._K], [self._tau, 1])
        
        self._t1, self._yout1 = ctl.forced_response(self._G1, np.linspace(0,5,5000), self._u)
        self._t1 = self._t1 + 5
        self._t1 = np.array([*self._t_aux, *self._t1])
        self._yout1 = np.array([*self._v_aux, *self._yout1])

        # Figura primeira ordem
        plt.figure(2, figsize =  (self._fig_width_cm /2.54 , self._fig_height_cm /2.54))
        plt.subplot(2, 1, 1)
        plt.plot(self._data['Tempo'], self._data['Velocidade'], color = 'tab:blue', label = 'Ensaio')
        plt.plot(self._t1,self._valor_inicial + self._yout1, color = 'tab:orange', label = 'Identificado')
        plt.grid()
        plt.legend(loc = 'upper left')
        plt.xlim([0, 10])
        plt.ylabel('Velocidade [rad/s]')
        plt.title('Modelagem de primeira ordem')

        plt.subplot(2,1, 2)
        tensao_inicial = 154 * np.ones(5001)
        tensao_final = 180 * np.ones(5000)
        self._tensao1 = [*tensao_inicial, *tensao_final]
        plt.plot(self._data['Tempo'], self._tensao1 , color = 'tab:green', label = 'Razão Cíclica')
        plt.xlim([0, 10])
        plt.xlabel('Tempo [s]')
        plt.ylabel('Razão Cíclica [0-255]')
        plt.legend(loc = 'upper left')
        plt.grid()
        plt.savefig('Python\\Dados\\Figuras\\modelagem1ordem.pdf', bbox_inches = 'tight')

        # Figura primeira ordem detalhado
        plt.figure(3, figsize =  (self._fig_width_cm /2.54 , self._fig_height_cm /2.54))
        plt.subplot(2, 1, 1)
        plt.plot(self._data['Tempo'], self._data['Velocidade'], color = 'tab:blue', label = 'Ensaio')
        plt.plot(self._t1,self._valor_inicial + self._yout1, color = 'tab:orange', label = 'Identificado')
        plt.grid()
        plt.legend(loc = 'upper left')
        plt.xlim([4, 6])
        plt.ylabel('Velocidade [rad/s]')
        plt.title('Modelagem de primeira ordem')

        plt.subplot(2,1, 2)
        plt.plot(self._data['Tempo'], abs(self._data['Velocidade'] - (self._valor_inicial+self._yout1))/self._data['Velocidade']*100, color = 'tab:green', label = 'Erro relativo')
        plt.xlim([4, 6])
        plt.xlabel('Tempo [s]')
        plt.ylabel('Erro [%]')
        plt.legend(loc = 'upper left')
        plt.grid()

        plt.savefig('Python\\Dados\\Figuras\\modelagem1ordemDetalhado.pdf', bbox_inches = 'tight')
        plt.close(2)
        plt.close(3)

        print('-------------------------------------------------')
        print('------------ Parametros primeira ordem -----------')        
        print(f'K: {self._K}')
        print(f'Tau: {self._tau}')
        print('------------ Funcao de Transferencia ------------')
        print(self._G1)
        print('-------------------------------------------------')


    def _segundaOrdem(self):
        self._sigma = 1/self._tau
        self._Mp  = (self._data['Velocidade'][int(self._data['Velocidade'][5000:self._tempo_acomodacao].argmax())]  - self._valor_final) / self._valor_final
        if self._Mp > 0:
            self._qsi = abs(np.log(self._Mp) / sqrt(np.log(self._Mp)**2 + np.pi**2))
        else:
            self._qsi = 1
        self._Wn = self._sigma/self._qsi

        self._G = tf([self._K*self._Wn**2], [1, 2*self._qsi*self._Wn, self._Wn**2])
        self._t, self._yout = ctl.forced_response(self._G, np.linspace(0,5,5000), self._u)
        self._t = self._t + 5
        self._t = np.array([*self._t_aux, *self._t])
        self._yout = np.array([*self._v_aux, *self._yout])

        # Figura segunda ordem
        plt.figure(4, figsize =  (self._fig_width_cm /2.54 , self._fig_height_cm /2.54))
        plt.subplot(2, 1, 1)
        plt.plot(self._data['Tempo'], self._data['Velocidade'], color = 'tab:blue', label = 'Ensaio')
        plt.plot(self._t,self._valor_inicial + self._yout, color = 'tab:orange', label = 'Identificado')
        plt.grid()
        plt.legend(loc = 'upper left')
        plt.xlim([0, 10])
        plt.ylabel('Velocidade [rad/s]')
        plt.title('Modelagem de segunda ordem')

        plt.subplot(2,1, 2)
        self._tensao_inicial = 154 * np.ones(5001)
        self._tensao_final = 180 * np.ones(5000)
        self._tensao = [*self._tensao_inicial, *self._tensao_final]
        plt.plot(self._data['Tempo'], self._tensao, color = 'tab:green', label = 'Razão Cíclica')
        plt.xlim([0, 10])
        plt.xlabel('Tempo [s]')
        plt.ylabel('Razão Cíclica [0-255]')
        plt.legend(loc = 'upper left')
        plt.grid()

        plt.savefig('Python\\Dados\\Figuras\\modelagem2ordem.pdf', bbox_inches = 'tight')


        # Figura segunda ordem detalhada
        plt.figure(5, figsize =  (self._fig_width_cm /2.54 , self._fig_height_cm /2.54))
        plt.subplot(2, 1, 1)
        plt.plot(self._data['Tempo'], self._data['Velocidade'], color = 'tab:blue', label = 'Ensaio')
        plt.plot(self._t,self._valor_inicial + self._yout, color = 'tab:orange', label = 'Identificado')
        plt.grid()
        plt.legend(loc = 'upper left')
        plt.xlim([4, 6])
        plt.ylabel('Velocidade [rad/s]')
        plt.title('Modelagem de segunda ordem')

        plt.subplot(2,1, 2)
        plt.plot(self._data['Tempo'], abs(self._data['Velocidade'] - (self._valor_inicial+self._yout))/self._data['Velocidade']*100, color = 'tab:green', label = 'Erro relativo')
        plt.xlim([4, 6])
        plt.xlabel('Tempo [s]')
        plt.ylabel('Erro [%]')
        plt.legend(loc = 'upper left')
        plt.grid()


        plt.savefig('Python\\Dados\\Figuras\\modelagem2ordemDetalhado.pdf', bbox_inches = 'tight')
        plt.close(4)
        plt.close(5)
        print('-------------------------------------------------')
        print('------------ Parametros segunda ordem -----------')        
        print(f'K: {self._K}')
        print(f'Qsi: {self._qsi}')
        print(f'Wn: {self._Wn}')
        print('------------ Funcao de Transferencia ------------')
        print(self._G)
        print('-------------------------------------------------')







        

if __name__ == '__main__':
    data = 'Jan-15-2022--19-17-53'
    teste = identificaParametros(data)