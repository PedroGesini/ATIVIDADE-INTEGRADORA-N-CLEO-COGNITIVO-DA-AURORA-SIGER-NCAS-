from pathlib import Path
import ollama

from .modulos import carregar_dados


# ==========================================
# CAMINHOS DO PROJETO
# ==========================================

BASE_DIR = Path(__file__).resolve().parent.parent
PASTA_DATA = BASE_DIR / "data"

ARQUIVO_REGISTROS = PASTA_DATA / "registros_colonia.txt"
ARQUIVO_ALERTAS = PASTA_DATA / "alertas_colonia.txt"
ARQUIVO_HISTORICO = PASTA_DATA / "historico_colonia.txt"


# ==========================================
# CONFIGURAÇÃO DO OLLAMA
# ==========================================

cliente_ollama = ollama.Client(
    host="http://127.0.0.1:11434"
)

MODELO_IA = "qwen2.5:0.5b"

# Limita o tamanho da resposta para evitar respostas excessivas.
LIMITE_TOKENS_RESPOSTA = 350

# Quantidade máxima de itens enviados de arquivos que crescem com o tempo.
LIMITE_REGISTROS_CONTEXTO = 30
LIMITE_ALERTAS_CONTEXTO = 30
LIMITE_HISTORICO_CONTEXTO = 40


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

    fontes = identificar_fontes(pergunta)

    secoes = []

    if "modulos" in fontes:

        dados = carregar_dados()
        secoes.append(
            "==============================\n"
            "DADOS DOS MÓDULOS\n"
            "==============================\n\n"
            + criar_contexto_modulos(dados)
        )

    if "registros" in fontes:

        secoes.append(
            "==============================\n"
            "REGISTROS OPERACIONAIS\n"
            "==============================\n\n"
            + carregar_registros(
                limite=LIMITE_REGISTROS_CONTEXTO
            )
        )

    if "alertas" in fontes:

        secoes.append(
            "==============================\n"
            "ALERTAS DO NCAS\n"
            "==============================\n\n"
            + carregar_alertas(
                limite=LIMITE_ALERTAS_CONTEXTO
            )
        )

    if "historico" in fontes:

        secoes.append(
            "==============================\n"
            "HISTÓRICO DO NCAS\n"
            "==============================\n\n"
            + carregar_historico(
                limite=LIMITE_HISTORICO_CONTEXTO
            )
        )

    contexto = "\n\n".join(secoes)

    prompt_sistema = """
Você é o Assistente Inteligente do NCAS
(Núcleo Cognitivo da Aurora SIGER).

Sua função é auxiliar o operador na consulta e
análise dos sistemas da Colônia Aurora SIGER.

REGRAS OBRIGATÓRIAS:

1. Utilize EXCLUSIVAMENTE as informações fornecidas
no contexto do NCAS.

2. Nunca invente valores, números, distâncias, datas,
módulos, status, prioridades, alertas, ocorrências,
responsáveis, eventos, alterações ou históricos.

3. Nunca diga que um valor aumentou, diminuiu ou
mudou se não existir registro que comprove isso.

4. Distâncias representam apenas conexões físicas.
Nunca interprete uma distância como qualidade,
capacidade ou nível de suporte.

5. Um consumo energético maior que outro NÃO
significa automaticamente que existe problema.

6. Só afirme que existe problema quando um alerta
ou registro fornecido indicar isso.

7. A prioridade operacional representa apenas o
valor atual informado.

8. Status "Ativo" significa somente que o módulo
está operacional segundo os dados atuais.

9. Diferencie:
- módulos = situação atual;
- registros = ocorrências cadastradas;
- alertas = situações formalmente registradas;
- histórico = ações executadas no NCAS.

10. Ao sugerir melhorias, baseie cada sugestão em
algum dado, registro ou alerta fornecido.

11. Se a informação solicitada não estiver no
contexto, responda:
"Não há informações suficientes nos registros do NCAS para responder a essa pergunta."

12. Responda sempre em português do Brasil.

13. Seja objetivo, organizado e direto.

14. Não repita a mesma informação.

15. Prefira respostas curtas. Use listas somente
quando ajudarem na leitura.
""".strip()

    prompt_usuario = f"""
DADOS DISPONÍVEIS PARA ESTA PERGUNTA:

{contexto}

==============================
PERGUNTA DO OPERADOR
==============================

{pergunta}
""".strip()

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
                "num_predict": LIMITE_TOKENS_RESPOSTA
            }
        )

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
# IDENTIFICAR FONTES NECESSÁRIAS
# ==========================================

