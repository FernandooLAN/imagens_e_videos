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

def particao_retangulo_central(image: np.array, percent: float = 0.1):
    """
    Cria duas partições, uma com o retângulo interior e outra com o retângulo exterior

    O retângulo exterior possui o mesmo tamanho da imagem original, mas possui valor -1
    """
    y1 = int(image.shape[0] * percent)
    y2 = int(image.shape[0] * (1 - percent))

    x1 = int(image.shape[1] * percent)
    x2 = int(image.shape[1] * (1 - percent))

    retangulo_interno = image[y1:y2, x1:x2]
    retangulo_externo = image.copy().astype(int)

    for i in range(y1, y2):
        for j in range(x1, x2):
            retangulo_externo[i,j] = (-1,-1,-1)

    return retangulo_interno, retangulo_externo

def mapeia_quantizacao(q_img):
    """
    Mapeia a imagem quantizada (3 canais) para uma imagem de 1 canal (bins 0-63).
    Retorna a imagem mapeada e uma máscara de pixels válidos.
    """
    # Cria uma máscara para pixels válidos (ignorando o marcador -1)
    # q_img[..., 0] pega o primeiro canal (ex: Azul) de todos os pixels
    valid_mask = (q_img[..., 0] != -1)
    
    # Cria uma imagem de saída, preenchida com -1 (nosso marcador)
    mapped_img = np.full((q_img.shape[0], q_img.shape[1]), -1, dtype=np.int32)
    
    # Pega apenas os pixels válidos para o cálculo
    valid_pixels = q_img[valid_mask]
    
    # --- ESTA É A LÓGICA QUE EU ASSUMI ---
    # Mapeia BGR (4x4x4) para um bin de 0-63
    # B*16 + G*4 + R
    mapped_bins = (valid_pixels[..., 0] * 16 +
                   valid_pixels[..., 1] * 4 +
                   valid_pixels[..., 2])
    # --- FIM DA LÓGICA ASSUMIDA ---

    # Coloca os bins calculados de volta na imagem de saída,
    # apenas nas posições válidas
    mapped_img[valid_mask] = mapped_bins
    
    return mapped_img, valid_mask
