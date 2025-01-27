Programa de Coleta e Armazenamento de Dados para sistemas trifasicos de energia

Este repositório contém um programa para coleta, processamento, armazenamento  e apresentação de dados para uma rede de distribuição de energia trifasica.


![image](https://github.com/user-attachments/assets/0006180c-bcd6-4159-90c7-e7dad1acc008)


🛠️ Funcionalidades

    Recepção de dados de tensão, corrente e fator de potencia, para uma rede trifasica;
    
    Representação grafica dos sinais de tensão e corrente em tempo real;
    Calculo e representação grafica dos dados de potencia ativa, reativa, aparente e fator de potencia para os dados coletados;
    Calculo e representação grafica dos dados de variação de tensão instantanea;
    Calculo e representação grafica dos dados de  tempo de interrupção nos sinais de tensão;
    Calculo e representação grafica dos dados da Transformada rapida de Fourier(FFT);
    Calculo e representação grafica dos dados de variação da frequencia fundamental;
    
    OBS: É possivel armanezar todos os dados em um arquivo excel e posteriomente voltar a plotar a representação grafica a partir do mesmo.

📋 Instruções
Configuração Inicial

    Certifique-se de que a BaudRate de recepção seja igual à de coleta do sinal.
    A frequência de conversão deve ser definida por fase.
    Crie um novo arquivo Excel sempre que armazenar novos dados.
    Configure o número de amostras por linha como 1/4 do número de amostras por segundo.
        Exemplos:
            Para 40.000 Hz: 10.000 amostras por linha.
            Para 2.000 Hz: 500 amostras por linha.
    Pause os cronômetros após a plotagem dos dados.

Formato das Entradas

    BaudRate: Exemplo: 1000000
    Frequência de amostragem: Exemplo: 10000
    Porta USB: Exemplo: COM4
    Tensão de fase: Exemplo: 127
    Tempo de coleta (segundos): Exemplo: 60
    Número de amostras por linha: Exemplo: 10000

⚠️ Observações Importantes

    O processo de armazenamento dos dados da FFT é EXTREMAMENTE demorado.
    Configure corretamente as entradas para evitar erros durante a coleta.

🔑 Caracteres de Identificação para Envio
Sinal	Caractere
Tensão Fase A	!
Tensão Fase B	@
Tensão Fase C	#
Corrente Fase A	&
Corrente Fase B	%
Corrente Fase C	?
FP Fase A	<
FP Fase B	>
FP Fase C	*
Separador	-

🛡️ Licença

Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais detalhes.
