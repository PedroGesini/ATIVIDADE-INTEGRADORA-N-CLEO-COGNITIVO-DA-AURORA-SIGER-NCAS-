import json
import os
from tabulate import tabulate

from historico import registrar_historico


# ==========================================
# DADOS DOS MÓDULOS DA COLÔNIA
# ==========================================

colonia_aurora_siger = {
    "Habitação": {
        "consumo_energetico_kwh": 120,
        "prioridade_operacional": 2,
        "capacidade_armazenamento": "500 kWh / 1000L Água",
        "necessidade_comunicacao": "Média",
        "status_operacional": "Ativo",
        "conexoes": [
            ("Centro de controle", 50),
            ("Suporte médico", 20),
            ("Produção de oxigênio", 80),
            ("Agricultura", 100)
        ]
    },

    "Centro de controle": {
        "consumo_energetico_kwh": 85,
        "prioridade_operacional": 1,
        "capacidade_armazenamento": "Servidores / Nobreaks",
        "necessidade_comunicacao": "Altíssima",
        "status_operacional": "Ativo",
        "conexoes": [
            ("Habitação", 50),
            ("Comunicação", 30),
            ("Armazenamento de energia", 150),
            ("Laboratório científico", 120)
        ]
    },

    "Armazenamento de energia": {
        "consumo_energetico_kwh": 15,
        "prioridade_operacional": 1,
        "capacidade_armazenamento": "50.000 kWh",
        "necessidade_comunicacao": "Média",
        "status_operacional": "Ativo",
        "conexoes": [
            ("Centro de controle", 150),
            ("Produção de oxigênio", 200),
            ("Agricultura", 300)
        ]
    },

    "Agricultura": {
        "consumo_energetico_kwh": 250,
        "prioridade_operacional": 3,
        "capacidade_armazenamento": "Estufas / Água",
        "necessidade_comunicacao": "Baixa",
        "status_operacional": "Ativo",
        "conexoes": [
            ("Habitação", 100),
            ("Armazenamento de energia", 300),
            ("Laboratório científico", 60)
        ]
    },

    "Laboratório científico": {
        "consumo_energetico_kwh": 180,
        "prioridade_operacional": 4,
        "capacidade_armazenamento": "Amostras / Equipamentos",
        "necessidade_comunicacao": "Alta",
        "status_operacional": "Ativo",
        "conexoes": [
            ("Centro de controle", 120),
            ("Agricultura", 60),
            ("Suporte médico", 90)
        ]
    },

    "Comunicação": {
        "consumo_energetico_kwh": 95,
        "prioridade_operacional": 2,
        "capacidade_armazenamento": "Terabytes",
        "necessidade_comunicacao": "Altíssima",
        "status_operacional": "Ativo",
        "conexoes": [
            ("Centro de controle", 30)
        ]
    },

    "Suporte médico": {
        "consumo_energetico_kwh": 60,
        "prioridade_operacional": 1,
        "capacidade_armazenamento": "Suprimentos médicos",
        "necessidade_comunicacao": "Média",
        "status_operacional": "Ativo",
        "conexoes": [
            ("Habitação", 20),
            ("Laboratório científico", 90)
        ]
    },

    "Produção de oxigênio": {
        "consumo_energetico_kwh": 300,
        "prioridade_operacional": 1,
        "capacidade_armazenamento": "Tanques O2",
        "necessidade_comunicacao": "Baixa",
        "status_operacional": "Ativo",
        "conexoes": [
            ("Habitação", 80),
            ("Armazenamento de energia", 200)
        ]
    }
}


ARQUIVO_JSON = "dados_colonia.json"


# ==========================================
# CRIAR / ATUALIZAR JSON
# ==========================================

def criar_dados_json():

    with open(ARQUIVO_JSON, "w", encoding="utf-8") as arquivo:

        json.dump(
            {
                "modulos": colonia_aurora_siger
            },
            arquivo,
            ensure_ascii=False,
            indent=4
        )


# ==========================================
# CARREGAR DADOS
# ==========================================

def carregar_dados():

    if not os.path.exists(ARQUIVO_JSON):
        criar_dados_json()

    try:

        with open(
            ARQUIVO_JSON,
            "r",
            encoding="utf-8"
        ) as arquivo:

            dados = json.load(arquivo)

        return dados

    except (json.JSONDecodeError, EOFError):

        print("Arquivo dados_colonia.json inválido ou vazio.")
        print("Recriando arquivo...")

        criar_dados_json()

        with open(
            ARQUIVO_JSON,
            "r",
            encoding="utf-8"
        ) as arquivo:

            return json.load(arquivo)


# ==========================================
# CONSULTAR TODOS OS MÓDULOS
# ==========================================

def consultar_modulos():

    print("\n")
    print("=" * 120)
    print("                 STATUS DOS MÓDULOS DA COLÔNIA AURORA SIGER")
    print("=" * 120)

    dados = carregar_dados()

    modulos = dados.get("modulos", {})

    if not modulos:

        print("Nenhum módulo cadastrado.")
        return

    tabela = []

    for nome, info in modulos.items():

        conexoes = ", ".join(
            f"{destino} ({distancia}m)"
            for destino, distancia in info["conexoes"]
        )

        tabela.append([
            nome,
            info["status_operacional"],
            info["prioridade_operacional"],
            f"{info['consumo_energetico_kwh']} kWh",
            info["necessidade_comunicacao"],
            info["capacidade_armazenamento"],
            conexoes
        ])

    cabecalho = [
        "Módulo",
        "Status",
        "Prioridade",
        "Consumo",
        "Comunicação",
        "Armazenamento",
        "Conexões"
    ]

    print(
        tabulate(
            tabela,
            headers=cabecalho,
            tablefmt="grid"
        )
    )

    print("=" * 120)

    # ==========================================
    # REGISTRAR NO HISTÓRICO
    # ==========================================

    registrar_historico(
        "Consulta de módulos",
        "Sistema",
        "Consulta geral dos módulos da colônia"
    )


# ==========================================
# CONSULTAR MÓDULO ESPECÍFICO
# ==========================================

def consultar_modulo_especifico():

    dados = carregar_dados()

    modulos = dados.get("modulos", {})

    if not modulos:

        print("Nenhum módulo cadastrado.")
        return

    print("\nMódulos disponíveis:")

    for nome in modulos:

        print(f"- {nome}")

    nome = input("\nDigite o nome do módulo: ").strip()

    info = modulos.get(nome)

    if info is None:

        print("Módulo não encontrado.")
        return

    print("\n" + "=" * 60)
    print(f"              {nome.upper()}")
    print("=" * 60)

    print(
        f"Status:                 "
        f"{info['status_operacional']}"
    )

    print(
        f"Prioridade operacional: "
        f"{info['prioridade_operacional']}"
    )

    print(
        f"Consumo energético:     "
        f"{info['consumo_energetico_kwh']} kWh"
    )

    print(
        f"Comunicação:            "
        f"{info['necessidade_comunicacao']}"
    )

    print(
        f"Armazenamento:          "
        f"{info['capacidade_armazenamento']}"
    )

    print("\nConexões:")

    for destino, distancia in info["conexoes"]:

        print(
            f"  → {destino}: {distancia}m"
        )

    print("=" * 60)

    # ==========================================
    # REGISTRAR NO HISTÓRICO
    # ==========================================

    registrar_historico(
        "Consulta de módulo",
        nome,
        f"Consulta detalhada do módulo {nome}"
    )


# ==========================================
# TESTE DO ARQUIVO
# ==========================================

if __name__ == "__main__":

    consultar_modulos()