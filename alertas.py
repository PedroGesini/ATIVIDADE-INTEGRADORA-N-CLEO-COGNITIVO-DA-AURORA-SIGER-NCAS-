import os
from datetime import datetime
from tabulate import tabulate

from historico import registrar_historico


ARQUIVO_ALERTAS = "alertas_colonia.txt"


# ==========================================
# CRIAR ALERTA
# ==========================================

def criar_alerta():

    print("\n")
    print("=" * 70)
    print("                         CRIAR ALERTA")
    print("=" * 70)

    modulo = input("Módulo afetado: ").strip()

    if not modulo:
        print("O módulo não pode ficar vazio.")
        return

    descricao = input("Descrição do alerta: ").strip()

    if not descricao:
        print("A descrição não pode ficar vazia.")
        return

    print("\nNível de prioridade:")
    print("1 - Baixa")
    print("2 - Média")
    print("3 - Alta")
    print("4 - Crítica")

    try:
        prioridade = int(input("\nDigite a prioridade: "))

    except ValueError:

        print("Digite apenas números.")
        return

    match prioridade:

        case 1:
            nivel = "Baixa"

        case 2:
            nivel = "Média"

        case 3:
            nivel = "Alta"

        case 4:
            nivel = "Crítica"

        case _:
            print("Prioridade inválida.")
            return

    data = datetime.now().strftime("%d/%m/%Y %H:%M")

    id_alerta = gerar_id_alerta()

    status = "Pendente"

    linha = (
        f"{id_alerta}|"
        f"{data}|"
        f"{modulo}|"
        f"{nivel}|"
        f"{descricao}|"
        f"{status}\n"
    )

    with open(
        ARQUIVO_ALERTAS,
        "a",
        encoding="utf-8"
    ) as arquivo:

        arquivo.write(linha)

    # ==========================================
    # REGISTRAR NO HISTÓRICO
    # ==========================================

    registrar_historico(
        "Criação de alerta",
        modulo,
        f"Alerta #{id_alerta} criado com prioridade {nivel}: {descricao}"
    )

    print("\n")
    print("=" * 70)
    print("                 ALERTA CRIADO COM SUCESSO")
    print("=" * 70)

    print(f"ID:         {id_alerta}")
    print(f"Data/Hora:  {data}")
    print(f"Módulo:     {modulo}")
    print(f"Prioridade: {nivel}")
    print(f"Descrição:  {descricao}")
    print(f"Status:     {status}")

    print("=" * 70)


# ==========================================
# GERAR ID DO ALERTA
# ==========================================

def gerar_id_alerta():

    if not os.path.exists(ARQUIVO_ALERTAS):

        return 1

    with open(
        ARQUIVO_ALERTAS,
        "r",
        encoding="utf-8"
    ) as arquivo:

        linhas = [
            linha.strip()
            for linha in arquivo
            if linha.strip()
        ]

    return len(linhas) + 1


# ==========================================
# ANALISAR ALERTA
# ==========================================

