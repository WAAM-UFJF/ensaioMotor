# ensaioMotor
 
## O Software
 Ferramenta computacional para auxiliar na identificação do modelo dinâmico de um motor de corrente continua a partir da análise da curva de resposta transitória a uma entrada do tipo degrau.Desenvolvido em Python, é capaz de monitorar medidas em tempo real do motor e realizar as seguintes tarefas:
 
 1. Aquisição de dados do motor em tempo real:
     * Velocidade
     * Corrente.
 3. Análise detalhada da resposta transitória ao degrau;
 4. Geração de arquivo de dados;
 5. Identificação dos parametros do motor
 6. Determinação da função de transferencia de velocidade do motor em primeira e segunda ordem;
 7. Análise do erro entre as curvas de ensaio e identificada.


## Funcionamento

Para realizar a aquisição de dados, é necessario a montagem de um circuito similar ao demonstrado na imagem.

![](Montagem.pdf)
