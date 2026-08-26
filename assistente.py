import os
import ollama

from modulos import carregar_dados


# ==========================================
# CONFIGURAÇÃO
# ==========================================

cliente_ollama = ollama.Client(
    host="http://127.0.0.1:11434"
)

MODELO_IA = "qwen2.5:0.5b"

ARQUIVO_REGISTROS = "registros_colonia.txt"
ARQUIVO_ALERTAS = "alertas_colonia.txt"
ARQUIVO_HISTORICO = "historico_colonia.txt"


# ==========================================
# ASSISTENTE INTELIGENTE
# ==========================================

def assistente_inteligente():

    print("\n")
    print("=" * 90)
    print("                    ASSISTENTE INTELIGENTE")
    print("                       NCAS - AURORA SIGER")
    print("=" * 90)

    print("\nAssistente iniciado.")
    print("Digite sua pergunta sobre a colônia.")
    print("Digite 'sair' para voltar ao menu.")

    while True:

        pergunta = input("\nOperador: ").strip()

        if pergunta.lower() == "sair":
            print("\nEncerrando assistente...")
            break

        if not pergunta:
            print("Digite uma pergunta.")
            continue

        resposta = consultar_ia(pergunta)

        print("\nAssistente:")
        print(resposta)


# ==========================================
# CONSULTAR IA
# ==========================================

def consultar_ia(pergunta):

    dados = carregar_dados()

    contexto_modulos = criar_contexto_modulos(dados)
    contexto_registros = carregar_registros()
    contexto_alertas = carregar_alertas()
    contexto_historico = carregar_historico()

    prompt_sistema = """
Você é o Assistente Inteligente do NCAS
(Núcleo Cognitivo da Aurora SIGER).

Sua função é auxiliar o operador na consulta e
análise dos sistemas da Colônia Aurora SIGER.

==================================================
REGRAS OBRIGATÓRIAS
==================================================

1. Utilize EXCLUSIVAMENTE as informações presentes
nos dados fornecidos pelo NCAS.

2. NUNCA invente:
- valores;
- números;
- distâncias;
- datas;
- módulos;
- status;
- prioridades;
- alertas;
- ocorrências;
- responsáveis;
- eventos;
- alterações;
- históricos;
- problemas que não estejam registrados.

3. Nunca diga que um valor aumentou, diminuiu ou
mudou se não existir um registro comprovando essa
alteração.

4. Nunca interprete uma distância de conexão como
qualidade, capacidade ou nível de suporte.

Exemplo:
"Suporte médico: 20 metros" significa apenas que
existe uma conexão localizada a 20 metros.

5. Um consumo energético alto em comparação com
outros módulos NÃO significa automaticamente que
há um problema.

Somente afirme que existe um problema se houver
um alerta ou registro que indique o problema.

6. A prioridade operacional representa somente
o valor atual informado nos dados.

Não invente mudanças de prioridade.

7. Status "Ativo" significa apenas que o módulo
está operacional segundo os dados atuais.

8. Diferencie claramente:

DADOS DOS MÓDULOS
= situação estrutural e operacional atual.

REGISTROS
= ocorrências cadastradas pelos operadores.

ALERTAS
= problemas ou situações que foram formalmente
registrados como alerta.

HISTÓRICO
= ações executadas no NCAS ao longo do tempo.

9. Quando o operador pedir histórico, utilize
principalmente a seção HISTÓRICO DO NCAS.

10. Quando o operador perguntar sobre alertas,
utilize principalmente a seção ALERTAS DO NCAS.

11. Quando perguntar sobre ocorrências ou registros,
utilize principalmente REGISTROS OPERACIONAIS.

12. Quando perguntar sobre a situação atual de um
módulo, utilize DADOS DOS MÓDULOS e complemente
somente com registros e alertas realmente existentes.

13. Ao sugerir melhorias:

- utilize alertas e ocorrências existentes;
- explique qual informação sustenta a sugestão;
- não crie limites técnicos que não foram fornecidos;
- não considere um módulo defeituoso apenas porque
consome mais energia que outro.

14. Se a informação solicitada não existir, responda:

"Não há informações suficientes nos registros do NCAS
para responder a essa pergunta."

15. Responda sempre em português do Brasil.

16. Seja objetivo, organizado e direto.
"""

    prompt_usuario = f"""
==================================================
DADOS ATUAIS DO NCAS
==================================================


==============================
DADOS DOS MÓDULOS
==============================

{contexto_modulos}


==============================
REGISTROS OPERACIONAIS
==============================

{contexto_registros}


==============================
ALERTAS DO NCAS
==============================

{contexto_alertas}


==============================
HISTÓRICO DO NCAS
==============================

{contexto_historico}


==================================================
PERGUNTA DO OPERADOR
==================================================

{pergunta}
"""

    try:

        resposta = cliente_ollama.chat(
    model=MODELO_IA,
    messages=[
        {
            "role": "system",
            "content": prompt_sistema
        },
        {
            "role": "user",
            "content": prompt_usuario
        }
    ],
    options={
        "temperature": 0,
        "num_predict": 400
    }
)

        # Compatibilidade entre versões da biblioteca ollama
        try:
            return resposta["message"]["content"].strip()

        except (TypeError, KeyError):
            return resposta.message.content.strip()

    except Exception as erro:

        return (
            "Não foi possível consultar o Assistente Inteligente.\n"
            f"Erro: {erro}"
        )


# ==========================================
# CRIAR CONTEXTO DOS MÓDULOS
# ==========================================