def analisar_alerta():

    print("\n")
    print("=" * 70)
    print("                    ANALISAR ALERTA")
    print("=" * 70)

    if not os.path.exists(ARQUIVO_ALERTAS):

        print("\nNenhum alerta cadastrado.")
        return

    with open(
        ARQUIVO_ALERTAS,
        "r",
        encoding="utf-8"
    ) as arquivo:

        linhas = [
            linha.strip()
            for linha in arquivo
            if linha.strip()
        ]

    if not linhas:

        print("\nNenhum alerta cadastrado.")
        return

    tabela = []

    for linha in linhas:

        dados = linha.split("|")

        if len(dados) != 6:
            continue

        id_alerta = dados[0]
        data = dados[1]
        modulo = dados[2]
        prioridade = dados[3]
        status = dados[5]

        tabela.append([
            id_alerta,
            data,
            modulo,
            prioridade,
            status
        ])

    print(
        tabulate(
            tabela,
            headers=[
                "ID",
                "Data/Hora",
                "Módulo",
                "Prioridade",
                "Status"
            ],
            tablefmt="grid"
        )
    )

    try:

        id_escolhido = int(
            input("\nDigite o ID do alerta que deseja analisar: ")
        )

    except ValueError:

        print("\nDigite um ID válido.")
        return

    alerta_encontrado = None

    for linha in linhas:

        dados = linha.split("|")

        if len(dados) != 6:
            continue

        if int(dados[0]) == id_escolhido:

            alerta_encontrado = dados
            break

    if alerta_encontrado is None:

        print("\nAlerta não encontrado.")
        return

    id_alerta = alerta_encontrado[0]
    data = alerta_encontrado[1]
    modulo = alerta_encontrado[2]
    prioridade = alerta_encontrado[3]
    descricao = alerta_encontrado[4]
    status = alerta_encontrado[5]

    # ==========================================
    # VERIFICAR SE JÁ FOI FINALIZADO
    # ==========================================

    if status == "Finalizado":

        print("\nEste alerta já foi finalizado.")
        print(f"ID: {id_alerta}")
        print(f"Módulo: {modulo}")

        return

    # ==========================================
    # ANÁLISE DA PRIORIDADE
    # ==========================================

    match prioridade:

        case "Baixa":

            classificacao = "BAIXO RISCO"

            analise = (
                "O alerta apresenta baixo impacto operacional. "
                "Recomenda-se acompanhar a situação."
            )

            recomendacao = (
                "Monitorar o módulo e realizar intervenção "
                "caso o problema evolua."
            )

        case "Média":

            classificacao = "RISCO MODERADO"

            analise = (
                "O alerta apresenta impacto operacional moderado. "
                "A situação deve ser acompanhada pela equipe responsável."
            )

            recomendacao = (
                "Realizar uma verificação preventiva e acompanhar "
                "a evolução do problema."
            )

        case "Alta":

            classificacao = "ALTO RISCO"

            analise = (
                "O alerta apresenta potencial de impacto significativo "
                "na operação da colônia."
            )

            recomendacao = (
                "Priorizar a análise do módulo e realizar intervenção "
                "em curto prazo."
            )

        case "Crítica":

            classificacao = "RISCO CRÍTICO"

            analise = (
                "O alerta apresenta risco crítico para a operação "
                "da colônia e pode comprometer sistemas essenciais."
            )

            recomendacao = (
                "Realizar intervenção imediata e priorizar o módulo "
                "afetado."
            )

        case _:

            classificacao = "NÃO CLASSIFICADO"

            analise = "Não foi possível determinar o nível de risco."

            recomendacao = "Realizar análise manual."

    # ==========================================
    # EXIBIR ANÁLISE
    # ==========================================

    print("\n")
    print("=" * 70)
    print("                     ANÁLISE DO ALERTA")
    print("=" * 70)

    print(f"ID:          {id_alerta}")
    print(f"Data/Hora:   {data}")
    print(f"Módulo:      {modulo}")
    print(f"Prioridade:  {prioridade}")
    print(f"Descrição:   {descricao}")
    print(f"Status:      {status}")

    print("\n" + "-" * 70)

    print(f"CLASSIFICAÇÃO: {classificacao}")

    print("\nANÁLISE:")
    print(analise)

    print("\nRECOMENDAÇÃO:")
    print(recomendacao)

    # ==========================================
    # REGISTRAR ANÁLISE NO HISTÓRICO
    # ==========================================

    registrar_historico(
        "Análise de alerta",
        modulo,
        f"Alerta #{id_alerta} analisado como {classificacao}"
    )

    print("\n" + "-" * 70)

    # ==========================================
    # FINALIZAR ALERTA
    # ==========================================

    print("\nDeseja finalizar este alerta?")
    print("1 - Sim")
    print("2 - Não")

    try:

        opcao = int(input("\nDigite a opção: "))

    except ValueError:

        print("\nOpção inválida.")
        return

    match opcao:

        case 1:

            novas_linhas = []

            for linha in linhas:

                dados = linha.split("|")

                if len(dados) != 6:

                    novas_linhas.append(linha)
                    continue

                if int(dados[0]) == id_escolhido:

                    dados[5] = "Finalizado"

                    nova_linha = "|".join(dados)

                    novas_linhas.append(nova_linha)

                else:

                    novas_linhas.append(linha)

            with open(
                ARQUIVO_ALERTAS,
                "w",
                encoding="utf-8"
            ) as arquivo:

                for linha in novas_linhas:

                    arquivo.write(linha + "\n")

            # ==========================================
            # REGISTRAR FINALIZAÇÃO NO HISTÓRICO
            # ==========================================

            registrar_historico(
                "Finalização de alerta",
                modulo,
                f"Alerta #{id_alerta} finalizado"
            )

            print("\n" + "=" * 70)
            print("                 ALERTA FINALIZADO")
            print("=" * 70)

            print(f"ID:      {id_alerta}")
            print(f"Módulo:  {modulo}")
            print("Status:  Finalizado")

            print("=" * 70)

        case 2:

            print("\nAlerta mantido como Pendente.")

        case _:

            print("\nOpção inválida.")