import pandas as pd
import matplotlib.pyplot as plt
import numpy as np




class identificaParametros():
    def __init__(self, dados):
        data = pd.read_csv(f'Python\\Dados\\{dados}.csv', sep=';')

        valor_inicial = sum(data['Velocidade'][:5000])/len(data['Velocidade'][:5000])
        valor_final = sum(data['Velocidade'][8000:])/len(data['Velocidade'][8000:])
        print(f'Valor final: {valor_final}')

        valor_tau = valor_inicial + ((valor_final - valor_inicial)*0.632)
        indice_tau = 0
        for i in range(len(data['Velocidade'])):
            # if data[len(data['Velocidade']) - 1 - i] > valor_final*1.02 or data[len(data['Velocidade']) - 1 - i] < valor_final*0.98:
            #     indice_tau = len(data['Velocidade']) - i
            #     break

            if data['Velocidade'][len(data['Velocidade']) - i - 1] > valor_final*1.02 or data['Velocidade'][len(data['Velocidade']) - i - 1] < valor_final*0.98:
                print(len(data['Velocidade']) - i - 1)
                indice_tau = len(data['Velocidade']) - 1 - i
                tau = (indice_tau/5000) - 5
                break

        print(indice_tau) 






        

if __name__ == '__main__':
    data = 'dados'
    teste = identificaParametros(data)