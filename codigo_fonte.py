from src.registros import cadastrar_registro,consultar_registros
from src.modulos import consultar_modulos
from src.alertas import criar_alerta,analisar_alerta
from src.historico import consultar_historico
from src.regras import executar_regra_logica
from src.prompts import exibir_prompts
from src.assistente import assistente_inteligente


#      NCAS - AURORA SIGER
while True:

    print("\n" + "=" * 50)
    print("          SEJA BEM-VINDO!")
    print("     SISTEMA OPERACIONAL AURORA")
    print("=" * 50)

    print("""
    1 - Cadastrar registro
    2 - Consultar registros
    3 - Consultar módulos
    4 - Criar alerta
    5 - Analisar alerta
    6 - Consultar histórico
    7 - Executar regra lógica
    8 - Assistente inteligente
    9 - Sair
    """)

    try:
        opcao = int(
            input("DIGITE A OPÇÃO DESEJADA: ")
        )

    except ValueError:
        print(
            "\nEntrada inválida! "
            "Por favor, digite um número."
        )
        continue

    match opcao:

        case 1:
            cadastrar_registro()
            input(
                "\nPressione ENTER para voltar ao menu..."
            )

        case 2:
            consultar_registros()
            input(
                "\nPressione ENTER para voltar ao menu..."
            )

        case 3:
            consultar_modulos()
            input(
                "\nPressione ENTER para voltar ao menu..."
            )

        case 4:
            criar_alerta()
            input(
                "\nPressione ENTER para voltar ao menu..."
            )

        case 5:
            analisar_alerta()
            input(
                "\nPressione ENTER para voltar ao menu..."
            )

        case 6:
            consultar_historico()
            input(
                "\nPressione ENTER para voltar ao menu..."
            )

        case 7:
            executar_regra_logica()
            input(
                "\nPressione ENTER para voltar ao menu..."
            )

        case 8:
            assistente_inteligente()
            input(
                "\nPressione ENTER para voltar ao menu..."
            )

        case 9:
            print(
                "\nEncerrando o Sistema Operacional Aurora. "
                "Até logo!"
            )
            break

        case _:
            print("\nOpção inválida.")
            input(
                "\nPressione ENTER para voltar ao menu..."
            )