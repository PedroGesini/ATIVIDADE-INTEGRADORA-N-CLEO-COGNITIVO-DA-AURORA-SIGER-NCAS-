from modulos import carregar_dados
from historico import registrar_historico


def executar_regra_logica():

    print("\n")
    print("=" * 100)
    print("                    EXECUTAR REGRA LÓGICA")
    print("                       NCAS - AURORA SIGER")
    print("=" * 100)

    dados = carregar_dados()
    modulos = dados.get("modulos", {})

    if not modulos:
        print("\nNenhum módulo encontrado.")
        return

    ocorrencias = []

    # ==========================================
    # ANÁLISE DOS MÓDULOS
    # ==========================================

    for nome, info in modulos.items():

        consumo = info["consumo_energetico_kwh"]
        prioridade = info["prioridade_operacional"]
        status = info["status_operacional"]

        # Regra 1
        if status != "Ativo":

            ocorrencias.append(
                f"{nome}: módulo está {status}."
            )

        # Regra 2
        if consumo >= 250:

            ocorrencias.append(
                f"{nome}: consumo energético elevado "
                f"({consumo} kWh)."
            )

        # Regra 3
        if prioridade == 1 and status == "Ativo":

            ocorrencias.append(
                f"{nome}: módulo possui prioridade operacional máxima."
            )

    # ==========================================
    # RESULTADO
    # ==========================================

    if not ocorrencias:

        print("\nNenhuma condição de atenção encontrada.")

        registrar_historico(
            "Execução de regra lógica",
            "Sistema",
            "Nenhuma ocorrência identificada."
        )

        return

    print("\nCONDIÇÕES IDENTIFICADAS:")
    print("-" * 100)

    for numero, ocorrencia in enumerate(ocorrencias, start=1):

        print(f"{numero}. {ocorrencia}")

    print("-" * 100)

    print(
        f"\nTotal de condições identificadas: "
        f"{len(ocorrencias)}"
    )

    registrar_historico(
        "Execução de regra lógica",
        "Sistema",
        f"{len(ocorrencias)} condição(ões) identificada(s)."
    )