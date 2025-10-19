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