def identificar_fontes(pergunta):

    texto = normalizar_texto(pergunta)

    palavras_historico = [
        "historico",
        "historica",
        "historicas",
        "atividade",
        "atividades",
        "acoes do sistema",
        "interacoes do sistema"
    ]

    palavras_alertas = [
        "alerta",
        "alertas",
        "risco",
        "riscos",
        "pendente",
        "pendentes",
        "critico",
        "critica"
    ]

    palavras_registros = [
        "registro",
        "registros",
        "ocorrencia",
        "ocorrencias",
        "responsavel",
        "responsaveis"
    ]

    palavras_modulos = [
        "modulo",
        "modulos",
        "colonia",
        "situacao",
        "status",
        "consumo",
        "energia",
        "energetico",
        "prioridade",
        "comunicacao",
        "armazenamento",
        "conexao",
        "conexoes",
        "habitacao",
        "agricultura",
        "oxigenio",
        "laboratorio",
        "suporte medico",
        "centro de controle"
    ]

    fontes = set()

    if contem_algum(texto, palavras_historico):
        fontes.add("historico")

    if contem_algum(texto, palavras_alertas):
        fontes.add("alertas")

    if contem_algum(texto, palavras_registros):
        fontes.add("registros")

    if contem_algum(texto, palavras_modulos):
        fontes.add("modulos")

    # Perguntas sobre problemas e melhorias normalmente precisam
    # cruzar situação atual, registros e alertas.
    if contem_algum(
        texto,
        [
            "problema",
            "problemas",
            "melhoria",
            "melhorias",
            "melhorado",
            "melhorar",
            "falha",
            "falhas"
        ]
    ):
        fontes.update({
            "modulos",
            "registros",
            "alertas"
        })

    # Se não for possível identificar a intenção,
    # usa os dados atuais dos módulos como contexto padrão.
    if not fontes:
        fontes.add("modulos")

    return fontes


# ==========================================
# FUNÇÕES AUXILIARES DE TEXTO
# ==========================================

def normalizar_texto(texto):

    substituicoes = str.maketrans({
        "á": "a",
        "à": "a",
        "ã": "a",
        "â": "a",
        "ä": "a",
        "é": "e",
        "è": "e",
        "ê": "e",
        "ë": "e",
        "í": "i",
        "ì": "i",
        "î": "i",
        "ï": "i",
        "ó": "o",
        "ò": "o",
        "õ": "o",
        "ô": "o",
        "ö": "o",
        "ú": "u",
        "ù": "u",
        "û": "u",
        "ü": "u",
        "ç": "c"
    })

    return texto.lower().translate(substituicoes)


def contem_algum(texto, palavras):

    return any(
        palavra in texto
        for palavra in palavras
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

            linhas.append(
                "- Nenhuma conexão cadastrada."
            )

        partes.append("\n".join(linhas))

    return "\n\n".join(partes)


# ==========================================
# LER LINHAS DE ARQUIVO
# ==========================================

def ler_linhas(arquivo, limite=None):

    if not arquivo.exists():
        return []

    try:

        with open(
            arquivo,
            "r",
            encoding="utf-8"
        ) as arquivo_aberto:

            linhas = [
                linha.strip()
                for linha in arquivo_aberto
                if linha.strip()
            ]

        if limite is not None and len(linhas) > limite:
            return linhas[-limite:]

        return linhas

    except OSError:
        return []


# ==========================================
# CARREGAR REGISTROS
# ==========================================

def carregar_registros(limite=None):

    linhas = ler_linhas(
        ARQUIVO_REGISTROS,
        limite=limite
    )

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

            registros_formatados.append(
                registro
            )

        except (IndexError, ValueError):

            registros_formatados.append(
                f"Registro bruto: {linha}"
            )

    return "\n\n".join(
        registros_formatados
    )


# ==========================================
# CARREGAR ALERTAS
# ==========================================

def carregar_alertas(limite=None):

    linhas = ler_linhas(
        ARQUIVO_ALERTAS,
        limite=limite
    )

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

        alertas_formatados.append(
            alerta
        )

    return "\n\n".join(
        alertas_formatados
    )


# ==========================================
# CARREGAR HISTÓRICO
# ==========================================

def carregar_historico(limite=None):

    linhas = ler_linhas(
        ARQUIVO_HISTORICO,
        limite=limite
    )

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

        historico_formatado.append(
            atividade
        )

    return "\n\n".join(
        historico_formatado
    )


# ==========================================
# TESTE DIRETO
# ==========================================

if __name__ == "__main__":
    assistente_inteligente()
