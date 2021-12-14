import pandas as pd
import matplotlib.pyplot as plt
import numpy as np




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

        sigma = 1/tau







        

if __name__ == '__main__':
    data = 'dados'
    teste = identificaParametros(data)