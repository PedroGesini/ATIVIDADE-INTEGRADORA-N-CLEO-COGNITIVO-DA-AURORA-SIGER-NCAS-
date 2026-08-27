from pathlib import Path
from datetime import datetime

from .historico import registrar_historico
from .regras import alerta_deve_ser_priorizado
from .tabela import exibir_tabela


BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_DATA = BASE_DIR / "data"
ARQUIVO_ALERTAS = PASTA_DATA / "alertas_colonia.txt"


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

    niveis = {
        1: "Baixa",
        2: "Média",
        3: "Alta",
        4: "Crítica",
    }

    nivel = niveis.get(prioridade)
    if nivel is None:
        print("Prioridade inválida.")
        return

    PASTA_DATA.mkdir(parents=True, exist_ok=True)
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    id_alerta = gerar_id_alerta()
    status = "Pendente"

    linha = (
        f"{id_alerta}|{data}|{modulo}|{nivel}|"
        f"{descricao}|{status}\n"
    )

    with open(ARQUIVO_ALERTAS, "a", encoding="utf-8") as arquivo:
        arquivo.write(linha)

    registrar_historico(
        "Criação de alerta",
        modulo,
        f"Alerta #{id_alerta} criado com prioridade {nivel}: {descricao}",
    )

    print("\n" + "=" * 70)
    print("                 ALERTA CRIADO COM SUCESSO")
    print("=" * 70)
    print(f"ID:         {id_alerta}")
    print(f"Data/Hora:  {data}")
    print(f"Módulo:     {modulo}")
    print(f"Prioridade: {nivel}")
    print(f"Descrição:  {descricao}")
    print(f"Status:     {status}")
    print("=" * 70)


def gerar_id_alerta():
    if not ARQUIVO_ALERTAS.exists():
        return 1

    with open(ARQUIVO_ALERTAS, "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]

    ids = []

    for linha in linhas:
        dados = linha.split("|", 1)
        try:
            ids.append(int(dados[0]))
        except (ValueError, IndexError):
            continue

    return max(ids) + 1 if ids else 1


def analisar_alerta():
    print("\n")
    print("=" * 70)
    print("                    ANALISAR ALERTA")
    print("=" * 70)

    if not ARQUIVO_ALERTAS.exists():
        print("\nNenhum alerta cadastrado.")
        return

    with open(ARQUIVO_ALERTAS, "r", encoding="utf-8") as arquivo:
        linhas = [linha.strip() for linha in arquivo if linha.strip()]

    if not linhas:
        print("\nNenhum alerta cadastrado.")
        return

    tabela = []

    for linha in linhas:
        dados = linha.split("|", 5)
        if len(dados) != 6:
            continue

        tabela.append([
            dados[0].strip(),
            dados[1].strip(),
            dados[2].strip(),
            dados[3].strip(),
            dados[5].strip(),
        ])

    if not tabela:
        print("\nNenhum alerta válido encontrado.")
        return

    exibir_tabela(
        ["ID", "Data/Hora", "Módulo", "Prioridade", "Status"],
        tabela,
        [6, 16, 28, 12, 12],
    )

    try:
        id_escolhido = int(input("\nDigite o ID do alerta que deseja analisar: "))
    except ValueError:
        print("\nDigite um ID válido.")
        return

    alerta_encontrado = None

    for linha in linhas:
        dados = linha.split("|", 5)
        if len(dados) != 6:
            continue

        try:
            id_atual = int(dados[0])
        except ValueError:
            continue

        if id_atual == id_escolhido:
            alerta_encontrado = [campo.strip() for campo in dados]
            break

    if alerta_encontrado is None:
        print("\nAlerta não encontrado.")
        return

    id_alerta, data, modulo, prioridade, descricao, status = alerta_encontrado

    print("\n" + "=" * 70)
    print("                     DADOS DO ALERTA")
    print("=" * 70)
    print(f"ID:          {id_alerta}")
    print(f"Data/Hora:   {data}")
    print(f"Módulo:      {modulo}")
    print(f"Prioridade:  {prioridade}")
    print(f"Descrição:   {descricao}")
    print(f"Status:      {status}")

    if status == "Finalizado":
        print("\nResultado: este alerta já está Finalizado.")
        registrar_historico(
            "Análise de alerta",
            modulo,
            f"Consulta do alerta #{id_alerta}, já finalizado.",
        )
        return

    prioritario = alerta_deve_ser_priorizado(status, prioridade)

    print("\n" + "-" * 70)
    print("RESULTADO DA REGRA LÓGICA:")

    if prioritario:
        print("ATENÇÃO PRIORITÁRIA: SIM")
        print(
            "Motivo: o alerta está Pendente e a prioridade cadastrada "
            f"é {prioridade}."
        )
        resultado_historico = "atende à regra de atenção prioritária"
    else:
        print("ATENÇÃO PRIORITÁRIA: NÃO")
        print(
            "Motivo: o alerta não reúne simultaneamente as condições "
            "definidas pela regra P AND (A OR C)."
        )
        resultado_historico = "não atende à regra de atenção prioritária"

    registrar_historico(
        "Análise de alerta",
        modulo,
        f"Alerta #{id_alerta} analisado: {resultado_historico}.",
    )

    print("\nDeseja finalizar este alerta?")
    print("1 - Sim")
    print("2 - Não")

    try:
        opcao = int(input("\nDigite a opção: "))
    except ValueError:
        print("\nOpção inválida.")
        return

    if opcao == 1:
        novas_linhas = []

        for linha in linhas:
            dados = linha.split("|", 5)
            if len(dados) != 6:
                novas_linhas.append(linha)
                continue

            try:
                id_atual = int(dados[0])
            except ValueError:
                novas_linhas.append(linha)
                continue

            if id_atual == id_escolhido:
                dados[5] = "Finalizado"
                novas_linhas.append("|".join(dados))
            else:
                novas_linhas.append(linha)

        with open(ARQUIVO_ALERTAS, "w", encoding="utf-8") as arquivo:
            for linha in novas_linhas:
                arquivo.write(linha + "\n")

        registrar_historico(
            "Finalização de alerta",
            modulo,
            f"Alerta #{id_alerta} finalizado",
        )

        print("\n" + "=" * 70)
        print("                 ALERTA FINALIZADO")
        print("=" * 70)
        print(f"ID:      {id_alerta}")
        print(f"Módulo:  {modulo}")
        print("Status:  Finalizado")
        print("=" * 70)

    elif opcao == 2:
        print("\nAlerta mantido como Pendente.")
    else:
        print("\nOpção inválida.")
