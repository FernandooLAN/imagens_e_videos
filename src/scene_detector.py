# Importa funções para gerar histogramas e utilitários necessários
from descriptors.Bic import gerar_histograma_bic_com_particao
from descriptors.HistogramaLocal import gerar_histograma_local_com_particao
from descriptors.descritors_utils import particao_retangulo_central, dLog
import cv2
import sys
import numpy as np

# Obtém os argumentos de linha de comando: nome do vídeo, arquivo de registro e limiar
nome_do_video = sys.argv[1]
registro = sys.argv[2]

# Lê os frames de referência do arquivo de registro
with open(registro, "r") as arquivo:
    conteudo = arquivo.read().strip()
    frames_ref = [int(x) for x in conteudo.split(",")]
threshold = float(sys.argv[3])

# Abre o vídeo para leitura
video = cv2.VideoCapture(nome_do_video)

# Verifica se o vídeo foi aberto corretamente
if not video.isOpened():
    print("Erro ao abrir o vídeo.")
    exit()

# Inicializa variáveis para controle de frames e salto entre eles
numero_do_frame = 0  
salto = int(video.get(cv2.CAP_PROP_FPS))

# Listas para armazenar os frames detectados pelos métodos BIC e Histograma Local
frames_registrados_BIC = []  
frames_registrados_HistLocal = []

# Inicializa os histogramas passados como zeros
histBic_passado, histLocal_passado = np.zeros(256), np.zeros(128)

# Loop principal para processar os frames do vídeo
while True:
    # Define o frame atual a ser lido
    video.set(cv2.CAP_PROP_POS_FRAMES, numero_do_frame)

    # Lê o frame atual
    ret, frame = video.read()
    # Verifica se o frame foi lido corretamente
    if not ret:
        break
    
    # Divide o frame em regiões interna e externa
    interno, externo = particao_retangulo_central(frame)

    # Gera os histogramas BIC e Local para as regiões
    histBic = gerar_histograma_bic_com_particao(interno, externo)
    histLocal = gerar_histograma_local_com_particao(interno, externo)

    # Calcula as diferenças entre os histogramas atuais e os anteriores
    difBic = dLog(histBic_passado, histBic)
    difLocal = dLog(histLocal_passado, histLocal)

    # Verifica se a diferença BIC excede o limiar e registra o frame
    if difBic > threshold:
        frames_registrados_BIC.append(numero_do_frame)
        histBic_passado = histBic

    # Verifica se a diferença Local excede o limiar e registra o frame
    if difLocal > threshold:
        frames_registrados_HistLocal.append(numero_do_frame)
        histLocal_passado = histLocal

    # Incrementa o número do frame pelo valor do salto
    numero_do_frame += salto    
    print(f"Frame {numero_do_frame} processado.")

# Determina o número máximo de linhas para a saída
n_row = max(len(frames_registrados_BIC), len(frames_registrados_HistLocal), len(frames_ref))

# Imprime os resultados em formato tabular
print("bic\thist\tref")
for i in range(n_row):  
    print(
        (str(frames_registrados_BIC[i]) if i < len(frames_registrados_BIC) else "") + "\t" +
        (str(frames_registrados_HistLocal[i]) if i < len(frames_registrados_HistLocal) else "") + "\t" +
        (str(frames_ref[i]) if i < len(frames_ref) else "")
    )

# Libera os recursos do vídeo e fecha as janelas abertas
video.release()
cv2.destroyAllWindows()