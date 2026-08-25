from registros import cadastrar_registro, consultar_registros
# ====================================
#      NCAS - AURORA SIGER
# ====================================

while True:

    print(f"----- SEJA BEM-VINDO! -----")

    print("""
        SISTEMA OPERACIONAL AURORA

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

    # PROGRAMA PRINCIPAL
    try:
        opcao = int(input("DIGITE A OPÇÃO DESEJADA: "))

    except ValueError:
        print("Entrada inválida! Por favor, digite um número.")
        continue

    match opcao:

        case 1:
            cadastrar_registro()
            input("\nPressione ENTER para voltar ao menu...")

        case 2:
            consultar_registros()
            input("\nPressione ENTER para voltar ao menu...")

        case 3:
            # Consultar módulos
            input("\nPressione ENTER para voltar ao menu...")

        case 4:
            # Criar alerta
            input("\nPressione ENTER para voltar ao menu...")

        case 5:
            # Analisar alerta
            input("\nPressione ENTER para voltar ao menu...")

        case 6:
            # Consultar histórico
            input("\nPressione ENTER para voltar ao menu...")

        case 7:
            # Executar regra lógica
            input("\nPressione ENTER para voltar ao menu...")

        case 8:
            # Assistente inteligente
            input("\nPressione ENTER para voltar ao menu...")

        case 9:
            print("Encerrando o Sistema Operacional Aurora. Até logo!")
            break

        case _:
            print("Opção inválida.")
            input("\nPressione ENTER para voltar ao menu...")