def criar_contexto_modulos(dados):

    modulos = dados.get("modulos", {})

    if not modulos:
        return "Nenhum módulo cadastrado."

    partes = []

    for nome, info in modulos.items():

        linhas = [
            f"MÓDULO: {nome}",
            f"Status operacional: {info.get('status_operacional', 'N/A')}",
            (
                "Consumo energético: "
                f"{info.get('consumo_energetico_kwh', 'N/A')} kWh"
            ),
            (
                "Prioridade operacional: "
                f"{info.get('prioridade_operacional', 'N/A')}"
            ),
            (
                "Necessidade de comunicação: "
                f"{info.get('necessidade_comunicacao', 'N/A')}"
            ),
            (
                "Capacidade/Tipo de armazenamento: "
                f"{info.get('capacidade_armazenamento', 'N/A')}"
            ),
            "Conexões físicas:"
        ]

        conexoes = info.get("conexoes", [])

        if conexoes:

            for conexao in conexoes:

                if len(conexao) >= 2:

                    destino = conexao[0]
                    distancia = conexao[1]

                    linhas.append(
                        f"- {destino}: {distancia} metros"
                    )

        else:
            linhas.append("- Nenhuma conexão cadastrada.")

        partes.append("\n".join(linhas))

    return "\n\n".join(partes)


# ==========================================
# CARREGAR REGISTROS
# ==========================================

def carregar_registros():

    if not os.path.exists(ARQUIVO_REGISTROS):
        return "Nenhum registro operacional cadastrado."

    try:

        with open(
            ARQUIVO_REGISTROS,
            "r",
            encoding="utf-8"
        ) as arquivo:

            linhas = [
                linha.strip()
                for linha in arquivo
                if linha.strip()
            ]

        if not linhas:
            return "Nenhum registro operacional cadastrado."

        registros_formatados = []

        for linha in linhas:

            try:

                data = (
                    linha
                    .split("]")[0]
                    .replace("[", "")
                    .strip()
                )

                modulo = (
                    linha
                    .split("Módulo:", 1)[1]
                    .split("|", 1)[0]
                    .strip()
                )

                ocorrencia = (
                    linha
                    .split("Ocorrência:", 1)[1]
                    .split("|", 1)[0]
                    .strip()
                )

                responsavel = (
                    linha
                    .split("Responsável:", 1)[1]
                    .strip()
                )

                registro = (
                    f"Data/Hora: {data}\n"
                    f"Módulo: {modulo}\n"
                    f"Ocorrência: {ocorrencia}\n"
                    f"Responsável: {responsavel}"
                )

                registros_formatados.append(registro)

            except (IndexError, ValueError):

                registros_formatados.append(
                    f"Registro bruto: {linha}"
                )

        return "\n\n".join(registros_formatados)

    except OSError as erro:

        return (
            "Não foi possível carregar os registros.\n"
            f"Erro: {erro}"
        )


# ==========================================
# CARREGAR ALERTAS
# ==========================================

def carregar_alertas():

    if not os.path.exists(ARQUIVO_ALERTAS):
        return "Nenhum alerta cadastrado."

    try:

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
            return "Nenhum alerta cadastrado."

        alertas_formatados = []

        for linha in linhas:

            dados = linha.split("|", 5)

            if len(dados) != 6:

                alertas_formatados.append(
                    f"Alerta bruto: {linha}"
                )

                continue

            id_alerta = dados[0].strip()
            data = dados[1].strip()
            modulo = dados[2].strip()
            prioridade = dados[3].strip()
            descricao = dados[4].strip()
            status = dados[5].strip()

            alerta = (
                f"ID: {id_alerta}\n"
                f"Data/Hora: {data}\n"
                f"Módulo: {modulo}\n"
                f"Prioridade: {prioridade}\n"
                f"Descrição: {descricao}\n"
                f"Status: {status}"
            )

            alertas_formatados.append(alerta)

        return "\n\n".join(alertas_formatados)

    except OSError as erro:

        return (
            "Não foi possível carregar os alertas.\n"
            f"Erro: {erro}"
        )


# ==========================================
# CARREGAR HISTÓRICO
# ==========================================

def carregar_historico():

    if not os.path.exists(ARQUIVO_HISTORICO):
        return "Nenhuma atividade registrada no histórico."

    try:

        with open(
            ARQUIVO_HISTORICO,
            "r",
            encoding="utf-8"
        ) as arquivo:

            linhas = [
                linha.strip()
                for linha in arquivo
                if linha.strip()
            ]

        if not linhas:
            return "Nenhuma atividade registrada no histórico."

        historico_formatado = []

        for linha in linhas:

            dados = linha.split("|", 3)

            if len(dados) != 4:

                historico_formatado.append(
                    f"Histórico bruto: {linha}"
                )

                continue

            data = dados[0].strip()
            acao = dados[1].strip()
            modulo = dados[2].strip()
            descricao = dados[3].strip()

            atividade = (
                f"Data/Hora: {data}\n"
                f"Ação: {acao}\n"
                f"Módulo: {modulo}\n"
                f"Descrição: {descricao}"
            )

            historico_formatado.append(atividade)

        return "\n\n".join(historico_formatado)

    except OSError as erro:

        return (
            "Não foi possível carregar o histórico.\n"
            f"Erro: {erro}"
        )


# ==========================================
# TESTE DIRETO
# ==========================================

if __name__ == "__main__":
    assistente_inteligente()
