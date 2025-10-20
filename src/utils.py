# funções de ajuda (salvar frames, calcular acurácia)
def gerar_tabela_markdown(nome_arquivo, frames_ref, frames_hist_local, frames_bic, header=None):
    """
    Gera um arquivo .md com uma tabela contendo as colunas Referencia, Histograma Local e BIC,
    mesmo quando as listas têm tamanhos diferentes.

    :param nome_arquivo: Nome do arquivo Markdown a ser gerado.
    :param frames_ref: Lista de frames de referência.
    :param frames_hist_local: Lista de frames detectados pelo histograma local.
    :param frames_bic: Lista de frames detectados pelo método BIC.
    :param header: Texto opcional para o cabeçalho do arquivo Markdown.
    """
    # Determina o tamanho máximo entre as listas
    max_len = max(len(frames_ref), len(frames_hist_local), len(frames_bic))

    # Preenche as listas menores com strings vazias
    frames_ref = frames_ref + [""] * (max_len - len(frames_ref))
    frames_hist_local = frames_hist_local + [""] * (max_len - len(frames_hist_local))
    frames_bic = frames_bic + [""] * (max_len - len(frames_bic))

    with open(nome_arquivo, 'w') as arquivo:
        if header:
            arquivo.write(f"{header}\n\n")

        # Escreve o cabeçalho da tabela
        arquivo.write("| Referencia | Histograma Local | BIC |\n")
        arquivo.write("|------------|------------------|-----|\n")

        # Escreve os dados na tabela
        for ref, hist, bic in zip(frames_ref, frames_hist_local, frames_bic):
            arquivo.write(f"| ![[{ref}]] | ![[{hist}]] | ![[{bic}]] |\n")

    print(f"Tabela Markdown gerada com sucesso: {nome_arquivo}")

def acuracia (frames_ref, frames_detected):
        """
        Calcula a acurácia de detecção de cenas.

        :param frames_ref: Lista de frames de referência.
        :param frames_detected: Lista de frames detectados.
        :return: Acurácia como uma porcentagem.
        """
        verdadeiros_positivos = len(set(frames_ref) & set(frames_detected))
        total_referencias = len(frames_ref)

        if total_referencias == 0:
            return 0.0

        acuracia = (verdadeiros_positivos / total_referencias) * 100
        return acuracia

# ...existing code...
def acuracia(frames_ref, frames_detected, frame_rate=30):
    """
    Calcula a acurácia de detecção de cenas.

    :param frames_ref: Lista de frames de referência.
    :param frames_detected: Lista de frames detectados.
    :param frame_rate: Tolerância em número de frames (inteiro >= 0).
    :return: Acurácia como uma porcentagem.
    """
    if not frames_ref:
        return 0.0

    # Mantém compatibilidade com comportamento anterior quando frame_rate == 0
    if not frame_rate:
        verdadeiros_positivos = len(set(frames_ref) & set(frames_detected))
        return (verdadeiros_positivos / len(frames_ref)) * 100

    # Garante listas mutáveis e ordenadas (não obrigatório, mas facilita lógica)
    refs = list(frames_ref)
    detected = list(frames_detected)
    matched = [False] * len(detected)
    verdadeiros_positivos = 0

    for ref in refs:
        for i, det in enumerate(detected):
            if not matched[i]:
                try:
                    # assume valores numéricos; se não, convertendo pode falhar
                    if abs(int(det) - int(ref)) <= int(frame_rate):
                        matched[i] = True
                        verdadeiros_positivos += 1
                        break
                except Exception:
                    # se conversão falhar, pula este par
                    continue

    return (verdadeiros_positivos / len(refs)) * 100