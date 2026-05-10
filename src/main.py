import time
import csv
import cv2
import numpy as np
from pathlib import Path

from descriptors.Bic import gerar_histograma_bic_com_particao
from descriptors.descritors_utils import particao_retangulo_central, dLog


def coleta_baseline_video_completo(caminho_video: Path, arquivo_csv_saida: Path, percent: float = 0.1):
    """
    Processa um vídeo completo e calcula a latência média do algoritmo BIC
    (Partição de Retângulo Central) em blocos sequenciais de 30 frames.

    Os resultados são exportados para um arquivo CSV, registrando as
    configurações como metadados essenciais.
    """
    video = cv2.VideoCapture(str(caminho_video))

    if not video.isOpened():
        print(f"Erro ao abrir o vídeo: {caminho_video}")
        return

    tamanho_bloco = 30
    histBic_passado = np.zeros(256)

    cabecalho = ["run", "cenario", "carga", "metrica", "valor", "unidade", "timestamp", "obs"]
    dados_coletados = []

    print(f"Iniciando coleta: {caminho_video.name}")

    run_atual = 1

    while True:
        # Etapa de Leitura (I/O)
        bloco_de_imagens = []

        for _ in range(tamanho_bloco):
            ret, frame = video.read()
            if not ret:
                break
            bloco_de_imagens.append(frame)

        if len(bloco_de_imagens) < tamanho_bloco:
            print(f"Fim do vídeo; {run_atual - 1} blocos completos processados.")
            break

        cenas_detectadas_no_bloco = 0

        # Etapa de Processamento
        inicio_bloco = time.perf_counter()

        for frame in bloco_de_imagens:
            interno, externo = particao_retangulo_central(frame, percent)
            histBic = gerar_histograma_bic_com_particao(interno, externo)
            difBic = dLog(histBic_passado, histBic)
            histBic_passado = histBic

        fim_bloco = time.perf_counter()

        # Processamento dos Dados
        tempo_total_bloco_ms = (fim_bloco - inicio_bloco) * 1000
        tempo_medio_frame_ms = tempo_total_bloco_ms / tamanho_bloco
        timestamp_atual = time.strftime("%H:%M:%S")

        registro = [
            run_atual,
            "BIC_Retangulo_Central",
            caminho_video.name,
            "Tempo",
            round(tempo_medio_frame_ms, 3),
            "ms",
            timestamp_atual,
            f"percent={percent} | cortes={cenas_detectadas_no_bloco}"
        ]

        dados_coletados.append(registro)
        print(f"Bloco {run_atual} processado: {tempo_medio_frame_ms:.3f} ms/frame")

        run_atual += 1

    video.release()

    # Escrita dos Dados Brutos
    with open(arquivo_csv_saida, mode='w', newline='') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow(cabecalho)
        escritor.writerows(dados_coletados)

    print(f"Coleta finalizada. Dados salvos em: {arquivo_csv_saida}")


if __name__ == "__main__":
    VIDEO_BASELINE = Path("data/videos/minecraft_trailer.mp4")
    ARQUIVO_SAIDA = Path("baseline.csv")

    coleta_baseline_video_completo(
        caminho_video=VIDEO_BASELINE,
        arquivo_csv_saida=ARQUIVO_SAIDA,
        percent=0.2
    )