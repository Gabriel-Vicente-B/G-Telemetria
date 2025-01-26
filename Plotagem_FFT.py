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

def FFT_Sinais(tempo,taxa,guardar_dados):
    tempo_de_coleta=tempo
    cont_coleta=0#contador para o tempo de coleta
    cont=0  # contador para indicar a partir de onde o codigo vai começar a pegar as amostras
    num_linha=3 #numero de linhas com 10k amostra que vai ler por ciclor total 40k amostra
    taxa_de_amostragem=taxa

    while(True):

        Tensão_A_aux = ler_arq('Tensão_A.txt', cont, num_linha)
        Tensão_B_aux = ler_arq('Tensão_B.txt', cont, num_linha)           
        Tensão_C_aux = ler_arq('Tensão_C.txt', cont, num_linha)
        Corrente_A_aux = ler_arq('Corrente_A.txt', cont, num_linha)
        Corrente_B_aux = ler_arq('Corrente_B.txt', cont, num_linha)
        Corrente_C_aux = ler_arq('Corrente_C.txt', cont, num_linha)
        Tensão_A_aux = Tensão_A_aux - np.mean(Tensão_A_aux)
        Tensão_B_aux = Tensão_B_aux - np.mean(Tensão_B_aux)
        Tensão_C_aux = Tensão_C_aux - np.mean(Tensão_C_aux)
        Corrente_A_aux = Corrente_A_aux - np.mean(Corrente_A_aux)
        Corrente_B_aux = Corrente_B_aux - np.mean(Corrente_B_aux)
        Corrente_C_aux = Corrente_C_aux - np.mean(Corrente_C_aux)


        cont_coleta+=1
        cont+=num_linha
        if cont_coleta==tempo_de_coleta:
            break   
        try: 
            Freq_Tensão_A = np.fft.fftfreq(len(Tensão_A_aux), 1/taxa_de_amostragem)
            Freq_Tensão_Af = Freq_Tensão_A[:len(Tensão_A_aux)//2]
        except Exception:
            Freq_Tensão_Af = 0

        try: 
            FFT_Tensão_A = np.fft.fft(Tensão_A_aux)
            FFT_Tensão_A = abs(FFT_Tensão_A)/len(Tensão_A_aux)
            FFT_Tensão_Af = FFT_Tensão_A[:len(Tensão_A_aux)//2] ** 2
        except Exception:
            FFT_Tensão_Af = 0

        try: 
            Freq_Tensão_B = np.fft.fftfreq(len(Tensão_B_aux), 1/taxa_de_amostragem)
            Freq_Tensão_Bf = Freq_Tensão_B[:len(Tensão_B_aux)//2]
        except Exception:
            Freq_Tensão_Bf = 0

        try: 
            FFT_Tensão_B = np.fft.fft(Tensão_B_aux)
            FFT_Tensão_B = abs(FFT_Tensão_B)/len(Tensão_B_aux)
            FFT_Tensão_Bf = FFT_Tensão_B[:len(Tensão_B_aux)//2] ** 2
        except Exception:
            FFT_Tensão_Bf = 0

        try: 
            Freq_Tensão_C = np.fft.fftfreq(len(Tensão_C_aux), 1/taxa_de_amostragem)
            Freq_Tensão_Cf = Freq_Tensão_C[:len(Tensão_C_aux)//2]
        except Exception:
            Freq_Tensão_Cf = 0

        try: 
            FFT_Tensão_C = np.fft.fft(Tensão_C_aux)
            FFT_Tensão_C = abs(FFT_Tensão_C)/len(Tensão_C_aux)
            FFT_Tensão_Cf = FFT_Tensão_C[:len(Tensão_C_aux)//2] ** 2
        except Exception:
            FFT_Tensão_Cf = 0

        try: 
            Freq_Corrente_A = np.fft.fftfreq(len(Corrente_A_aux), 1/taxa_de_amostragem)
            Freq_Corrente_Af = Freq_Corrente_A[:len(Corrente_A_aux)//2]
        except Exception:
            Freq_Corrente_Af = 0

        try: 
            FFT_Corrente_A = np.fft.fft(Corrente_A_aux)
            FFT_Corrente_A = abs(FFT_Corrente_A)/len(Corrente_A_aux)
            FFT_Corrente_Af = FFT_Corrente_A[:len(Corrente_A_aux)//2] ** 2
        except Exception:
            FFT_Corrente_Af = 0

        try: 
            Freq_Corrente_B = np.fft.fftfreq(len(Corrente_B_aux), 1/taxa_de_amostragem)
            Freq_Corrente_Bf = Freq_Corrente_B[:len(Corrente_B_aux)//2]
        except Exception:
            Freq_Corrente_Bf = 0

        try: 
            FFT_Corrente_B = np.fft.fft(Corrente_B_aux)
            FFT_Corrente_B = abs(FFT_Corrente_B)/len(Corrente_B_aux)
            FFT_Corrente_Bf = FFT_Corrente_B[:len(Corrente_B_aux)//2] ** 2
        except Exception:
            FFT_Corrente_Bf = 0

        try: 
            Freq_Corrente_C = np.fft.fftfreq(len(Corrente_C_aux), 1/taxa_de_amostragem)
            Freq_Corrente_Cf = Freq_Corrente_C[:len(Corrente_C_aux)//2]
        except Exception:
            Freq_Corrente_Cf = 0

        try: 
            FFT_Corrente_C = np.fft.fft(Corrente_C_aux)
            FFT_Corrente_C = abs(FFT_Corrente_C)/len(Corrente_C_aux)
            FFT_Corrente_Cf = FFT_Corrente_C[:len(Corrente_C_aux)//2] ** 2
        except Exception:
            FFT_Corrente_Cf = 0

    plt.style.use('classic')
    plt.subplot(3,2,1)
    plt.title('FFT TENSÃO FASE A')
    plt.xlabel('Frequencia (Hz)')
    plt.ylabel('Energia(V²)')
    plt.xlim(0,3500)
    plt.grid()
    plt.tight_layout()
    plt.plot(Freq_Tensão_Af,FFT_Tensão_Af)
    plt.subplot(3,2,3)
    plt.title('FFT TENSÃO FASE B')
    plt.xlabel('Frequencia (Hz)')
    plt.ylabel('Energia(V²)')
    plt.xlim(0,3500)
    plt.grid()
    plt.tight_layout()
    plt.plot(Freq_Tensão_Bf,FFT_Tensão_Bf)
    plt.subplot(3,2,5)
    plt.title('FFT TENSÃO FASE C')
    plt.xlabel('Frequencia (Hz)')
    plt.ylabel('Energia(V²)')
    plt.xlim(0,3500)
    plt.grid()
    plt.tight_layout()
    plt.plot(Freq_Tensão_Cf,FFT_Tensão_Cf)
    plt.subplot(3,2,2)
    plt.title('FFT Corrente FASE A')
    plt.xlabel('Frequencia (Hz)')
    plt.ylabel('Energia(I²)')
    plt.xlim(0,3500)
    plt.grid()
    plt.tight_layout()
    plt.plot(Freq_Corrente_Af,FFT_Corrente_Af)
    plt.subplot(3,2,4)
    plt.title('FFT Corrente FASE B')
    plt.xlabel('Frequencia (Hz)')
    plt.ylabel('Energia(I²)')
    plt.xlim(0,3500)
    plt.grid()
    plt.tight_layout()
    plt.plot(Freq_Corrente_Bf,FFT_Corrente_Bf)
    plt.subplot(3,2,6)
    plt.title('FFT Corrente FASE C')
    plt.xlabel('Frequencia (Hz)')
    plt.ylabel('Energia(I²)')
    plt.xlim(0,3500)
    plt.grid()
    plt.tight_layout()
    plt.plot(Freq_Corrente_Cf,FFT_Corrente_Cf)
    plt.tight_layout()
    plt.show()


    if guardar_dados ==True:
        Criação_Planilha.armazenar_excel(Freq_Tensão_Af,'Dados_Analisador.xlsx','FFT','A')
        Criação_Planilha.armazenar_excel(FFT_Tensão_Af,'Dados_Analisador.xlsx','FFT','B')
        Criação_Planilha.armazenar_excel(Freq_Tensão_Bf,'Dados_Analisador.xlsx','FFT','C')
        Criação_Planilha.armazenar_excel(FFT_Tensão_Bf,'Dados_Analisador.xlsx','FFT','D')
        Criação_Planilha.armazenar_excel(Freq_Tensão_Cf,'Dados_Analisador.xlsx','FFT','E')
        Criação_Planilha.armazenar_excel(FFT_Tensão_Cf,'Dados_Analisador.xlsx','FFT','F')
        Criação_Planilha.armazenar_excel(Freq_Corrente_Af,'Dados_Analisador.xlsx','FFT','G')
        Criação_Planilha.armazenar_excel(FFT_Corrente_Af,'Dados_Analisador.xlsx','FFT','H')
        Criação_Planilha.armazenar_excel(Freq_Corrente_Bf,'Dados_Analisador.xlsx','FFT','I')
        Criação_Planilha.armazenar_excel(FFT_Corrente_Bf,'Dados_Analisador.xlsx','FFT','J')
        Criação_Planilha.armazenar_excel(Freq_Corrente_Cf,'Dados_Analisador.xlsx','FFT','K')
        Criação_Planilha.armazenar_excel(FFT_Corrente_Cf,'Dados_Analisador.xlsx','FFT','L')
