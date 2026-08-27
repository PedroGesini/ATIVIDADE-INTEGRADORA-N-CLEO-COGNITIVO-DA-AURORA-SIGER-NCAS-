from pathlib import Path
from datetime import datetime

from .tabela import exibir_tabela


BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_DATA = BASE_DIR / "data"
ARQUIVO_HISTORICO = PASTA_DATA / "historico_colonia.txt"


def registrar_historico(acao, modulo="Sistema", descricao=""):
    PASTA_DATA.mkdir(parents=True, exist_ok=True)
    data = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    linha = f"{data}|{acao}|{modulo}|{descricao}\n"

    with open(ARQUIVO_HISTORICO, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)


def consultar_historico():
    print("\n")
    print("=" * 110)
    print("                    HISTÓRICO GERAL DO NCAS")
    print("=" * 110)

    if not ARQUIVO_HISTORICO.exists():
        print("\nNenhuma atividade registrada.")
        return

    with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]

    if not linhas:
        print("\nNenhuma atividade registrada.")
        return

    tabela = []

    for linha in linhas:
        dados = linha.split("|", 3)
        if len(dados) != 4:
            continue

        tabela.append([
            dados[0].strip(),
            dados[1].strip(),
            dados[2].strip(),
            dados[3].strip(),
        ])

    if not tabela:
        print("\nNenhum registro válido encontrado.")
        return

    exibir_tabela(
        ["Data/Hora", "Ação", "Módulo", "Descrição"],
        tabela,
        [19, 26, 24, 45],
    )

    print(f"\nTotal de atividades registradas: {len(tabela)}")
