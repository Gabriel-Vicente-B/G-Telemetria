
import customtkinter as tk
import tkinter as Tk
from PIL import ImageTk, Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import numpy as np
import os
import matplotlib.animation as animation
from Plotagem_Potencia import Plotar_Potencias
import multiprocessing
from Plotagem_THD import THD_Sinais
from Plotagem_Variação_de_Tensão import Variação_de_tensão
from Plotagem_Interrupções import Interrupção
from Criação_Planilha import criar_planilha
from Sequencia_de_Fase import sequencia_fase as seq
import Plotagem_Excel
from Recepcao_Dados import coleta_amostras
from Plotagem_FFT import FFT_Sinais
from Plotagem_de_Frequencia import Frequencia
import threading
import time
import re
import sys



####VARIAVEIS GLOBAIS####
Grafico = plt.figure(figsize=(11.68, 6))
taxa_de_atualização = 10
num_amostra_inicio = 0
num_amostra_final = taxa_de_atualização
taxa_inicial = 0
cont=0
est_pot=None
est_thd=None
est_variacao=None
est_Frequencia=None
est_interrupcao=None
est_FFT=None
val=True
p= None
pai_con = None
filho_con = None
####VARIAVEIS GLOBAIS####


####FUNÇÕES CHAMADAS PELA INTERFACE####
class Redirecionar_mensagem(object):
    def __init__(self, terminal):
        self.terminal = terminal

    def write(self, string):
        self.terminal.insert(tk.END, string)
        self.terminal.see(tk.END)

    def flush(self):
        pass

def read_pipe(pipe, terminal):
    while True:
        try:
            messagem = pipe.recv()
            if messagem:
                terminal.insert(tk.END, messagem + '\n')
                terminal.see(tk.END)
        except EOFError:
            break
        except Exception as e:
            terminal.insert(tk.END, f"Erro na leitura do pipe: {e}\n")
            break

def ler_arq(arq, cont, num_linha):
    data = []
    with open(arq, 'r') as file:
        for i, linha in enumerate(file):
            if i >= cont:
                linha = linha.strip()  # Remove espaços em branco e quebras de linha no início e no fim
                if linha:  # Verifica se a linha não está vazia
                    # Limpa a linha usando regex para permitir apenas números e pontos
                    linha_limpia = re.sub(r'[^\d.,-]', '', linha)
                    valores = linha_limpia.split(',')
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
def atualização(taxa):
    global taxa_de_atualização           

    if taxa != taxa_de_atualização:
        return taxa_de_atualização, True
    return taxa_de_atualização, False

def zoom_mais():
     global taxa_de_atualização
     val=int(0.01*N_linhas)
     taxa_de_atualização+=val

def zoom_menos():
     global taxa_de_atualização
     val=int(0.01*N_linhas)
     taxa_de_atualização-=val

