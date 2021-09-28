import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# plt.style.use('fivethirtyeight')
# x_vals = []
# y_vals = []

# index = count()

# def animate(i):
#     x_vals.append(next(index))
#     y_vals.append(random.randint(0, 5))
#     plt.cla()
#     plt.plot(x_vals, y_vals)



# ani = FuncAnimation(plt.gcf(), animate, interval = 1000)

# plt.tight_layout()
# plt.show()

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

    
    def plot(self, data):
        self.dados = data
        plt.figure(figsize = (2560/96, 1080/96))
        plt.style.use('fivethirtyeight')
        self.ani = FuncAnimation(plt.gcf(), self.animate, interval = 1000)
        plt.tight_layout()
        plt.show()
        
    def animate(self, i):
        plt.plot(self.dados['Tempo'], self.dados["Corrente"])
        plt.cla()
    

    