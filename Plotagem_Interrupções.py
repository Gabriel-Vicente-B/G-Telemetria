import matplotlib.pyplot as plt
import numpy as np
from numba import njit
import Criação_Planilha
import re

@njit
def calcular_percentual_variacao(tensao,freq_amostragem):
    tempo_por_amostra=1/freq_amostragem
    cont=0
    i=1
    for i in range(len(tensao)):
        if tensao[i-1]==0 and tensao[i]==0:
            cont+=1

        tempo_interrupção=cont*tempo_por_amostra
    return tempo_interrupção
           
    
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

def Interrupção(tempo, taxa_amostragem,guardar_dados):
    tempo_de_coleta = tempo
    num_linha = 3 # 40k de amostras ou seja 1s para 1 mim num_linha=180 p/ 1 hr num_linha=10800  o numero de amostra será 108000*10k
    cont = 0
    cont_coleta = 0
    Interrupção_A, Interrupção_B, Interrupção_C = [], [], []

    while True:
        Tensão_A_aux = ler_arq('Tensão_A.txt', cont, num_linha)
        Tensão_B_aux = ler_arq('Tensão_B.txt', cont, num_linha)
        Tensão_C_aux = ler_arq('Tensão_C.txt', cont, num_linha)

        if Tensão_A_aux.size > 0:
            val_aux = calcular_percentual_variacao(Tensão_A_aux,taxa_amostragem)
            Interrupção_A.append(val_aux)
        
        if Tensão_B_aux.size > 0:
            val_aux = calcular_percentual_variacao(Tensão_B_aux,taxa_amostragem)
            Interrupção_B.append(val_aux)
        
        if Tensão_C_aux.size > 0:
            val_aux = calcular_percentual_variacao(Tensão_C_aux,taxa_amostragem)
            Interrupção_C.append(val_aux)
        
        cont_coleta += 1
        cont += num_linha
        if cont_coleta == tempo_de_coleta:
            break
    
    if guardar_dados==True:
        Criação_Planilha.armazenar_excel(Interrupção_A,'Dados_Analisador.xlsx','Interrupção','A')
        Criação_Planilha.armazenar_excel(Interrupção_B,'Dados_Analisador.xlsx','Interrupção','B')
        Criação_Planilha.armazenar_excel(Interrupção_C,'Dados_Analisador.xlsx','Interrupção','C')


    eixo_x_A = np.arange(len(Interrupção_A))
    eixo_x_B = np.arange(len(Interrupção_B))
    eixo_x_C = np.arange(len(Interrupção_C))
    
    plt.style.use('classic')
    plt.subplot(3, 1, 1)
    plt.title('Interrupção na Tensão FASE A')
    plt.ylabel('Tempo de interrupção (s)')
    plt.xlabel('Tempo (s)')
    plt.bar(eixo_x_A, Interrupção_A)
    plt.grid()
    plt.tight_layout()
    plt.subplot(3, 1, 2)
    plt.title('Interrupção na Tensão FASE B')
    plt.ylabel('Tempo de interrupção (s)')
    plt.xlabel('Tempo (s)')
    plt.bar(eixo_x_B, Interrupção_B)
    plt.grid()
    plt.tight_layout()
    plt.subplot(3, 1, 3)
    plt.title('Interrupção na Tensão FASE C')
    plt.ylabel('Tempo de interrupção (s)')
    plt.xlabel('Tempo (s)')
    plt.bar(eixo_x_C, Interrupção_C)
    plt.grid()
    plt.tight_layout()
    plt.show()

