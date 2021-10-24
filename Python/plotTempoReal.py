import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class plotTempoReal():
    """
    Classe para realizar o plot em tempo real
    """
    def __init__(self):
        """
        Construtor da classe plotTempoReal
        :param data: dicionario com os dados a serem plotados
        """
        print("Plot em tempo real inicializado")
        self._tamJanela = 10
        self._tempo = [0.01*i for i in range(0,1001)]

    
    def plot(self, tempo, corrente):
        """
        Método que realiza o plot dos dados.
        :param tempo: lista com os valores de tempo
        :param corrente: lista com os valores de corrente
        """
        plt.cla()
        if len(corrente) < len(self._tempo):
            try:
                plt.plot(self._tempo[:len(corrente)], corrente, linewidth = 3, color = 'tab:blue', label = "Corrente")
            except:
                print("Erro ao tentar realizar o plot com dados incompletos!")
        else:
            try:
                plt.plot(self._tempo, corrente, linewidth = 3, color = 'tab:blue', label = "Corrente")
            except:
                print("Erro ao tentar realizar o plot com dados completos!")
        try:            
            plt.xlim([-1*self._tamJanela, 0])
            plt.xticks([i for i in range(-1*self._tamJanela, 1)])            
            plt.xlabel("Tempo [ms]")
            plt.ylabel("Corrente [mA]")
            plt.plot(tempo, corrente, label = 'Corrente')
            plt.legend(loc='upper right', fontsize = 20)
            plt.tight_layout()
        except:
            print("Erro ao tentar traçar o grafico!")
        
    def trataDados(self, ser):
        """
        Método que reliza o recebimento e tratamento dos dados
        :param ser: variavel de conexão, do tipo serial.serial
        """
        self._corrente = []
        self._tempo = []
        dados = ser.read(ser.inWaiting()).decode('utf-8')
        if dados != "":
            try:
                dados = dados.split('\r\n')
                dados.pop()
                dados.pop(0)
                try:
                    for data in dados:
                        self._tempoAux, self._correnteAux = data.split(';')
                        self._corrente.append(float(self._correnteAux))
                        self._tempo.append(float(self._tempoAux))
                except:
                    print("Falha ao separar dados!")
                    print(f'Dados recebidos: {dados}')                    
            except:
                print("Erro ao tentar receber dados!")

        return self._tempo, self._corrente

    

    