import numpy as np
from scipy.fft import fft, fftfreq
import re
import matplotlib.pyplot as plt

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
    
def sequencia_fase(taxa):
    taxa_amostragem=taxa
    num_linha = 3
    cont = 0
    Freq=60
    Tensão_A_aux = ler_arq('Tensão_A.txt', cont, num_linha)
    Tensão_B_aux = ler_arq('Tensão_B.txt', cont, num_linha)
    Tensão_C_aux = ler_arq('Tensão_C.txt', cont, num_linha)

    N = len(Tensão_A_aux)

    ##CALCULO FFT###
    fft_A = fft(Tensão_A_aux)
    fft_B = fft(Tensão_B_aux)
    fft_C = fft(Tensão_C_aux)
    frequencias = fftfreq(N, (1/taxa_amostragem))
    ##CALCULO FFT##
    ### ENCONTRA A FUNDAMENTAL ###
    fundamental = np.argmin(np.abs(frequencias - Freq))
    ### ENCONTRA A FUNDAMENTAL ###
    

    
    Ang_A = np.angle(fft_A[fundamental])
    Ang_B = np.angle(fft_B[fundamental])
    Ang_C = np.angle(fft_C[fundamental])
    Ang_A = np.degrees(Ang_A) % 360
    Ang_B = np.degrees(Ang_B) % 360
    Ang_C = np.degrees(Ang_C) % 360
    Ang_B = (Ang_B - Ang_A) % 360
    Ang_C = (Ang_C - Ang_A) % 360
    Ang_A = 0  # 
    ### ENCONTRA OS ANGULOS COLOCA EM GRAUS E COLOCA A NA REFERENCIA###
    
    ### PLOTAGEM###

    for angulo, fase in zip([Ang_A, Ang_B, Ang_C], ['A', 'B', 'C']):
        radiano = np.radians(angulo)
        plt.polar([0, radiano], [0, 1], label=f'{fase}: {angulo:.1f}°')
        plt.text(radiano, 1.2, f'{fase}: {angulo:.1f}°', horizontalalignment='center', verticalalignment='bottom')
        plt.plot(radiano, 1, '->', markersize=5, color='Black') 
    plt.title("Sequência de Fase")
    plt.legend()
    plt.tight_layout()
    plt.show()
