from textwrap import wrap


def _texto(valor):
    if valor is None:
        return ""
    return str(valor)


def exibir_tabela(cabecalhos, linhas, larguras_maximas=None):
    """Exibe uma tabela ASCII"""
    if not cabecalhos:
        return

    quantidade_colunas = len(cabecalhos)

    for linha in linhas:
        if len(linha) != quantidade_colunas:
            raise ValueError("Todas as linhas devem ter o mesmo número de colunas.")

    if larguras_maximas is None:
        larguras_maximas = [30] * quantidade_colunas

    if len(larguras_maximas) != quantidade_colunas:
        raise ValueError("larguras_maximas deve ter uma largura para cada coluna.")

    conteudo = [cabecalhos] + linhas
    larguras = []

    for indice in range(quantidade_colunas):
        maior = max(len(_texto(linha[indice])) for linha in conteudo)
        largura = min(max(maior, len(_texto(cabecalhos[indice]))), larguras_maximas[indice])
        larguras.append(max(largura, 3))

    separador = "+" + "+".join("-" * (largura + 2) for largura in larguras) + "+"

    def imprimir_linha(valores):
        blocos = []
        altura = 1

        for indice, valor in enumerate(valores):
            texto = _texto(valor)
            partes = wrap(
                texto,
                width=larguras[indice],
                break_long_words=True,
                break_on_hyphens=False,
            ) or [""]
            blocos.append(partes)
            altura = max(altura, len(partes))

        for numero_linha in range(altura):
            celulas = []
            for indice, partes in enumerate(blocos):
                trecho = partes[numero_linha] if numero_linha < len(partes) else ""
                celulas.append(f" {trecho:<{larguras[indice]}} ")
            print("|" + "|".join(celulas) + "|")

    print(separador)
    imprimir_linha(cabecalhos)
    print(separador)

    for linha in linhas:
        imprimir_linha(linha)
        print(separador)
