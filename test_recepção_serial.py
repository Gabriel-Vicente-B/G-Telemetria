import serial
import threading
import keyboard

# Configurações da porta serial
port = 'COM5'  # Substitua pelo nome da sua porta serial
baudrate = 2000000  # Verifique a taxa de transmissão

# Função para receber dados da porta serial
def receive_data(ser):
    while not stop_event.is_set():  # Verifica se o evento de parada não foi acionado
        if ser.in_waiting > 0:  # Verifica se há dados para ler
            data = ser.readline().decode('utf-8').strip()  # Lê e decodifica os dados
            if data:
                print(f"Dados recebidos: {data}")

# Cria um evento para sinalizar a parada
stop_event = threading.Event()

try:
    ser = serial.Serial(port, baudrate, timeout=1)
    ser.flushInput()  # Limpa o buffer de entrada da serial
    print(f"Conectado à porta {port} com baudrate {baudrate}")

    # Inicia a thread de recepção
    receive_thread = threading.Thread(target=receive_data, args=(ser,))
    receive_thread.start()

    print("Pressione 'Esc' para interromper a recepção.")

    # Loop principal para controle
    keyboard.wait('esc')  # Espera até que a tecla 'Esc' seja pressionada
    stop_event.set()  # Aciona o evento de parada

except serial.SerialException as e:  # pyserial deve estar instalado para isso funcionar
    print(f"Erro ao tentar abrir a porta serial: {e}")
    exit(1)

finally:
    # Aguarda a thread de recepção finalizar
    receive_thread.join()
    if ser.is_open:
        ser.close()
    print("Conexão serial fechada.")