import numpy as np
import cv2
from descriptors.descritors_utils import *

def gerar_histograma_local(img: np.array) -> np.array:
    """
    Gera um histograma local e retorna um vetor com histograma de cor
    """
    img_quantizada = quantizar_imagem(img)

    histograma = np.zeros((64,), dtype=int)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            histograma[mapeia_quantizacao(img_quantizada[i,j])] += 1 
    
    return histograma