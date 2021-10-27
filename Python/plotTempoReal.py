import matplotlib.pyplot as plt


class plotTempoReal():
    """
    Classe para realizar o plot em tempo real
    """
    def __init__(self):
        """
        Construtor da classe plotTempoReal
        """
        print("Plot em tempo real inicializado")
        self._tamJanela = 20
        self._tempo = [-0.01*i for i in range(0,100*self._tamJanela + 1)]

    
    def plot(self, tempo, corrente):
        """
        Método que realiza o plot dos dados.
        :param tempo: lista com os valores de tempo
        :param corrente: lista com os valores de corrente
        """
        plt.cla()
        if len(corrente) < len(self._tempo):
            try:
                plt.plot(self._tempo[:len(corrente)], list(reversed(corrente)), linewidth = 3, color = 'tab:blue', label = "Corrente")
            except:
                print("Erro ao tentar realizar o plot com dados incompletos!")
        else:
            try:
                plt.plot(self._tempo, list(reversed(corrente)), linewidth = 3, color = 'tab:blue')
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
        
    def trataDados(self, ser, velocidade, corrente):
        """
        Método que reliza o recebimento e tratamento dos dados
        :param ser: variavel de conexão, do tipo serial.serial
        :param velocidade: vetor com os valores de velocidade
        :param corrente: veotr com os valores de corrente
        """
        self._corrente = corrente
        self._velocidade = velocidade
        try:
            dados = ser.read(ser.inWaiting()).decode('utf-8')
        except:
            print("Erro ao decodificar os dados!")
        if dados != "":
            try:
                dados = dados.split('\r\n')
                dados.pop()
                dados.pop(0)
                try:
                    for data in dados:
                        self._velocidadeAux, self._correnteAux = data.split(';')
                        self._corrente.append(float(self._correnteAux))
                        self._velocidade.append(float(self._velocidadeAux))
                        if len(self._velocidade) > len(self._tempo):
                            self._corrente.pop(0)
                            self._velocidade.pop(0)
                except:
                    print("Falha ao separar dados!")
                    print(f'Dados recebidos: {dados}')                    
            except:
                print("Erro ao tentar receber dados!")

        return self._velocidade, self._corrente

    

    