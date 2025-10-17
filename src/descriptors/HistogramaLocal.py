import numpy as np
import cv2

def gerar_histograma_local(img: np.array) -> np.array:
    """
    Gera um histograma local e retorna um vetor com os histogramas de cor concatenados
    """
    red_channel = np.zeros((256,), dtype=int)
    green_channel = np.zeros((256,), dtype=int)
    blue_channel = np.zeros((256,), dtype=int)

    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            blue_channel[img[i,j,0]] += 1
            green_channel[img[i,j,1]] += 1
            red_channel[img[i,j,2]] += 1

    return np.concatenate((red_channel, green_channel, blue_channel))