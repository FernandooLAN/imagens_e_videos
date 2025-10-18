import numpy as np
import cv2
from descritors_utils import *

def gerar_histograma_local(img: np.array) -> np.array:
    """
    Gera um histograma local e retorna um vetor com histograma de cor
    """
    q_img = quantizar_imagem(img)

    # A partir daqui, otimizei com código reaproveitado do BIC
    mapped_img, valid_mask = mapeia_quantizacao(q_img)
    
    histograma = np.bincount(mapped_img[valid_mask], minlength=64)

    if len(histograma) > 64: histograma = histograma[:64]

    return histograma

def gerar_histograma_local_com_particao(retangulo_interno, retangulo_externo):
    hist1 = gerar_histograma_local(retangulo_interno)
    hist2 = gerar_histograma_local(retangulo_externo)

    return np.concatenate((hist1, hist2))

""" Exemplo de uso
imagem = cv2.imread("deserto1.jpg")
interno, externo = particao_retangulo_central(imagem)

histograma1 = gerar_histograma_local_com_particao(interno, externo)

imagem = cv2.imread("deserto2.jpg")
interno, externo = particao_retangulo_central(imagem)

histograma2 = gerar_histograma_local_com_particao(interno, externo)

distancia = dLog(histograma1, histograma2)
print(distancia)
"""