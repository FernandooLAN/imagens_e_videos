import numpy as np
import cv2
from .descritors_utils import * 

# Essa função foi feita manualmente antes, mas como demorava muito, pedi para
# o gemini otimizar
def gerar_histograma_bic(imagem: np.array) -> np.array:
    """
    Retorna um array concatenado dos histogramas de borda e interior,
    calculado de forma vetorizada com NumPy. 
    """
    
    q_img = quantizar_imagem(imagem)
    
    # Cria máscaras 2D (H, W)
    is_border_mask_2d = np.zeros(q_img.shape[:2], dtype=bool)
    is_interior_mask_2d = np.zeros(q_img.shape[:2], dtype=bool)

    # O perímetro da imagem é sempre borda
    is_border_mask_2d[0, :] = True
    is_border_mask_2d[-1, :] = True
    is_border_mask_2d[:, 0] = True
    is_border_mask_2d[:, -1] = True

    # Analisa os pixels centrais (internos)
    # Fatias do centro e seus vizinhos (ainda 3-channel)
    center = q_img[1:-1, 1:-1, :]  # (H-2, W-2, 3)
    up     = q_img[0:-2, 1:-1, :]
    down   = q_img[2:  , 1:-1, :]
    left   = q_img[1:-1, 0:-2, :]
    right  = q_img[1:-1, 2:  , :]

    # Compara o centro com os vizinhos.
    diff_up    = np.any(center != up, axis=2)
    diff_down  = np.any(center != down, axis=2)
    diff_left  = np.any(center != left, axis=2)
    diff_right = np.any(center != right, axis=2)

    # Checa a segunda condição (vizinho é -1)
    neg_up    = (up[..., 0] == -1)
    neg_down  = (down[..., 0] == -1)
    neg_left  = (left[..., 0] == -1)
    neg_right = (right[..., 0] == -1)

    # Combina todas as condições de borda (lógica 'or' é o pipe '|')
    inner_border_mask = (
        diff_up | diff_down | diff_left | diff_right |
        neg_up | neg_down | neg_left | neg_right
    )

    # Atualiza as máscaras 2D principais
    is_border_mask_2d[1:-1, 1:-1] = inner_border_mask
    is_interior_mask_2d[1:-1, 1:-1] = ~inner_border_mask # Interior é o oposto

    # Mapeamento Vetorizado para Bins (0-63)
    mapped_img, valid_mask = mapeia_quantizacao(q_img)
    
    # Pega os valores dos bins (0-63) que são Borda E Válidos
    border_pixels = mapped_img[is_border_mask_2d & valid_mask]
    
    # Pega os valores dos bins (0-63) que são Interior E Válidos
    interior_pixels = mapped_img[is_interior_mask_2d & valid_mask]

    # np.bincount é a forma mais rápida de criar um histograma
    # a partir de índices inteiros.
    borda_histograma = np.bincount(border_pixels, minlength=64)
    interior_histograma = np.bincount(interior_pixels, minlength=64)

    # Garante que o histograma não passe de 64 (caso o mapeamento esteja errado)
    if len(borda_histograma) > 64: borda_histograma = borda_histograma[:64]
    if len(interior_histograma) > 64: interior_histograma = interior_histograma[:64]

    hist = np.concatenate((borda_histograma, interior_histograma))

    return hist.astype(int) # Retorna como int, igual ao seu original

def gerar_histograma_bic_com_particao(retangulo_interno, retangulo_externo):
    hist1 = gerar_histograma_bic(retangulo_interno)
    hist2 = gerar_histograma_bic(retangulo_externo)

    return np.concatenate((hist1, hist2))

""" Exemplo de uso
imagem = cv2.imread("deserto1.jpg")
interno, externo = particao_retangulo_central(imagem)

histograma1 = gerar_histograma_bic_com_particao(interno, externo)

imagem = cv2.imread("madeira1.jpg")
interno, externo = particao_retangulo_central(imagem)

histograma2 = gerar_histograma_bic_com_particao(interno, externo)

# essa é a distância que diz o quão próxima as duas imagens estão
distancia = dLog(histograma1, histograma2)
print(distancia)
"""