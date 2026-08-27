import json

from src.historico import registrar_historico


PROMPT_ZERO_SHOT = """
Você é o Assistente Inteligente do NCAS.
Analise o alerta operacional fornecido usando exclusivamente os dados disponíveis.
Não invente causas, consequências, responsáveis ou soluções.
""".strip()

PROMPT_FEW_SHOT = """
Você é o Assistente Inteligente do NCAS.
Os exemplos abaixo são apenas exemplos didáticos de formato e não representam registros reais.

Exemplo:
Entrada: Módulo Exemplo | Prioridade: Alta | Status: Pendente
Saída: O módulo informado possui um alerta de prioridade Alta com status Pendente.

Agora responda ao alerta fornecido seguindo o mesmo formato e usando somente os dados fornecidos.
""".strip()

PROMPT_SAIDA_ESTRUTURADA = """
Retorne exclusivamente um objeto JSON válido no formato:
{
    "modulo": "",
    "prioridade": "",
    "status": "",
    "descricao": "",
    "resumo": ""
}
Use somente os dados fornecidos. Se um campo não estiver disponível, utilize null.
""".strip()


def exemplo_saida_estruturada():
    exemplo = {
        "modulo": "<módulo informado>",
        "prioridade": "<prioridade informada>",
        "status": "<status informado>",
        "descricao": "<descrição registrada>",
        "resumo": "<resumo baseado somente nos dados fornecidos>",
    }
    return json.dumps(exemplo, ensure_ascii=False, indent=4)


def exibir_prompts():
    print("\n" + "=" * 70)
    print(" PROMPTS ESTRUTURADOS DO NCAS")
    print("=" * 70)

    print("\n1 - PROMPT ZERO-SHOT\n" + "-" * 70)
    print(PROMPT_ZERO_SHOT)

    print("\n2 - PROMPT FEW-SHOT\n" + "-" * 70)
    print(PROMPT_FEW_SHOT)

    print("\n3 - PROMPT DE SAÍDA ESTRUTURADA\n" + "-" * 70)
    print(PROMPT_SAIDA_ESTRUTURADA)

    print("\n4 - EXEMPLO DE STRUCTURED OUTPUT\n" + "-" * 70)
    print(exemplo_saida_estruturada())

    registrar_historico(
        "Consulta de prompts",
        "Sistema",
        "Prompts zero-shot, few-shot e saída estruturada exibidos.",
    )
