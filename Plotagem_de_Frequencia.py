import numpy as np
from scipy.fft import fft, fftfreq
import re
import matplotlib.pyplot as plt
import Criação_Planilha

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
    
def Frequencia(tempo,taxa_amostragem,guardar_dados):
    tempo_de_coleta = tempo
    num_linha = 3 # 40k de amostras ou seja 1s para 1 mim num_linha=180 p/ 1 hr num_linha=10800  o numero de amostra será 108000*10k
    cont = 0
    cont_coleta = 0
    Freq_A, Freq_B, Freq_C = [], [], []

    while True:
        Tensão_A_aux = ler_arq('Tensão_A.txt', cont, num_linha)
        Tensão_B_aux = ler_arq('Tensão_B.txt', cont, num_linha)
        Tensão_C_aux = ler_arq('Tensão_C.txt', cont, num_linha)
        Tensão_A_aux = Tensão_A_aux - np.mean(Tensão_A_aux)
        Tensão_B_aux = Tensão_B_aux - np.mean(Tensão_B_aux)
        Tensão_C_aux = Tensão_C_aux - np.mean(Tensão_C_aux)

        N_V_A = len(Tensão_A_aux)
        N_V_B = len(Tensão_A_aux)
        N_V_C = len(Tensão_A_aux)


        fft_A = fft(Tensão_A_aux)
        fft_B = fft(Tensão_B_aux)
        fft_C = fft(Tensão_C_aux)

        frequencias_A = fftfreq(N_V_A, (1/taxa_amostragem))
        frequencias_B = fftfreq(N_V_B, (1/taxa_amostragem)) 
        frequencias_C = fftfreq(N_V_C, (1/taxa_amostragem))

        mag_V_A = np.abs(fft_A)
        mag_V_B = np.abs(fft_B)
        mag_V_C = np.abs(fft_C)

        Val_max_V_A= np.argmax(mag_V_A[:N_V_A//2])
        Val_max_V_B= np.argmax(mag_V_B[:N_V_B//2])
        Val_max_V_C= np.argmax(mag_V_C[:N_V_C//2])

        Freq_A.append(frequencias_A[Val_max_V_A])
        Freq_B.append(frequencias_B[Val_max_V_B])
        Freq_C.append(frequencias_C[Val_max_V_C])


        cont_coleta += 1
        cont += num_linha
        if cont_coleta == tempo_de_coleta:
            break

    if guardar_dados==True:
        Criação_Planilha.armazenar_excel(Freq_A,'Dados_Analisador.xlsx','Frequência','A')
        Criação_Planilha.armazenar_excel(Freq_B,'Dados_Analisador.xlsx','Frequência','B')
        Criação_Planilha.armazenar_excel(Freq_C,'Dados_Analisador.xlsx','Frequência','C')

    eixo_x_A = np.arange(len(Freq_A))
    eixo_x_B = np.arange(len(Freq_B))
    eixo_x_C = np.arange(len(Freq_C))
    
    plt.style.use('classic')
    plt.subplot(3, 1, 1)
    plt.title('Frequência de Fase A')
    plt.ylabel('Frequência (Hz)')
    plt.xlabel('Tempo (s)')
    plt.plot(eixo_x_A, Freq_A,c='r')
    plt.grid()
    plt.tight_layout()
    plt.subplot(3, 1, 2)
    plt.title('Frequência de Fase B')
    plt.ylabel('Frequência (Hz)')
    plt.xlabel('Tempo (s)')
    plt.plot(eixo_x_B, Freq_B,c='r')
    plt.grid()
    plt.tight_layout()
    plt.subplot(3, 1, 3)
    plt.title('Frequência de Fase C')
    plt.ylabel('Frequência (Hz)')
    plt.xlabel('Tempo (s)')
    plt.plot(eixo_x_C, Freq_C,c='r')
    plt.grid()
    plt.tight_layout()
    plt.show()

