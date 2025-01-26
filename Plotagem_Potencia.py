import matplotlib.pyplot as plt
import numpy as np
from numba import njit
import Criação_Planilha
import re

@njit
def calcular_rms_e_fp(tensao, corrente, fp):
    V_rms = np.sqrt(np.mean(tensao ** 2))
    I_rms = np.sqrt(np.mean(corrente ** 2))
    FP_medio = np.mean(fp)
    Theta = np.arccos(FP_medio)
    P_VA = V_rms * I_rms
    P_W = P_VA * np.cos(Theta)
    P_VAR = P_VA * np.sin(Theta)
    return P_VA, P_W, P_VAR, FP_medio,V_rms,I_rms


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

        
def Plotar_Potencias(tempo,guardar_dados):
    tempo_de_coleta = tempo
    num_linha = 3
    cont = 0
    cont_coleta = 0

    P_VA_A, P_VA_B, P_VA_C = [], [], []
    P_W_A, P_W_B, P_W_C = [], [], []
    P_FP_A, P_FP_B, P_FP_C = [], [], []
    P_VAR_A, P_VAR_B, P_VAR_C = [], [], []

    V_RMS_A,V_RMS_B,V_RMS_C= [], [], []
    I_RMS_A,I_RMS_B,I_RMS_C= [], [], [] 

    while True:
        Tensão_A_aux = ler_arq('Tensão_A.txt', cont, num_linha)
        Corrente_A_aux = ler_arq('Corrente_A.txt', cont, num_linha)
        FP_A_aux = ler_arq('FP_A.txt', cont, num_linha)
        Tensão_B_aux = ler_arq('Tensão_B.txt', cont, num_linha)
        Corrente_B_aux = ler_arq('Corrente_B.txt', cont, num_linha)
        FP_B_aux = ler_arq('FP_B.txt', cont, num_linha)
        Tensão_C_aux = ler_arq('Tensão_C.txt', cont, num_linha)
        Corrente_C_aux = ler_arq('Corrente_C.txt', cont, num_linha)
        FP_C_aux = ler_arq('FP_C.txt', cont, num_linha)

        if Tensão_A_aux.size > 0 and Corrente_A_aux.size > 0 and FP_A_aux.size > 0:
            P_VA_A_value, P_W_A_value, P_VAR_A_value, FP_medio_A,V_RMS_A_value,I_RMS_A_Value = calcular_rms_e_fp(Tensão_A_aux, Corrente_A_aux, FP_A_aux)
            P_VA_A.append(P_VA_A_value)
            P_W_A.append(P_W_A_value)
            P_VAR_A.append(P_VAR_A_value)
            P_FP_A.append(FP_medio_A)
            V_RMS_A.append(V_RMS_A_value)
            I_RMS_A.append(I_RMS_A_Value)

        if Tensão_B_aux.size > 0 and Corrente_B_aux.size > 0 and FP_B_aux.size > 0:
            P_VA_B_value, P_W_B_value, P_VAR_B_value, FP_medio_B,V_RMS_B_value,I_RMS_B_Value = calcular_rms_e_fp(Tensão_B_aux, Corrente_B_aux, FP_B_aux)
            P_VA_B.append(P_VA_B_value)
            P_W_B.append(P_W_B_value)
            P_VAR_B.append(P_VAR_B_value)
            P_FP_B.append(FP_medio_B)
            V_RMS_B.append(V_RMS_B_value)
            I_RMS_B.append(I_RMS_B_Value)

        if Tensão_C_aux.size > 0 and Corrente_C_aux.size > 0 and FP_C_aux.size > 0:
            P_VA_C_value, P_W_C_value, P_VAR_C_value, FP_medio_C,V_RMS_C_value,I_RMS_C_Value = calcular_rms_e_fp(Tensão_C_aux, Corrente_C_aux, FP_C_aux)
            P_VA_C.append(P_VA_C_value)
            P_W_C.append(P_W_C_value)
            P_VAR_C.append(P_VAR_C_value)
            P_FP_C.append(FP_medio_C)
            V_RMS_C.append(V_RMS_C_value)
            I_RMS_C.append(I_RMS_C_Value)
        cont_coleta += 1
        cont += num_linha
        if cont_coleta == tempo_de_coleta:
            break

    if guardar_dados==True:
        Criação_Planilha.armazenar_excel(P_VA_A,'Dados_Analisador.xlsx','Potencia','A')
        Criação_Planilha.armazenar_excel(P_VA_B,'Dados_Analisador.xlsx','Potencia','B')
        Criação_Planilha.armazenar_excel(P_VA_C,'Dados_Analisador.xlsx','Potencia','C')
        Criação_Planilha.armazenar_excel(P_W_A,'Dados_Analisador.xlsx','Potencia','D')
        Criação_Planilha.armazenar_excel(P_W_B,'Dados_Analisador.xlsx','Potencia','E')
        Criação_Planilha.armazenar_excel(P_W_C,'Dados_Analisador.xlsx','Potencia','F')
        Criação_Planilha.armazenar_excel(P_VAR_A,'Dados_Analisador.xlsx','Potencia','G')
        Criação_Planilha.armazenar_excel(P_VAR_B,'Dados_Analisador.xlsx','Potencia','H')
        Criação_Planilha.armazenar_excel(P_VAR_C,'Dados_Analisador.xlsx','Potencia','I')
        Criação_Planilha.armazenar_excel(V_RMS_A,'Dados_Analisador.xlsx','Grandezas','A')
        Criação_Planilha.armazenar_excel(V_RMS_B,'Dados_Analisador.xlsx','Grandezas','B')
        Criação_Planilha.armazenar_excel(V_RMS_C,'Dados_Analisador.xlsx','Grandezas','C')
        Criação_Planilha.armazenar_excel(I_RMS_A,'Dados_Analisador.xlsx','Grandezas','D')
        Criação_Planilha.armazenar_excel(I_RMS_B,'Dados_Analisador.xlsx','Grandezas','E')
        Criação_Planilha.armazenar_excel(I_RMS_C,'Dados_Analisador.xlsx','Grandezas','F')
        Criação_Planilha.armazenar_excel(P_FP_A,'Dados_Analisador.xlsx','Grandezas','G')
        Criação_Planilha.armazenar_excel(P_FP_B,'Dados_Analisador.xlsx','Grandezas','H')
        Criação_Planilha.armazenar_excel(P_FP_C,'Dados_Analisador.xlsx','Grandezas','I') 

    plt.style.use('classic')
    plt.subplot(3, 2, 1)
    plt.title('Potencia FASE A')
    plt.ylabel('Potencia')
    plt.xlabel('Tempo (s)')
    plt.plot(P_VA_A, color='m', label='Potencia Aparente')
    plt.plot(P_W_A, color='g', label='Potencia Ativa')
    plt.plot(P_VAR_A, color='r', label='Potencia Reativa')
    plt.legend()
    plt.grid()
    plt.subplot(3, 2, 3)
    plt.title('Potencia FASE B')
    plt.ylabel('Potencia')
    plt.xlabel('Tempo (s)')
    plt.plot(P_VA_B, color='m', label='Potencia Aparente')
    plt.plot(P_W_B, color='g', label='Potencia Ativa')
    plt.plot(P_VAR_B, color='r', label='Potencia Reativa')
    plt.legend()
    plt.grid()
    plt.subplot(3, 2, 5)
    plt.title('Potencia FASE C')
    plt.ylabel('Potencia')
    plt.xlabel('Tempo (s)')
    plt.plot(P_VA_C, color='m', label='Potencia Aparente')
    plt.plot(P_W_C, color='g', label='Potencia Ativa')
    plt.plot(P_VAR_C, color='r', label='Potencia Reativa')
    plt.legend()
    plt.grid()
    plt.subplot(3, 2, 2)
    plt.title('FP FASE A')
    plt.ylim(0,1)
    plt.ylabel('FP')
    plt.xlabel('Tempo (s)')
    plt.plot(P_FP_A, color='y', label='Fp')
    plt.axhline(y=0.92, color='b', label='Fp de Referencia')
    plt.legend()
    plt.grid()
    plt.subplot(3, 2, 4)
    plt.title('FP FASE B')
    plt.ylim(0,1)
    plt.ylabel('FP')
    plt.xlabel('Tempo (s)')
    plt.plot(P_FP_B, color='y', label='Fp')
    plt.axhline(y=0.92, color='b', label='Fp de Referencia')
    plt.legend()
    plt.grid()
    plt.subplot(3, 2, 6)
    plt.title('FP FASE C')
    plt.ylim(0,1)
    plt.ylabel('FP')
    plt.xlabel('Tempo (s)')
    plt.plot(P_FP_C, color='y', label='Fp')
    plt.axhline(y=0.92, color='b', label='Fp de Referencia')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()
