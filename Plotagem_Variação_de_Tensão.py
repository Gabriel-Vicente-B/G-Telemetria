import matplotlib.pyplot as plt
import numpy as np
from numba import njit
import Criação_Planilha
import re
@njit
def calcular_percentual_variacao(tensao, linha):
    V_rms = np.sqrt(np.mean(tensao**2))
    percentual = round((((V_rms * 100) / linha) - 100), 2)
    return percentual

def ler_arq(arq, cont, num_linha):
    data = []
    with open(arq, 'r') as file:
        for i, linha in enumerate(file):
            if i >= cont:
                linha = linha.strip()  # Remove espaços em branco e quebras de linha no início e no fim
                if linha:  # Verifica se a linha não está vazia
                    # Limpa a linha usando regex para permitir apenas números e pontos
                    linha_limpa = re.sub(r'[^\d.,-]', '', linha)
                    valores = linha_limpa.split(',')
                    try:
                        # Filtra valores vazios e converte para float
                        val_aux = np.array([float(v) for v in valores if v], dtype=float)
                        data.append(val_aux)
                    except ValueError as e:
                        print(f"Erro ao converter linha: {linha} - {e}")
            if i >= num_linha + cont:
                break
    if data:
        return np.concatenate(data)
    else:
        return np.array([])

def Variação_de_tensão(tempo, V_fase,guardar_dados):
    tempo_de_coleta = tempo
    num_linha = 3
    cont = 0
    cont_coleta = 0
    Tensão_Linha = V_fase
    Variação_A, Variação_B, Variação_C = [], [], []

    while True:
        Tensão_A_aux = ler_arq('Tensão_A.txt', cont, num_linha)
        Tensão_B_aux = ler_arq('Tensão_B.txt', cont, num_linha)
        Tensão_C_aux = ler_arq('Tensão_C.txt', cont, num_linha)

        if Tensão_A_aux.size > 0:
            Percentual_A = calcular_percentual_variacao(Tensão_A_aux, Tensão_Linha)
            Variação_A.append(Percentual_A)
        
        if Tensão_B_aux.size > 0:
            Percentual_B = calcular_percentual_variacao(Tensão_B_aux, Tensão_Linha)
            Variação_B.append(Percentual_B)
        
        if Tensão_C_aux.size > 0:
            Percentual_C = calcular_percentual_variacao(Tensão_C_aux, Tensão_Linha)
            Variação_C.append(Percentual_C)

        cont_coleta += 1
        cont += num_linha
        if cont_coleta == tempo_de_coleta:
            break

    eixo_x_A = np.arange(len(Variação_A))
    eixo_x_B = np.arange(len(Variação_B))
    eixo_x_C = np.arange(len(Variação_C))

    if guardar_dados==True:
        Criação_Planilha.armazenar_excel(Variação_A,'Dados_Analisador.xlsx','Variação','A')
        Criação_Planilha.armazenar_excel(Variação_B,'Dados_Analisador.xlsx','Variação','B')
        Criação_Planilha.armazenar_excel(Variação_C,'Dados_Analisador.xlsx','Variação','C')
    plt.style.use('classic')
    plt.subplot(3, 1, 1)
    plt.title('Variação de Tensão A(%)')
    plt.xlabel('Tempo(s)')
    plt.ylabel('(%)')
    plt.axhline(10,c='r')
    plt.axhline(-10,c='r')
    plt.bar(eixo_x_A, Variação_A)
    plt.grid()
    plt.tight_layout()
    plt.subplot(3, 1, 2)
    plt.title('Variação de Tensão B(%)')
    plt.xlabel('Tempo(s)')
    plt.ylabel('(%)')
    plt.axhline(10,c='r')
    plt.axhline(-10,c='r')
    plt.bar(eixo_x_B, Variação_B)
    plt.grid()
    plt.tight_layout()
    plt.subplot(3, 1, 3)
    plt.title('Variação de Tensão C(%)')
    plt.xlabel('Tempo(s)')
    plt.ylabel('(%)')
    plt.axhline(10,c='r')
    plt.axhline(-10,c='r')
    plt.bar(eixo_x_C, Variação_C)
    plt.grid()
    plt.tight_layout()
    plt.show()
