import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import re

# Função para ler dados dos arquivos e armazenar em arrays
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

    
Grafico = plt.figure()
# Variáveis globais
Dados=open("Taxa_de_Atualização.txt").read() 
linhas = Dados.split('\n')
for i in linhas: 
    if "T" in i: 
            taxa_de_atualização = eval(i[2:]) 

num_amostra_inicio = 0
num_amostra_final = taxa_de_atualização
taxa_inicial = 0
cont=0

def atualização(taxa):
    global taxa_de_atualização, Est
    
    Dados = open("Taxa_de_Atualização.txt").read() 
    linhas = Dados.split('\n')
    
    for linha in linhas: 
        if "T" in linha: 
            taxa_de_atualização = eval(linha[2:]) 
        if "E" in linha: 
            Est = eval(linha[2:])                

    if Est != 'Play':
        anim.event_source.stop()     
    if taxa != taxa_de_atualização:
        return taxa_de_atualização, True
    return taxa_de_atualização, False

def Plotagem(t):
    
    global num_amostra_inicio, num_amostra_final, taxa_inicial,cont
    num_linha=3
    taxa_de_atualização, i = atualização(taxa_inicial)
    taxa_inicial = taxa_de_atualização

    Tensão_A= ler_arq('Tensão_A.txt', cont, num_linha)
    Tensão_B= ler_arq('Tensão_B.txt', cont, num_linha)
    Tensão_C= ler_arq('Tensão_C.txt', cont, num_linha)
    Corrente_A= ler_arq('Corrente_A.txt', cont, num_linha)
    Corrente_B= ler_arq('Corrente_B.txt', cont, num_linha)
    Corrente_C = ler_arq('Corrente_C.txt', cont, num_linha)


    Tensão_A_format = Tensão_A[num_amostra_inicio:num_amostra_final]
    Tensão_B_format = Tensão_B[num_amostra_inicio:num_amostra_final]
    Tensão_C_format = Tensão_C[num_amostra_inicio:num_amostra_final]
    Corrente_A_format = Corrente_A[num_amostra_inicio:num_amostra_final]
    Corrente_B_format = Corrente_B[num_amostra_inicio:num_amostra_final]
    Corrente_C_format = Corrente_C[num_amostra_inicio:num_amostra_final]

    if i: 
        num_amostra_inicio += taxa_de_atualização
        num_amostra_final = num_amostra_inicio + taxa_de_atualização
        i = False
    else:
        num_amostra_inicio += taxa_de_atualização
        num_amostra_final += taxa_de_atualização 

    if num_amostra_final >= len(Tensão_A):
        num_amostra_inicio = 0
        num_amostra_final = taxa_de_atualização
        cont += num_linha
    
    
    Grafico.clear()
    plt.style.use('classic')
    plt.subplot(2, 1, 1)
    plt.plot(Tensão_A_format, color='m', label='Fase A')
    plt.plot(Tensão_B_format, color='g', label='Fase B')
    plt.plot(Tensão_C_format, color='r', label='Fase C')
    plt.title('Tensões')
    plt.xlabel('t')
    plt.ylabel('Tensão(V)')
    plt.legend()
    plt.grid()
    
    plt.subplot(2, 1, 2)
    plt.plot(Corrente_A_format, color='m', label='Fase A')
    plt.plot(Corrente_B_format, color='g', label='Fase B')
    plt.plot(Corrente_C_format, color='r', label='Fase C')
    plt.title('Correntes')
    plt.xlabel('t')
    plt.ylabel('Corrente(A)')
    plt.legend()
    plt.grid()
    
    plt.tight_layout()

# Inicialização da animação
anim = animation.FuncAnimation(Grafico, Plotagem, interval=100, repeat=True, cache_frame_data=False)
plt.show()


