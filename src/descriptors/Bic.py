import numpy as np
import cv2
from descriptors.descritors_utils import * 

def pixels_borda_interior(imagem):
    """
    Retorna duas listas de pixels de borda e pixels de interior
    """
    borda = []
    interior = []

    # Os primeiros dois loops adicionam as bordas da imagem na lista de borda
    for i in [0, imagem.shape[0]-1]:
        for j in range(0, imagem.shape[1]):
            borda.append((i,j))

    for i in range(1, imagem.shape[0]-1):
        for j in [0, imagem.shape[1]-1]:
            borda.append((i,j))

    # Faz a verificação de pixels de borda e interior
    for i in range(1, imagem.shape[0]-1):
        for j in range(1, imagem.shape[1]-1):
            eh_borda = (
                np.any(imagem[i, j] != imagem[i - 1, j]) or
                np.any(imagem[i, j] != imagem[i, j - 1]) or
                np.any(imagem[i, j] != imagem[i, j + 1]) or
                np.any(imagem[i, j] != imagem[i + 1, j])
            )
            if eh_borda:
                borda.append((i,j))
            else:
                interior.append((i,j))
    
    return borda, interior

def gerar_histograma_bic(imagem: np.array) -> np.array:
    """
    Retorna um array concatenado dos histogramas de borda e interior
    """
    # Processo de quantização e determinação dos pixels de borda e interior
    img_edges = quantizar_imagem(imagem)
    borda, interior = pixels_borda_interior(img_edges)

    # Criação dos histogramas 
    borda_histograma = np.zeros((64,), dtype=int)
    interior_histograma = np.zeros((64,), dtype=int)

    # Histograma de borda
    for i,j in borda:
        borda_histograma[mapeia_quantizacao(img_edges[i,j])] += 1 

    # Histograma de interior
    for i,j in interior:
        interior_histograma[mapeia_quantizacao(img_edges[i,j])] += 1        

    hist = np.concatenate((borda_histograma, interior_histograma))

    return hist
