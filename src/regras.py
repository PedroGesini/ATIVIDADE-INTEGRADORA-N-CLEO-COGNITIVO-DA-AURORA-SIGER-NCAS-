from pathlib import Path

from src.historico import registrar_historico


BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_DATA = BASE_DIR / "data"
ARQUIVO_ALERTAS = PASTA_DATA / "alertas_colonia.txt"


def alerta_deve_ser_priorizado(status, prioridade):
    """Regra simplificada: P AND (A OR C)."""
    P = status == "Pendente"
    A = prioridade == "Alta"
    C = prioridade == "Crítica"
    return P and (A or C)


def _expressoes_equivalentes(P, A, C):
    original = (P and A) or (P and C)
    simplificada = P and (A or C)
    return original == simplificada


def validar_simplificacao_booleana():
    for P in (False, True):
        for A in (False, True):
            for C in (False, True):
                if not _expressoes_equivalentes(P, A, C):
                    return False
    return True


def executar_regra_logica():
    print("\n" + "=" * 70)
    print(" REGRA LÓGICA DO NCAS")
    print("=" * 70)

    print("\nREGRA:")
    print(
        "Um alerta recebe atenção prioritária quando estiver "
        "Pendente e possuir prioridade Alta ou Crítica."
    )

    print("\nVARIÁVEIS BOOLEANAS:")
    print("P = alerta está Pendente")
    print("A = prioridade é Alta")
    print("C = prioridade é Crítica")

    print("\nEXPRESSÃO ORIGINAL:")
    print("PRIORIZAR = (P AND A) OR (P AND C)")

    print("\nSIMPLIFICAÇÃO:")
    print("(P AND A) OR (P AND C) = P AND (A OR C)")

    print("\nEXPRESSÃO SIMPLIFICADA:")
    print("PRIORIZAR = P AND (A OR C)")

    if not validar_simplificacao_booleana():
        print("\nErro: as expressões não produziram resultados equivalentes.")
        return

    print("\nValidação booleana: expressões equivalentes para todas as combinações.")

    if not ARQUIVO_ALERTAS.exists():
        print("\nNenhum alerta cadastrado.")
        registrar_historico(
            "Execução de regra lógica",
            "Sistema",
            "Nenhum alerta disponível para validação.",
        )
        return

    with open(ARQUIVO_ALERTAS, "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]

    alertas_prioritarios = []

    for linha in linhas:
        dados = linha.split("|", 5)
        if len(dados) != 6:
            continue

        id_alerta, data, modulo, prioridade, descricao, status = [
            campo.strip() for campo in dados
        ]

        if alerta_deve_ser_priorizado(status, prioridade):
            alertas_prioritarios.append({
                "id": id_alerta,
                "data": data,
                "modulo": modulo,
                "prioridade": prioridade,
                "descricao": descricao,
                "status": status,
            })

    print("\nRESULTADO:")
    print("-" * 70)

    if not alertas_prioritarios:
        print("Nenhum alerta Pendente com prioridade Alta ou Crítica foi encontrado.")
        registrar_historico(
            "Execução de regra lógica",
            "Sistema",
            "Nenhum alerta prioritário identificado.",
        )
        return

    for numero, alerta in enumerate(alertas_prioritarios, start=1):
        print(f"\n{numero}. Alerta #{alerta['id']}")
        print(f"   Data: {alerta['data']}")
        print(f"   Módulo: {alerta['modulo']}")
        print(f"   Prioridade: {alerta['prioridade']}")
        print(f"   Status: {alerta['status']}")
        print(f"   Descrição: {alerta['descricao']}")

    total = len(alertas_prioritarios)
    print("\n" + "-" * 70)
    print(f"Total de alertas que atendem à regra: {total}")

    registrar_historico(
        "Execução de regra lógica",
        "Sistema",
        f"{total} alerta(s) atenderam à regra lógica.",
    )
