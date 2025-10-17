import cv2
import numpy as np

def normalizar_para_255(hist: np.ndarray) -> np.ndarray:
    """
    Normaliza o histograma para valores entre 0 e 255
    """
    # Evita divisão por zero se o histograma estiver todo zerado
    max_value = hist.max()
    
    # Se o histograma estiver vazio, retorna um array de zeros
    if max_value == 0:
        return np.zeros(hist.shape, dtype=float)
    
    # Normalização vetorial
    normalized_hist = (hist.astype(float) / max_value) * 255
    
    return normalized_hist

def f_log(hist: np.ndarray) -> np.ndarray:
    """
    Aplica a função logaritmica da distância dLog
    """
    # Cria um array de zeros para o resultado
    fx = np.zeros(hist.shape, dtype=float)

    for i in range(fx.shape[0]):
        # Valor entre 0 e 1
        if hist[i] > 0 and hist[i] <= 1:
            fx[i] = 1
        # Valor maior que 1
        elif hist[i] > 1:
            fx[i] = np.floor(np.log2(hist[i])) + 1
        
    return fx

def dLog(q_raw: np.ndarray, d_raw: np.ndarray) -> float:
    """
    Retorna a distância dLog entre um histograma Q e D
    """
    # Normaliza os histogramas brutos (raw) para o intervalo [0, 255]
    q_norm = normalizar_para_255(q_raw)
    d_norm = normalizar_para_255(d_raw)
    
    # Aplica a transformação logarítmica f(x)
    f_q = f_log(q_norm)
    f_d = f_log(d_norm)
    
    # 3. Calcula a diferença absoluta e o somatório
    # Fórmula (1): dLog(q, d) = Somatório |f(q[i]) - f(d[i])|
    result = np.abs(f_q - f_d)
    result = np.sum(result)
    
    return float(result)

def quantizar_imagem(imagem):
    """
    Quantiza para uma imagem RGB de 4 x 4 x 4 = 64
    """
    return imagem // 64

def mapeia_quantizacao(pixel_RGB):
    """
    Função que mapeia um pixel quantizado 4x4x4 num histograma com 64 posições
    """
    red = pixel_RGB[0]
    green = pixel_RGB[1] 
    blue = pixel_RGB[2]
    
    return red*16 + green*4 + blue*1