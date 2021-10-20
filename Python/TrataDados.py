import serial

dados = b'242226.00;45.98\r\n242234.00;50.50\r\n242242.00;53.18\r\n242250.00;46.16\r\n242258.00;48.42\r\n242266.00;54.88\r\n242274.00;48.32\r\n242282.00;51.50\r\n242290.00;53'
print(dados)
print(type(dados))
dados = dados.decode('utf-8')
print(dados)
print(type(dados))

dados = dados.split('\r\n')
print(dados)
type(dados)

corrente = []
tempo = []

for data in dados:
    tempoAux, correnteAux = data.split(';')
    corrente.append(correnteAux)
    tempo.append(tempoAux)

print(f'Tempo: {tempo}          Corrente: {corrente}')

try:
    text = ser.read(ser.InWai)
except:
    print("Só pra tirar o erro")


class TrataDados():
    """
    Classe para tratar os dados e plotar os graficos em tempo real
    """
    def __init__(self):
        """
        Construtor da classe TrataDados
        """
    
    def trataDados(self, ser):
        dados = ser.read(ser.inWaiting()).decode('utf-8')
        if dados != "":
            try:
                dados = dados.split('\r\n')
                try:
                    for data in dados:
                        tempoAux, correnteAux = data.split(';')
                        corrente.append(correnteAux)
                        tempo.append(tempoAux)
                except:
                    print("Falha ao separar dados!")
            except:
                print("Erro ao tentar receber dados!")

        return tempo, corrente
