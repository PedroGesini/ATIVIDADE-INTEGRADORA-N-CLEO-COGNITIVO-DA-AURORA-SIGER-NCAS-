from pathlib import Path
from datetime import datetime

from src.historico import registrar_historico
from src.tabela import exibir_tabela


BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_DATA = BASE_DIR / "data"
ARQUIVO_TXT = PASTA_DATA / "registros_colonia.txt"


def cadastrar_registro():
    print("\n")
    print("=" * 70)
    print("                 CADASTRAR REGISTRO")
    print("=" * 70)

    modulo = input("Módulo: ").strip()
    if not modulo:
        print("O módulo não pode ficar vazio.")
        return

    descricao = input("Descrição da ocorrência: ").strip()
    if not descricao:
        print("A descrição não pode ficar vazia.")
        return

    responsavel = input("Responsável: ").strip()
    if not responsavel:
        print("O responsável não pode ficar vazio.")
        return

    PASTA_DATA.mkdir(parents=True, exist_ok=True)
    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    linha = (
        f"[{data}] | "
        f"Módulo: {modulo} | "
        f"Ocorrência: {descricao} | "
        f"Responsável: {responsavel}"
    )

    with open(ARQUIVO_TXT, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha + "\n")

    registrar_historico(
        "Cadastro de registro",
        modulo,
        f"Ocorrência registrada: {descricao} | Responsável: {responsavel}",
    )

    print("\n" + "-" * 70)
    print("Registro salvo com sucesso!")
    print("-" * 70)


def consultar_registros():
    print("\n")
    print("=" * 120)
    print("                    REGISTROS DA COLÔNIA AURORA SIGER")
    print("=" * 120)

    if not ARQUIVO_TXT.exists():
        print("\nNenhum registro encontrado.")
        return

    with open(ARQUIVO_TXT, "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]

    if not linhas:
        print("\nNenhum registro encontrado.")
        return

    tabela = []

    for numero, linha in enumerate(linhas, start=1):
        try:
            data = linha.split("]")[0].replace("[", "").strip()
            modulo = linha.split("Módulo:", 1)[1].split("|", 1)[0].strip()
            ocorrencia = linha.split("Ocorrência:", 1)[1].split("|", 1)[0].strip()
            responsavel = linha.split("Responsável:", 1)[1].strip()

            tabela.append([numero, data, modulo, ocorrencia, responsavel])
        except (IndexError, ValueError):
            tabela.append([numero, "N/A", "N/A", linha, "N/A"])

    exibir_tabela(
        ["ID", "Data/Hora", "Módulo", "Ocorrência", "Responsável"],
        tabela,
        [5, 16, 24, 50, 24],
    )

    print(f"\nTotal de registros: {len(tabela)}")

    registrar_historico(
        "Consulta de registros",
        "Sistema",
        f"Consulta geral realizada. Total de registros: {len(tabela)}",
    )
