import serial
import os

def excluir_arquivos(caminho):
    if os.path.exists(caminho):
        os.remove(caminho)

def coleta_amostras(porta, baudrate,num_de_amostras_por_linha,con):
    try:
        val_recep = serial.Serial(port=porta, baudrate=baudrate)
        if con:
            con.send(f"A porta '{porta}' foi aberta com baudrate de {baudrate}.")
    except Exception as e:
        if con:
            con.send(f"Erro na abertura da porta: {e}.")
        return
    # Indicadores dos sinais
    s_va, s_vb, s_vc, s_ia, s_ib, s_ic, s_fp_A, s_fp_B, s_fp_C, s_sep = '!', '@', '#', '&', '%', '?', '<', '>', '*', '\n'
    num_de_amostras_por_linha=int(num_de_amostras_por_linha)
    num_max_amostras = 50000000
    num_max_amostras_fp = 500000

    # Caminho do diretório
    diretorio_arquivo = os.path.dirname(os.path.abspath(__file__))
    
    # excluindo arquivos
    excluir_arquivos(os.path.join(diretorio_arquivo, 'Tensão_A.txt'))
    excluir_arquivos(os.path.join(diretorio_arquivo, 'Tensão_B.txt'))
    excluir_arquivos(os.path.join(diretorio_arquivo, 'Tensão_C.txt'))
    excluir_arquivos(os.path.join(diretorio_arquivo, 'Corrente_A.txt'))
    excluir_arquivos(os.path.join(diretorio_arquivo, 'Corrente_B.txt'))
    excluir_arquivos(os.path.join(diretorio_arquivo, 'Corrente_C.txt'))
    excluir_arquivos(os.path.join(diretorio_arquivo, 'FP_A.txt'))
    excluir_arquivos(os.path.join(diretorio_arquivo, 'FP_B.txt'))
    excluir_arquivos(os.path.join(diretorio_arquivo, 'FP_C.txt'))
    # excluindo arquivos

    # Inicialização de arquivos
    arquivos = {
        'Tensão_A': open(os.path.join(diretorio_arquivo, 'Tensão_A.txt'), "w+"),
        'Tensão_B': open(os.path.join(diretorio_arquivo, 'Tensão_B.txt'), "w+"),
        'Tensão_C': open(os.path.join(diretorio_arquivo, 'Tensão_C.txt'), "w+"),
        'Corrente_A': open(os.path.join(diretorio_arquivo, 'Corrente_A.txt'), "w+"),
        'Corrente_B': open(os.path.join(diretorio_arquivo, 'Corrente_B.txt'), "w+"),
        'Corrente_C': open(os.path.join(diretorio_arquivo, 'Corrente_C.txt'), "w+"),
        'FP_A': open(os.path.join(diretorio_arquivo, 'FP_A.txt'), "w+"),
        'FP_B': open(os.path.join(diretorio_arquivo, 'FP_B.txt'), "w+"),
        'FP_C': open(os.path.join(diretorio_arquivo, 'FP_C.txt'), "w+")
    }
    
    # Contadores
    contadores = {
        'Tensão_A': 0,
        'Tensão_B': 0,
        'Tensão_C': 0,
        'Corrente_A': 0,
        'Corrente_B': 0,
        'Corrente_C': 0,
        'FP_A': 0,
        'FP_B': 0,
        'FP_C': 0
    }
    
    cont_VI = 0
    cont_FP = 0

    def limpar_primeiras_linhas(arquivo, num_linhas_para_limpar):
        with open(arquivo.name, 'r') as f:
            linhas = f.readlines()
        with open(arquivo.name, 'w') as f:
            f.writelines(linhas[num_linhas_para_limpar:])

    while True:
        try:
            valor = val_recep.read(1).decode()
        except Exception as e:
            if con:
                con.send(f"Erro ao ler dados: {e}")
            break
        
        tipo_dado = {
            s_va: 'Tensão_A',
            s_vb: 'Tensão_B',
            s_vc: 'Tensão_C',
            s_ia: 'Corrente_A',
            s_ib: 'Corrente_B',
            s_ic: 'Corrente_C',
            s_fp_A: 'FP_A',
            s_fp_B: 'FP_B',
            s_fp_C: 'FP_C'
        }

        if valor in tipo_dado:
            tipo = tipo_dado[valor]
            amostra = ''
            while True:
                amostra += val_recep.read(1).decode(errors='ignore')
                if s_sep in amostra:
                    if contadores[tipo] < num_de_amostras_por_linha:
                        arquivos[tipo].write((amostra.strip().replace(valor, '').replace(s_sep, '') + ','))
                        #print(amostra)
                        contadores[tipo] += 1
                        if tipo in ['Tensão_A', 'Tensão_B', 'Tensão_C', 'Corrente_A', 'Corrente_B', 'Corrente_C']:
                            cont_VI += 1
                        elif tipo in ['FP_A', 'FP_B', 'FP_C']:
                            cont_FP += 1
                    if contadores[tipo] == num_de_amostras_por_linha:
                        arquivos[tipo].write('\n')
                        contadores[tipo] = 0
                    break
                 
        if cont_VI >= num_max_amostras:
            for tipo in ['Tensão_A', 'Tensão_B', 'Tensão_C', 'Corrente_A', 'Corrente_B', 'Corrente_C']:
                limpar_primeiras_linhas(arquivos[tipo], num_max_amostras)
            cont_VI = 0
        
        if cont_FP >= num_max_amostras_fp:
            for tipo in ['FP_A', 'FP_B', 'FP_C']:
                limpar_primeiras_linhas(arquivos[tipo], num_max_amostras_fp)
            cont_FP = 0
            