def Plotagem(t):    
    global num_amostra_inicio, num_amostra_final, taxa_inicial,cont
    num_linha=1
    taxa_de_atualização,i = atualização(taxa_inicial)
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
 
    Tensão_A_freq = Tensão_A - np.mean(Tensão_A)
    N_V_A = len(Tensão_A_freq)
    fft_A = np.fft.fft(Tensão_A_freq)
    frequencias_A = np.fft.fftfreq(N_V_A, (1/Fs_conversão))
    mag_V_A = np.abs(fft_A)
    Val_max_V_A= np.argmax(mag_V_A[:N_V_A//2])
    frequencia=frequencias_A[Val_max_V_A]
    saida_terminal_freq.delete("1.0", tk.END) 
    saida_terminal_freq.insert(tk.END, f"F: {frequencia:.2f} Hz")
    

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

def Iniciar_coleta():
    global p, val, pai_con, filho_con
    try:
        if val:
            pai_con, filho_con = multiprocessing.Pipe()
            p=multiprocessing.Process(target=coleta_amostras,args=(Porta,baudrate,N_linhas, filho_con))
            p.start()
            if pai_con:
                threading.Thread(target=read_pipe, args=(pai_con, saida_terminal), daemon=True).start()
            saida_terminal.insert(tk.END,f'Recepção de Dados Iniciada.' + '\n')
            val=False
        else:
           if p and p.is_alive():
            p.terminate()
            saida_terminal.insert(tk.END, 'Recepção de Dados Parada.' + '\n')
            val = True
           else:
               val = True
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')

def E_potencia():
    try:
        processo=multiprocessing.Process(target=Plotagem_Excel.Plotar_Potencia)
        processo.start()
        saida_terminal.insert(tk.END,f'Os grafico de potencia foram plotados a partir do excel.' + '\n')
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')

def E_THD():
    try:
        processo=multiprocessing.Process(target=Plotagem_Excel.Plotar_THD)
        processo.start()
        saida_terminal.insert(tk.END,f'O grafico de THD foi plotado a partir do excel.' + '\n')
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')

def E_Variação():
    try:
        processo=multiprocessing.Process(target=Plotagem_Excel.Plotar_Variação)
        processo.start()
        saida_terminal.insert(tk.END,f'Os graficos de variação foram plotados a partir do excel.' + '\n')
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')

def E_Interupção():
    try:
        processo=multiprocessing.Process(target=Plotagem_Excel.Plotar_Interrupção)
        processo.start()
        saida_terminal.insert(tk.END,f'Os graficos de interrupção foram plotados a partir do excel.' + '\n')
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')

def E_Grandezas():
    try:
        processo=multiprocessing.Process(target=Plotagem_Excel.Plotar_Grandezas)
        processo.start()
        saida_terminal.insert(tk.END,f'Os graficos das grandezas foram plotados a partir do excel.' + '\n')
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')

def E_FFT():
    try:
        processo=multiprocessing.Process(target=Plotagem_Excel.Plotar_FFT)
        processo.start()
        saida_terminal.insert(tk.END,f'Os graficos das FFTs foram plotados a partir do excel.' + '\n')
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')

def E_Frequencia():
    try:
        processo=multiprocessing.Process(target=Plotagem_Excel.Plotar_Frequência)
        processo.start()
        saida_terminal.insert(tk.END,f'Os graficos das frequência foram plotados a partir do excel.' + '\n')
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')


def E_Todos():
    try:
        E_potencia()
        E_THD()
        E_Interupção()
        E_Variação()
        E_FFT()
        E_Grandezas()
        E_Frequencia()
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')

def C_Criar_Excel():
    try:
        processo=multiprocessing.Process(target=criar_planilha)
        processo.start()
        saida_terminal.insert(tk.END,f'Planilha Criada.' + '\n')
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')

def C_potencia():
    global evento_parar2
    evento_parar2= threading.Event()
    try:
        thread_temporizador = threading.Thread(target=temporizador,args=(saida_terminal_pot,evento_parar2,'Potencia'))
        thread_temporizador.start()
        processo=multiprocessing.Process(target=Plotar_Potencias,args=(tempo_coleta,est_pot))
        processo.start()
        thread_monitor = threading.Thread(target=monitorar_processo, args=(processo,evento_parar2))
        thread_monitor.start()
        if est_pot:
            saida_terminal.insert(tk.END, 'Os gráficos de potência e FP estão sendo preparados para plotagem e armazenamento.\n')
        else:
            saida_terminal.insert(tk.END, 'Os gráficos de potência e FP estão sendo preparados para plotagem.\n')
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')
        
def C_FFT():
    global evento_parar4
    evento_parar4= threading.Event()
    try:
        thread_temporizador = threading.Thread(target=temporizador,args=(saida_terminal_FFT,evento_parar4,'FFT'))
        thread_temporizador.start()
        processo=multiprocessing.Process(target=FFT_Sinais,args=(tempo_coleta,Fs_conversão,est_FFT))
        processo.start()
        thread_monitor = threading.Thread(target=monitorar_processo, args=(processo,evento_parar4))
        thread_monitor.start()
        if est_FFT:
            saida_terminal.insert(tk.END,f'Os gráficos das FFTs estão sendo preparados para plotagem e armazenamento.' + '\n')
        else:
            saida_terminal.insert(tk.END,f'Os graficos das FFTs estão sendo preparados para plotagem.' + '\n')
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')

def C_THD():
    global evento_parar1
    evento_parar1= threading.Event()
    try:
        thread_temporizador = threading.Thread(target=temporizador,args=(saida_terminal_THD,evento_parar1,'THD'))
        thread_temporizador.start()
        processo=multiprocessing.Process(target=THD_Sinais,args=(tempo_coleta,Fs_conversão,est_thd))
        processo.start()
        thread_monitor = threading.Thread(target=monitorar_processo, args=(processo, evento_parar1))
        thread_monitor.start()
        if est_thd:
            saida_terminal.insert(tk.END,f'Os gráficos de THD estão sendo preparados para plotagem e armazenamento.' + '\n')
        else:
            saida_terminal.insert(tk.END,f'Os gráficos de THD estão sendo preparados para plotagem.' + '\n')
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')

def C_Variação():
    global evento_parar0
    evento_parar0 = threading.Event()
    try:
        thread_temporizador = threading.Thread(target=temporizador,args=(saida_terminal_variação,evento_parar0,'Variação'))
        thread_temporizador.start()
        processo=multiprocessing.Process(target=Variação_de_tensão,args=(tempo_coleta,V_fase,est_variacao))
        processo.start()
        thread_monitor = threading.Thread(target=monitorar_processo, args=(processo, evento_parar0))
        thread_monitor.start()
        if est_thd==True:
            saida_terminal.insert(tk.END,f'Os gráficos de variação de tensão estão sendo preparados para plotagem e armazenamento.' + '\n')
        else:
            saida_terminal.insert(tk.END,f'Os gráficos de variação de tensão estão sendo preparados para plotagem.' + '\n')
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')

def C_Interrupções():
    global evento_parar3
    evento_parar3= threading.Event()
    try:
        thread_temporizador = threading.Thread(target=temporizador,args=(saida_terminal_Interrupção,evento_parar3,'Interrupção'))
        thread_temporizador.start()
        processo=multiprocessing.Process(target=Interrupção,args=(tempo_coleta,Fs_conversão,est_interrupcao))
        processo.start()
        thread_monitor = threading.Thread(target=monitorar_processo, args=(processo, evento_parar3))
        thread_monitor.start()
        if est_interrupcao==True:
            saida_terminal.insert(tk.END,f'Os gráficos de interrupção da tensão estão sendo preparados para plotagem e armazenamento.' + '\n')
        else:
            saida_terminal.insert(tk.END,f'Os gráficos de interrupção da tensão estão sendo preparados para plotagem.' + '\n')
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')      

def C_Frequencia():
    global evento_parar5
    evento_parar5= threading.Event()
    try:
        thread_temporizador = threading.Thread(target=temporizador,args=(saida_terminal_freque,evento_parar5,'Frequência'))
        thread_temporizador.start()
        processo=multiprocessing.Process(target=Frequencia,args=(tempo_coleta,Fs_conversão,est_Frequencia))
        processo.start()
        thread_monitor = threading.Thread(target=monitorar_processo, args=(processo, evento_parar5))
        thread_monitor.start()
        if est_Frequencia==True:
            saida_terminal.insert(tk.END,f'Os gráficos de Frequência das Fases estão sendo preparados para plotagem e armazenamento.' + '\n')
        else:
            saida_terminal.insert(tk.END,f'Os gráficos de Frequência das Fases  estão sendo preparados para plotagem.' + '\n')
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')  

def C_todos():
    try:
        C_potencia()
        C_THD()
        C_Interrupções()
        C_Variação()
        C_FFT()
        C_Frequencia()
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')   

def Sequencia():
    try:
        processo=multiprocessing.Process(target=seq,args=(Fs_conversão,))
        processo.start()
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')  

def limpar():
        saida_terminal.delete("1.0", tk.END)

def plotar_grafico():
    global anim,evento_parar_1 
    evento_parar_1 = threading.Event()
    try:
        thread_temporizador = threading.Thread(target=temporizador,args=(saida_terminal_Tempo,evento_parar_1,'real'))
        thread_temporizador.start()
        anim = animation.FuncAnimation(Grafico, Plotagem, interval=100, repeat=True, cache_frame_data=False) 
        canvas.draw()
    except Exception as e:
        saida_terminal.insert(tk.END, f'Ocorreu um erro: {e}\n')

def play_pause(): 
    global evento_parar_1
    evento_parar_1.set()
    anim.event_source.stop()

def temporizador(terminal, parada, dado):
    inicio = time.perf_counter()  
    while not parada.is_set():
        tempocorrido = time.perf_counter()
        tempo = tempocorrido - inicio 
        terminal.delete("1.0", tk.END) 
        terminal.insert(tk.END, f"Tempo de coleta dados {dado}: {tempo:.2f}s")
        time.sleep(1)

def monitorar_processo(processo, evento,):
    processo.join() 
    evento.set() 

def monitorar_botao(evento):
    global evento_parar0,evento_parar1, evento_parar2,evento_parar3,evento_parar4
    evento.set()     
####FUNÇÕES CHAMADAS PELA INTERFACE####

####INICIAR E CONFIGURAR INTERFACE####
def criar_interface():
    def checkbox_potencia():
        global est_pot
        if var_pot.get():
            est_pot=True
        else:
            est_pot=False

    def checkbox_thd():
        global est_thd
        if var_thd.get():
            est_thd=True
        else:
            est_thd=False

    def checkbox_variacao():
        global est_variacao
        if var_variacao.get():
            est_variacao=True
        else:
            est_variacao=False

    def checkbox_interrupcao():
        global est_interrupcao
        if var_interrupcao.get():
            est_interrupcao=True
        else:
            est_interrupcao=False

    def checkbox_FFT():
        global est_FFT
        if var_FFT.get():
            est_FFT=True
        else:
            est_FFT=False
    def checkbox_Freq():
        global est_Frequencia
        if var_freq.get():
            est_Frequencia=True
        else:
            est_Frequencia=False

    def config_frame(event):
        largura_total = Programa.winfo_width()
        altura_total = Programa.winfo_height()
        frame_dados.place(x=10, y=int(altura_total * 0.28))
        frame_func_coleta.place(x=int(largura_total * 0.135),y=int(altura_total * 0.02))
        frame_func_excel.place(x=int(largura_total * 0.135), y=int(altura_total * 0.515))
        frame_Grafico.place(x=int(largura_total * 0.264), y=int(altura_total * 0.02))
        frame_Chat.place(x=int(largura_total * 0.264), y=int(altura_total * 0.68))
        frame_Dev.place(x=int(largura_total * 0.264), y=int(altura_total * 0.963))
        frame_indices.place(x=int(largura_total * 0.813), y=int(altura_total * 0.68))

    def coletar_temp_coleta():
        cont=0
        global tempo_coleta 
        try:
            tempo_coleta= float(QNTD_amostras.get())
            cont+=1
        except Exception as e:
            saida_terminal.insert(tk.END, f'Verifique o tempo de coleta.\n')    
        global baudrate
        try:
            baudrate=float(baudrate_b.get())
            cont+=1
        except Exception as e:
            saida_terminal.insert(tk.END, f'Verifique a baudrate.\n')      
        global Fs_conversão
        try:
            Fs_conversão=float(Fs_conversão_b.get())
            cont+=1
        except Exception as e:
            saida_terminal.insert(tk.END, f'Verifique a frequencia de amostragem das fases.\n')    
        global V_fase
        try:
            V_fase=float(Tensão_FASE.get())
            cont+=1
        except Exception as e:
            saida_terminal.insert(tk.END, f'Verifique a tensão de fase.\n')        
        global Porta
        try:
            Porta=Porta_b.get()
            cont+=1
        except Exception as e:
            saida_terminal.insert(tk.END, f'Verifique a porta de conexão.\n')    
        global N_linhas
        try:
            N_linhas=float(QNTD_amostras_linha.get())
            cont+=1
        except Exception as e:
            saida_terminal.insert(tk.END, f'Verifique a quantidade de amostras por linha.\n')  
        if cont==6:  
            saida_terminal.insert(tk.END,f'Todos os dados foram inseridos com sucesso.' + '\n')

    Programa = tk.CTk()
    Programa.title("G-Telemetria")
    Programa.geometry("1600x980")  
    
    #### CRIAÇÃO E CONFIGURAÇÃO DOS FRAMES####
    frame_dados = tk.CTkFrame(Programa)
    frame_func_coleta = tk.CTkFrame(Programa)
    frame_func_excel = tk.CTkFrame(Programa)
    frame_Grafico = tk.CTkFrame(Programa)
    frame_Chat = tk.CTkFrame(Programa)
    frame_Dev = tk.CTkFrame(Programa)
    frame_indices=tk.CTkFrame(Programa)
    largura_total = Programa.winfo_width()
    altura_total = Programa.winfo_height()
    frame_indices.configure(width=int(largura_total * 5.85), height=int(altura_total * 1.36))
    frame_dados.configure(width=int(largura_total * 1), height=int(altura_total * 3.5))
    frame_func_coleta.configure(width=int(largura_total * 1), height=int(altura_total * 2.35))
    frame_func_excel.configure(width=int(largura_total * 1), height=int(altura_total * 2.35))
    frame_Grafico.configure(width=int(largura_total *5.85), height=int(altura_total * 3.2))
    frame_Chat.configure(width=int(largura_total * 6.85), height=int(altura_total * 1.36))
    frame_Dev.configure(width=int(largura_total * 5.85), height=int(altura_total * 0.15))
    #### CRIAÇÃO E CONFIGURAÇÃO DOS FRAMES####
    
    ####MENU ENTRADA DE DADOS######
    titulo_frame = tk.CTkLabel(frame_dados, text='Configurações:', font=("Helvetica", 20))
    titulo_frame.grid(row=0, column=0, padx=10, pady=10)
    baudrate_b = tk.CTkEntry(frame_dados,placeholder_text='BaundRate', width=177, height=30, font=("Helvetica", 10))
    baudrate_b.grid(row=1, column=0, padx=10, pady=10)
    Fs_conversão_b= tk.CTkEntry(frame_dados,placeholder_text='Frequencia de Conversão(Hz)', width=177, height=30, font=("Helvetica", 10))
    Fs_conversão_b.grid(row=2, column=0, padx=10, pady=10)
    Porta_b=tk.CTkEntry(frame_dados,placeholder_text='Porta USB', width=177, height=30, font=("Helvetica", 10))
    Porta_b.grid(row=3, column=0, padx=10, pady=10)
    Tensão_FASE=tk.CTkEntry(frame_dados,placeholder_text='Tensão de Fase (V)', width=177, height=30, font=("Helvetica", 10))
    Tensão_FASE.grid(row=4, column=0, padx=10, pady=10)
    QNTD_amostras=tk.CTkEntry(frame_dados,placeholder_text='Tempo de coleta(s)', width=177, height=30, font=("Helvetica", 10))
    QNTD_amostras.grid(row=5, column=0, padx=10, pady=10)
    QNTD_amostras_linha=tk.CTkEntry(frame_dados,placeholder_text='Nº de amostras p/ linha', width=177, height=30, font=("Helvetica", 10))
    QNTD_amostras_linha.grid(row=6, column=0, padx=10, pady=10)
    botao_inserir = tk.CTkButton(frame_dados, text="Inserir parametros", width=177, height=38,font=("Helvetica", 20),command = coletar_temp_coleta)
    botao_inserir.grid(row=7, column=0, padx=10, pady=3)
    botao_Iniciar_coleta = tk.CTkButton(frame_dados, text="Play/Pause Coleta", width=177, height=38,font=("Helvetica", 20),command = Iniciar_coleta)
    botao_Iniciar_coleta.grid(row=8, column=0, padx=10, pady=3)
    Botão_Criar_Excel = tk.CTkButton(frame_dados, text="Criar Excel", width=177, height=38,font=("Helvetica", 20),command = C_Criar_Excel)
    Botão_Criar_Excel.grid(row=9, column=0, padx=10, pady=3)
    titulo_frame = tk.CTkLabel(frame_dados, text='Salvar Dados:', font=("Helvetica", 20))
    titulo_frame.grid(row=10, column=0, padx=10, pady=6)
    var_pot = tk.IntVar()
    checkbox_var_pot = tk.CTkCheckBox(master=frame_dados, text="Dados de Potencia", width=5, height=5, variable=var_pot,command=checkbox_potencia)
    checkbox_var_pot.grid(row=11, column=0,padx=(0, 10), pady=3)
    var_thd = tk.BooleanVar()
    checkbox_var_thd = tk.CTkCheckBox(master=frame_dados, text="Dados de THD", width=5, height=5,variable=var_thd,command=checkbox_thd)
    checkbox_var_thd.grid(row=12, column=0, padx=(0, 33), pady=3)
    var_variacao= tk.BooleanVar()
    checkbox_var_variacao = tk.CTkCheckBox(master=frame_dados, text="Dados de Δ Tensão", width=5, height=5,variable=var_variacao,command=checkbox_variacao)
    checkbox_var_variacao.grid(row=13, column=0, padx=(0, 5), pady=3)
    var_interrupcao= tk.BooleanVar()
    checkbox_var_interrupcao = tk.CTkCheckBox(master=frame_dados, text="Dados de Interrupção", width=5, height=5,variable=var_interrupcao,command=checkbox_interrupcao)
    checkbox_var_interrupcao.grid(row=14, column=0, padx=(6, 0), pady=3)
    var_FFT= tk.BooleanVar()
    checkbox_var_FFT = tk.CTkCheckBox(master=frame_dados, text="Dados de FFT", width=5, height=5,variable=var_FFT,command=checkbox_FFT)
    checkbox_var_FFT.grid(row=15, column=0, padx=(0, 37), pady=3)
    var_freq= tk.BooleanVar()
    checkbox_var_freq = tk.CTkCheckBox(master=frame_dados, text="Dados de Frequêcia", width=5, height=5,variable=var_freq,command=checkbox_Freq)
    checkbox_var_freq.grid(row=16, column=0, padx=(0, 3), pady=3)
    ####MENU ENTRADA DE DADOS######

    ####MENU PARA PLOTAGEM A PARTIR DO TXT ######
    titulo_frame = tk.CTkLabel(frame_func_coleta, text='Menu:', font=("Helvetica", 20))
    titulo_frame.grid(row=0, column=0, padx=10, pady=7)
    Botão_plotar_no_tempo=tk.CTkButton(frame_func_coleta, text='Plotagem em Tempo \n Real', width=160, height=40, font=("Helvetica", 15),command=plotar_grafico)
    Botão_plotar_no_tempo.grid(row=1, column=0, padx=20, pady=7)
    Botão_plotar_potencia=tk.CTkButton(frame_func_coleta, text='Plotagem Dados \n De Potencia', width=160, height=40, font=("Helvetica", 15),command=C_potencia)
    Botão_plotar_potencia.grid(row=2, column=0, padx=20, pady=7)
    Botão_plotar_THD=tk.CTkButton(frame_func_coleta, text='Plotagem Dados \n de THD', width=160, height=40, font=("Helvetica", 15),command=C_THD)
    Botão_plotar_THD.grid(row=3, column=0, padx=20, pady=7)
    Botão_plotar_variacao=tk.CTkButton(frame_func_coleta, text='Plotagem Dados \n de Δ Tensão', width=160, height=40, font=("Helvetica", 15),command=C_Variação)
    Botão_plotar_variacao.grid(row=4, column=0, padx=20, pady=7)
    Botão_plotar_interrupcao=tk.CTkButton(frame_func_coleta, text='Plotagem Dados \n de Interrupção', width=160, height=40, font=("Helvetica", 15),command=C_Interrupções)
    Botão_plotar_interrupcao.grid(row=5, column=0, padx=20, pady=7)
    Botão_plotar_FFT=tk.CTkButton(frame_func_coleta, text='Plotagem Dados \n de FFT', width=160, height=40, font=("Helvetica", 15),command=C_FFT)
    Botão_plotar_FFT.grid(row=6, column=0, padx=20, pady=7)
    Botão_plotar_freq=tk.CTkButton(frame_func_coleta, text='Plotagem Dados \n de Frequencia', width=160, height=40, font=("Helvetica", 15),command=C_Frequencia)
    Botão_plotar_freq.grid(row=7, column=0, padx=20, pady=7)
    Botão_plotar_todos=tk.CTkButton(frame_func_coleta, text='Plotar Todos \n os Dados ', width=160, height=40, font=("Helvetica", 15),command=C_todos)
    Botão_plotar_todos.grid(row=8, column=0, padx=20, pady=7)

    ####MENU PARA PLOTAGEM A PARTIR DO TXT ######

    ####MENU PARA PLOTAGEM A PARTIR DO EXCEL ######
    titulo_frame = tk.CTkLabel(frame_func_excel, text='Menu Excel:', font=("Helvetica", 20))
    titulo_frame.grid(row=0, column=0, padx=10, pady=7)
    Botão_plotar_potencia=tk.CTkButton(frame_func_excel, text='Plotagem Dados \n De Potencia', width=160, height=40, font=("Helvetica", 15),command=E_potencia)
    Botão_plotar_potencia.grid(row=1, column=0, padx=20, pady=7)
    Botão_plotar_THD=tk.CTkButton(frame_func_excel, text='Plotagem Dados \n de THD', width=160, height=40, font=("Helvetica", 15),command=E_THD)
    Botão_plotar_THD.grid(row=2, column=0, padx=20, pady=7)
    Botão_plotar_variacao=tk.CTkButton(frame_func_excel,  text='Plotagem Dados \n de Δ Tensão', width=160, height=40, font=("Helvetica", 15),command=E_Variação)
    Botão_plotar_variacao.grid(row=3, column=0, padx=20, pady=7)
    Botão_plotar_interrupcao=tk.CTkButton(frame_func_excel, text='Plotagem Dados \n de Interrupção', width=160, height=40, font=("Helvetica", 15),command=E_Interupção)
    Botão_plotar_interrupcao.grid(row=4, column=0, padx=20, pady=7)
    Botão_plotar_FFT=tk.CTkButton(frame_func_excel,text='Plotagem Dados \n de FFT', width=160, height=40, font=("Helvetica", 15),command=E_FFT)
    Botão_plotar_FFT.grid(row=5, column=0, padx=20, pady=7)
    Botão_plotar_Grandezas=tk.CTkButton(frame_func_excel, text='Plotagem Dados \n das Grandezas', width=160, height=40, font=("Helvetica", 15),command=E_Grandezas)
    Botão_plotar_Grandezas.grid(row=6, column=0, padx=20, pady=7)
    Botão_plotar_freq=tk.CTkButton(frame_func_excel, text='Plotagem Dados \n de Frequencia', width=160, height=40, font=("Helvetica", 15),command=E_Frequencia)
    Botão_plotar_freq.grid(row=7, column=0, padx=20, pady=7)
    Botão_plotar_todos=tk.CTkButton(frame_func_excel, text='Plotar Todos \n os Dados ', width=160, height=40, font=("Helvetica", 15),command=E_Todos)
    Botão_plotar_todos.grid(row=8, column=0, padx=20, pady=5)
    ####MENU PARA PLOTAGEM A PARTIR DO EXCEL ######

    ####CONFIGURAÇÃO CHAT E BOTÃO LIMPAR ######
    global saida_terminal
    saida_terminal = tk.CTkTextbox(frame_Chat, height=int(altura_total * 1.31), width=int(largura_total *4.33), wrap=tk.WORD)
    saida_terminal.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
    texto = ('Instruções:\n\n'
            '-> A BaundRate de recepção deve ser igual a BaundRate de coleta do sinal.\n\n'
            '-> A frequencia de conversão indicada, é definida por fase.\n\n'
            '-> O processo de armazenamento dos dados da FFT é EXTREMAMENTE demorado.\n\n'
            '-> Crie um novo arquivo excel, sempre que for armazenar novos dados.\n\n'
            '-> Configurar o numeros de amostra por linha para 1/4 do numero de amostras por segundo.\n     Exemplos:\n      1) Para 40000Hz -10000 amostras por linha.\n      2) Para 2000Hz - 500 amostras por linha.\n\n'
            '-> Os cronometros devem ser pausados após plotagem dos dados.\n\n'
            'Formato das entradas:\n\n'
            'OBS: Considerando uma configuração de BRR de 1000000, com taxa de amostragem por fase de 40000 Hz, utilizando a porta usb "com4", em uma rede 220/127V em que deseja-se coletar dados por 1 mim.\n\n'
            '-> BaundRate. Ex: "1000000".\n\n'
            '-> Frequencia. Ex: "10000".\n\n'
            '-> Porta. Ex: "COM4".\n\n'
            '-> Tensão de fase. Ex:"127".\n\n'
            '-> Tempo de coleta(s). Ex: "60".\n\n'
            '-> Nº de amostras p/ linha. Ex: "10000".\n\n'
            'Caracteres de identificação para envio:\n\n'
            '-> Tensão Fase A - !.\n\n'
            '-> Tensão Fase B - @.\n\n'
            '-> Tensão Fase C - #.\n\n'
            '-> Corrente Fase A - &.\n\n'
            '-> Corrente Fase B - %.\n\n'
            '-> Corrente Fase C - ?.\n\n'
            '-> FP Fase A - <.\n\n' 
            '-> FP Fase B - >.\n\n'
            '-> FP Fase C - *.\n\n'
            '-> Separador -. \n')
    saida_terminal.insert(tk.END,texto )
    frm_limpar = tk.CTkFrame(Programa, width=300, height=480)
    frm_limpar.place(x=int(largura_total *5.7), y=int(altura_total * 4.5))
    Botão_limpar=tk.CTkButton(frm_limpar, text='LIMPAR',command=limpar)
    Botão_limpar.grid(row=1, column=0, padx=0, pady=0)
    ####CONFIGURAÇÃO CHAT E BOTÃO LIMPAR ######

    ####CONFIGURAÇÃO TEMPORIZADORES######
    global saida_terminal_pot , saida_terminal_THD ,saida_terminal_variação,saida_terminal_Interrupção,saida_terminal_FFT,saida_terminal_Tempo,saida_terminal_freque
    saida_terminal_Tempo= tk.CTkTextbox(frame_indices, height=int(altura_total * 0.15), width=int(largura_total * 1.41), wrap=tk.WORD)
    saida_terminal_Tempo.grid(row=0, column=0, columnspan=2, padx=5, pady=4)
    saida_terminal_pot = tk.CTkTextbox(frame_indices, height=int(altura_total * 0.15), width=int(largura_total * 1.41), wrap=tk.WORD)
    saida_terminal_pot.grid(row=1, column=0, columnspan=2, padx=5, pady=4)
    saida_terminal_THD = tk.CTkTextbox(frame_indices, height=int(altura_total * 0.15), width=int(largura_total * 1.41), wrap=tk.WORD)
    saida_terminal_THD.grid(row=2, column=0, columnspan=2, padx=5, pady=4)
    saida_terminal_variação = tk.CTkTextbox(frame_indices, height=int(altura_total * 0.15), width=int(largura_total * 1.41), wrap=tk.WORD)
    saida_terminal_variação.grid(row=3, column=0, columnspan=2, padx=5, pady=4)
    saida_terminal_Interrupção = tk.CTkTextbox(frame_indices, height=int(altura_total * 0.15), width=int(largura_total * 1.41), wrap=tk.WORD)
    saida_terminal_Interrupção.grid(row=4, column=0, columnspan=2, padx=5, pady=4)
    saida_terminal_FFT = tk.CTkTextbox(frame_indices, height=int(altura_total * 0.15), width=int(largura_total * 1.41), wrap=tk.WORD)
    saida_terminal_FFT.grid(row=5, column=0, columnspan=2, padx=5, pady=4)
    saida_terminal_freque = tk.CTkTextbox(frame_indices, height=int(altura_total * 0.15), width=int(largura_total * 1.41), wrap=tk.WORD)
    saida_terminal_freque.grid(row=6, column=0, columnspan=2, padx=5, pady=4)
    Botão_stop_0=tk.CTkButton(frame_indices, text='⏸️', width=23, height=23, font=("Helvetica", 15),command=lambda: monitorar_botao(evento_parar0))
    Botão_stop_0.place(x=251,y=125)
    Botão_stop_1=tk.CTkButton(frame_indices, text='⏸️', width=23, height=23, font=("Helvetica", 15),command=lambda: monitorar_botao(evento_parar1))
    Botão_stop_1.place(x=251,y=86)
    Botão_stop_2=tk.CTkButton(frame_indices, text='⏸️', width=23, height=23, font=("Helvetica", 15),command=lambda: monitorar_botao(evento_parar2))
    Botão_stop_2.place(x=251,y=47)
    Botão_stop_3=tk.CTkButton(frame_indices, text='⏸️', width=23, height=23, font=("Helvetica", 15),command=lambda: monitorar_botao(evento_parar3))
    Botão_stop_3.place(x=251,y=164)
    Botão_stop_4=tk.CTkButton(frame_indices, text='⏸️', width=23, height=23, font=("Helvetica", 15),command=lambda: monitorar_botao(evento_parar4))
    Botão_stop_4.place(x=251,y=203)
    Botão_stop_5=tk.CTkButton(frame_indices, text='⏸️', width=23, height=23, font=("Helvetica", 15),command=lambda: monitorar_botao(evento_parar5))
    Botão_stop_5.place(x=251,y=242)
    ####CONFIGURAÇÃO TEMPORIZADORES######

    ####CONFIGURAÇÃO TERMINAL FREQUENCIA######
    global saida_terminal_freq
    frm_freq = tk.CTkFrame(Programa)
    frm_freq.place(x=int(largura_total *3.3), y=int(altura_total * 3.12))
    saida_terminal_freq= tk.CTkTextbox(frm_freq, height=int(altura_total * 0.15), width=int(largura_total * 0.41), wrap=tk.WORD)
    saida_terminal_freq.grid(row=0, column=0, padx=3, pady=3)

    frm_sequencia = tk.CTkFrame(Programa, width=100, height=100)
    frm_sequencia.place(x=int(largura_total *3.76), y=int(altura_total * 3.125))
    botão_sequencia=tk.CTkButton(frm_sequencia, text='Sequêcia De Fase',command=Sequencia, font=("Helvetica",15))
    botão_sequencia.grid(row=0, column=0, padx=3, pady=3) 
    ####CONFIGURAÇÃO TERMINAL FREQUENCIA######

    if getattr(sys, 'frozen', False):
        # Executando a partir do executável
        base_path = sys._MEIPASS
    else:
        # Executando a partir do código-fonte
        base_path = os.path.dirname(__file__)

    # Adicionar ícone da janela
    caminho_arquivo_icone1 = os.path.join(base_path, 'icon.ico')
    Programa.iconbitmap(caminho_arquivo_icone1)

    # Caminho para a imagem
    caminho_arquivo_icone2 = os.path.join(base_path, 'icon.png')

  
    # Carregar e redimensionar a imagem
    logo = Image.open(caminho_arquivo_icone2)
    logo = logo.resize((194, 240), Image.Resampling.LANCZOS)

    # Converter a imagem para o formato que o Label pode usar
    #tk_logo = ImageTk.PhotoImage(logo)

    # Criar um Label para a imagem e adicioná-lo ao Frame
    #label_imagem = Tk.Label(Programa, image=tk_logo)
    #label_imagem.place(x=10,y=20)
    #label_imagem.image = tk_logo


    ####CONFIGURAÇÃO INFORMAÇÕES DEV ######
    titulo_frame = tk.CTkLabel(frame_Dev, text='Dev by: Gabriel Vicente Barbosa da Silva')
    titulo_frame.grid(row=0, column=0, padx=10)
    titulo_frame = tk.CTkLabel(frame_Dev, text='Versão: 00-22/07/2024')
    titulo_frame.grid(row=0, column=2,padx=(785, 10))
    ####CONFIGURAÇÃO INFORMAÇÕES DEV ######

    ###Configuração Grafico do tempo real#####
    global canvas
    canvas = FigureCanvasTkAgg(Grafico, master=frame_Grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    toolbar = NavigationToolbar2Tk(canvas,frame_Grafico)
    toolbar.update()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    frm_play_stop = tk.CTkFrame(Programa, width=100, height=100)
    frm_play_stop.place(x=int(largura_total *7.18), y=int(altura_total * 3.13))
    botão_play_stop=tk.CTkButton(frm_play_stop, text='⏸️',command=play_pause, font=("Helvetica",20))
    botão_play_stop.grid(row=1, column=0, padx=0, pady=0)
    frm_mais = tk.CTkFrame(Programa)
    frm_mais.place(x=int(largura_total *7), y=int(altura_total * 3.13))
    botão_mais=tk.CTkButton(frm_mais, text='+', width=28, height=28, font=("Helvetica", 15),command=zoom_mais)
    botão_mais.grid(row=1, column=0, padx=0, pady=0)
    frm_menos = tk.CTkFrame(Programa)
    frm_menos.place(x=int(largura_total *6.82), y=int(altura_total * 3.13))
    botão_menos=tk.CTkButton(frm_menos, text='-', width=28, height=28, font=("Helvetica", 15),command=zoom_menos)
    botão_menos.grid(row=1, column=0, padx=0, pady=0)
    ###Configuração Grafico do tempo real#####

   
    sys.stdout = Redirecionar_mensagem(saida_terminal)
 ###Configuração da janela#####
    Programa.resizable(False,False)
    Programa.bind('<Configure>', config_frame)
    ###Configuração da janela#####
    Programa.mainloop()
if __name__ == "__main__":
    criar_interface()
