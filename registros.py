import os
from datetime import datetime

ARQUIVO_TXT = "registros_colonia.txt"


def cadastrar_registro():
    print("\n--- Cadastrar registro ---")
    modulo = input("Modulo: ").strip()
    descricao = input("Descricao da ocorrencia: ").strip()
    responsavel = input("Responsavel: ").strip()
    data = datetime.now().strftime("%Y-%m-%d %H:%M")

    linha = f"[{data}] Modulo: {modulo} | Ocorrencia: {descricao} | Responsavel: {responsavel}"

    with open(ARQUIVO_TXT, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha + "\n")

    print("Registro salvo com sucesso!")


def consultar_registros():
    print("\n--- Registros salvos ---")
    if not os.path.exists(ARQUIVO_TXT):
        print("Nenhum registro encontrado.")
        return
    with open(ARQUIVO_TXT, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            print(linha.rstrip("\n"))
            