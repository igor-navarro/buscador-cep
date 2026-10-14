import re
import sqlite3
import requests


def buscar_cep(cep: str) -> dict | None:
    cep = re.sub(r"\D", "", cep)  # remove traço e pontos

    if len(cep) != 8:
        print("CEP inválido: precisa ter 8 dígitos.")
        return None

    try:
        resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5)
        resposta.raise_for_status()
        dados = resposta.json()
    except requests.exceptions.RequestException:
        print("Erro de conexão com a API.")
        return None

    if dados.get("erro"):
        print("CEP não encontrado.")
        return None

    return dados


def salvar_historico(dados: dict) -> None:
    with sqlite3.connect("historico.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cep TEXT,
                logradouro TEXT,
                bairro TEXT,
                cidade TEXT,
                uf TEXT,
                consultado_em TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute(
            "INSERT INTO consultas (cep, logradouro, bairro, cidade, uf) VALUES (?, ?, ?, ?, ?)",
            (dados["cep"], dados["logradouro"], dados["bairro"], dados["localidade"], dados["uf"]),
        )


def listar_historico() -> None:
    with sqlite3.connect("historico.db") as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cep TEXT, logradouro TEXT, bairro TEXT,
                cidade TEXT, uf TEXT,
                consultado_em TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        linhas = conn.execute(
            "SELECT cep, cidade, uf, consultado_em FROM consultas ORDER BY id DESC LIMIT 10"
        ).fetchall()

    if not linhas:
        print("Nenhuma consulta no histórico ainda.")
        return

    for cep, cidade, uf, data in linhas:
        print(f"{data} | {cep} | {cidade}/{uf}")


if __name__ == "__main__":
    entrada = input("Digite o CEP (ou 'h' para ver o histórico): ")

    if entrada.strip().lower() == "h":
        listar_historico()
    else:
        resultado = buscar_cep(entrada)
        if resultado:
            print(f"{resultado['logradouro']}, {resultado['bairro']} - {resultado['localidade']}/{resultado['uf']}")
            salvar_historico(resultado)