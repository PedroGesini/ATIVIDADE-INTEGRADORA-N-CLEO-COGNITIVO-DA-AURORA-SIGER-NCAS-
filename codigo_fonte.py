
from src.modulos import consultar_modulos
from src.alertas import criar_alerta, analisar_alerta
from src.historico import consultar_historico
from src.regras import executar_regra_logica
from src.prompts import exibir_prompts
from src.assistente import assistente_inteligente
from src.registros import cadastrar_registro, consultar_registros


# NCAS - NÚCLEO COGNITIVO DA AURORA SIGER
def exibir_menu():
    """Exibe o menu principal do NCAS."""

    print("\n" + "=" * 60)
    print("          SEJA BEM-VINDO!")
    print("     SISTEMA OPERACIONAL AURORA")
    print("=" * 60)

    print("""
1 - Cadastrar registro
2 - Consultar registros
3 - Consultar módulos
4 - Criar alerta
5 - Analisar alerta
6 - Consultar histórico
7 - Executar regra lógica
8 - Exibir prompts estruturados
9 - Assistente inteligente
0 - Sair
""")


def pausar():
    """Pausa a execução antes de retornar ao menu."""

    input("\nPressione ENTER para voltar ao menu...")


def main():
    """Executa o menu principal do NCAS."""

    while True:

        exibir_menu()

        try:
            opcao = int(
                input("DIGITE A OPÇÃO DESEJADA: ")
            )

        except ValueError:
            print(
                "\nEntrada inválida! "
                "Por favor, digite apenas um número."
            )
            pausar()
            continue

        match opcao:

            case 1:
                cadastrar_registro()
                pausar()

            case 2:
                consultar_registros()
                pausar()

            case 3:
                consultar_modulos()
                pausar()

            case 4:
                criar_alerta()
                pausar()

            case 5:
                analisar_alerta()
                pausar()

            case 6:
                consultar_historico()
                pausar()

            case 7:
                executar_regra_logica()
                pausar()

            case 8:
                exibir_prompts()
                pausar()

            case 9:
                assistente_inteligente()
                pausar()

            case 0:
                print(
                    "\nEncerrando o Sistema Operacional Aurora. "
                    "Até logo!"
                )
                break

            case _:
                print("\nOpção inválida.")
                pausar()


if __name__ == "__main__":
    main()
