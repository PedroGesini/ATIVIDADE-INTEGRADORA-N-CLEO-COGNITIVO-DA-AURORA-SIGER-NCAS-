import os
from datetime import datetime
from tabulate import tabulate


ARQUIVO_TXT = "registros_colonia.txt"


# ==========================================
# CADASTRAR REGISTRO
# ==========================================

def cadastrar_registro():

    print("\n")
    print("=" * 70)
    print("                 CADASTRAR REGISTRO")
    print("=" * 70)

    modulo = input("Módulo: ").strip()
    descricao = input("Descrição da ocorrência: ").strip()
    responsavel = input("Responsável: ").strip()

    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    linha = (
        f"[{data}] | "
        f"Módulo: {modulo} | "
        f"Ocorrência: {descricao} | "
        f"Responsável: {responsavel}"
    )

    with open(ARQUIVO_TXT, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha + "\n")

    print("\n" + "-" * 70)
    print("Registro salvo com sucesso!")
    print("-" * 70)


# ==========================================
# CONSULTAR REGISTROS
# ==========================================

def consultar_registros():

    print("\n")
    print("=" * 120)
    print("                    REGISTROS DA COLÔNIA AURORA SIGER")
    print("=" * 120)

    if not os.path.exists(ARQUIVO_TXT):

        print("\nNenhum registro encontrado.")
        return

    with open(ARQUIVO_TXT, "r", encoding="utf-8") as arquivo:

        linhas = [
            linha.strip()
            for linha in arquivo
            if linha.strip()
        ]

    if not linhas:

        print("\nNenhum registro encontrado.")
        return

    tabela = []

    for numero, linha in enumerate(linhas, start=1):

        try:

            data = linha.split("]")[0].replace("[", "").strip()

            modulo = (
                linha.split("Módulo:")[1]
                .split("|")[0]
                .strip()
            )

            ocorrencia = (
                linha.split("Ocorrência:")[1]
                .split("|")[0]
                .strip()
            )

            responsavel = (
                linha.split("Responsável:")[1]
                .strip()
            )

            tabela.append([
                numero,
                data,
                modulo,
                ocorrencia,
                responsavel
            ])

        except (IndexError, ValueError):

            tabela.append([
                numero,
                "N/A",
                "N/A",
                linha,
                "N/A"
            ])

    cabecalho = [
        "ID",
        "Data/Hora",
        "Módulo",
        "Ocorrência",
        "Responsável"
    ]

    print(
        tabulate(
            tabela,
            headers=cabecalho,
            tablefmt="grid"
        )
    )

    print("=" * 120)
    print(f"Total de registros: {len(tabela)}")