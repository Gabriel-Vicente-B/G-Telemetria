import numpy as np
import matplotlib.pyplot as plt
import Criação_Planilha
import re

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
    
def thd(Freq_Final,FFT_final):
    try:
        indice_fundamental = np.argmin(np.abs(Freq_Final- 60))
        componente_fundamental = np.abs(FFT_final[indice_fundamental])
        harmonicos = np.abs(FFT_final)
        harmonicos = np.delete(harmonicos, indice_fundamental)  # Remove a componente fundamental

        if componente_fundamental > 0:
            thd = np.sqrt(np.sum(harmonicos**2)) / componente_fundamental
        else:
            thd = 0
        THD=thd * 100
    except Exception:
        THD=0
    return round(THD,2)

def THD_Sinais(tempo,taxa,guardar_dados):
    tempo_de_coleta=tempo
    cont_coleta=0#contador para o tempo de coleta
    cont=0  # contador para indicar a partir de onde o codigo vai começar a pegar as amostras
    num_linha=3 #numero de linhas com 10k amostra que vai ler por ciclor total 40k amostra
    THD_V_A,THD_V_B,THD_V_C=[],[],[]
    THD_I_A,THD_I_B,THD_I_C=[],[],[]
    taxa_de_amostragem=taxa
    while(True):

        Tensão_A_aux = ler_arq('Tensão_A.txt', cont, num_linha)
        Tensão_A_aux = Tensão_A_aux - np.mean(Tensão_A_aux)
        try: 
            Freq_Tensão_A = np.fft.fftfreq(len(Tensão_A_aux), 1/taxa_de_amostragem)
            Freq_Tensão_Af = Freq_Tensão_A[Freq_Tensão_A > 0]
        except Exception:
            Freq_Tensão_Af = 0

        try: 
            FFT_Tensão_A = np.fft.fft(Tensão_A_aux)
            FFT_Tensão_Af = FFT_Tensão_A[Freq_Tensão_A > 0]
        except Exception:
            FFT_Tensão_Af = 0

        v = thd(Freq_Tensão_Af, FFT_Tensão_Af)
        THD_V_A.append(v)

        Tensão_B_aux = ler_arq('Tensão_B.txt', cont, num_linha)
        Tensão_B_aux = Tensão_B_aux - np.mean(Tensão_B_aux)

        try: 
            Freq_Tensão_B = np.fft.fftfreq(len(Tensão_B_aux), 1/taxa_de_amostragem)
            Freq_Tensão_Bf = Freq_Tensão_B[Freq_Tensão_B > 0]
        except Exception:
            Freq_Tensão_Bf = 0

        try: 
            FFT_Tensão_B = np.fft.fft(Tensão_B_aux)
            FFT_Tensão_Bf = FFT_Tensão_B[Freq_Tensão_B > 0]
        except Exception:
            FFT_Tensão_Bf = 0

        v = thd(Freq_Tensão_Bf, FFT_Tensão_Bf)
        THD_V_B.append(v)

        Tensão_C_aux = ler_arq('Tensão_C.txt', cont, num_linha)
        Tensão_C_aux = Tensão_C_aux - np.mean(Tensão_C_aux)

        try: 
            Freq_Tensão_C = np.fft.fftfreq(len(Tensão_C_aux), 1/taxa_de_amostragem)
            Freq_Tensão_Cf = Freq_Tensão_C[Freq_Tensão_C > 0]
        except Exception:
            Freq_Tensão_Cf = 0

        try: 
            FFT_Tensão_C = np.fft.fft(Tensão_C_aux)
            FFT_Tensão_Cf = FFT_Tensão_C[Freq_Tensão_C > 0]
        except Exception:
            FFT_Tensão_Cf = 0

        v = thd(Freq_Tensão_Cf, FFT_Tensão_Cf)
        THD_V_C.append(v)

        Corrente_A_aux = ler_arq('Corrente_A.txt', cont, num_linha)
        Corrente_A_aux = Corrente_A_aux - np.mean(Corrente_A_aux)

        try: 
            Freq_Corrente_A = np.fft.fftfreq(len(Corrente_A_aux), 1/taxa_de_amostragem)
            Freq_Corrente_Af = Freq_Corrente_A[Freq_Corrente_A > 0]
        except Exception:
            Freq_Corrente_Af = 0

        try: 
            FFT_Corrente_A = np.fft.fft(Corrente_A_aux)
            FFT_Corrente_Af = FFT_Corrente_A[Freq_Corrente_A > 0]
        except Exception:
            FFT_Corrente_Af = 0

        v = thd(Freq_Corrente_Af, FFT_Corrente_Af)
        THD_I_A.append(v)

        Corrente_B_aux = ler_arq('Corrente_B.txt', cont, num_linha)
        Corrente_B_aux = Corrente_B_aux - np.mean(Corrente_B_aux)

        try: 
            Freq_Corrente_B = np.fft.fftfreq(len(Corrente_B_aux), 1/taxa_de_amostragem)
            Freq_Corrente_Bf = Freq_Corrente_B[Freq_Corrente_B > 0]
        except Exception:
            Freq_Corrente_Bf = 0

        try: 
            FFT_Corrente_B = np.fft.fft(Corrente_B_aux)
            FFT_Corrente_Bf = FFT_Corrente_B[Freq_Corrente_B > 0]
        except Exception:
            FFT_Corrente_Bf = 0

        v = thd(Freq_Corrente_Bf, FFT_Corrente_Bf)
        THD_I_B.append(v)

        Corrente_C_aux = ler_arq('Corrente_C.txt', cont, num_linha)
        Corrente_C_aux = Corrente_C_aux - np.mean(Corrente_C_aux)

        try: 
            Freq_Corrente_C = np.fft.fftfreq(len(Corrente_C_aux), 1/taxa_de_amostragem)
            Freq_Corrente_Cf = Freq_Corrente_C[Freq_Corrente_C > 0]
        except Exception:
            Freq_Corrente_Cf = 0

        try: 
            FFT_Corrente_C = np.fft.fft(Corrente_C_aux)
            FFT_Corrente_Cf = FFT_Corrente_C[Freq_Corrente_C > 0]
        except Exception:
            FFT_Corrente_Cf = 0

        v = thd(Freq_Corrente_Cf, FFT_Corrente_Cf)
        THD_I_C.append(v)

        cont_coleta+=1
        cont+=num_linha
        if cont_coleta==tempo_de_coleta:
            break   

    if guardar_dados==True:
        Criação_Planilha.armazenar_excel(THD_V_A,'Dados_Analisador.xlsx','THD','A')
        Criação_Planilha.armazenar_excel(THD_V_B,'Dados_Analisador.xlsx','THD','B')
        Criação_Planilha.armazenar_excel(THD_V_C,'Dados_Analisador.xlsx','THD','C')
        Criação_Planilha.armazenar_excel(THD_I_A,'Dados_Analisador.xlsx','THD','D')
        Criação_Planilha.armazenar_excel(THD_I_B,'Dados_Analisador.xlsx','THD','E')
        Criação_Planilha.armazenar_excel(THD_I_C,'Dados_Analisador.xlsx','THD','F')

    eixo_x_V_A = np.arange(len(THD_V_A))
    eixo_x_V_B = np.arange(len(THD_V_B))
    eixo_x_V_C = np.arange(len(THD_V_C))
    eixo_x_I_A = np.arange(len(THD_I_A))
    eixo_x_I_B = np.arange(len(THD_I_B))
    eixo_x_I_C = np.arange(len(THD_I_C))

    plt.style.use('classic')
    plt.subplot(3,2,1)
    plt.title('THD TENSÃO FASE A')
    plt.xlabel('Tempo(s)')
    plt.ylabel('THD (%)')
    plt.axhline(10,c='r')
    plt.bar(eixo_x_V_A, THD_V_A)
    plt.grid()
    plt.tight_layout()
    plt.subplot(3,2,3)
    plt.title('THD TENSÃO FASE B')
    plt.xlabel('Tempo(s)')
    plt.ylabel('THD (%)')
    plt.axhline(10,c='r')
    plt.bar(eixo_x_V_B, THD_V_B)
    plt.grid()
    plt.tight_layout()
    plt.subplot(3,2,5)
    plt.title('THD TENSÃO FASE C')
    plt.xlabel('Tempo(s)')
    plt.ylabel('THD (%)')
    plt.axhline(10,c='r')
    plt.bar(eixo_x_V_C, THD_V_C)
    plt.grid()
    plt.tight_layout()
    plt.subplot(3,2,2)
    plt.title('THD Corrente FASE A')
    plt.xlabel('Tempo(s)')
    plt.ylabel('THD (%)')
    plt.axhline(10,c='r')
    plt.bar(eixo_x_I_A, THD_I_A)
    plt.grid()
    plt.tight_layout()
    plt.subplot(3,2,4)
    plt.title('THD Corrente FASE B')
    plt.xlabel('Tempo(s)')
    plt.ylabel('THD (%)')
    plt.axhline(10,c='r')
    plt.bar(eixo_x_I_B, THD_I_A)
    plt.grid()
    plt.tight_layout()
    plt.subplot(3,2,6)
    plt.title('THD Corrente FASE C')
    plt.xlabel('Tempo(s)')
    plt.ylabel('THD (%)')
    plt.axhline(10,c='r')
    plt.bar(eixo_x_I_C, THD_I_C)
    plt.grid()
    plt.tight_layout()
    plt.show()
