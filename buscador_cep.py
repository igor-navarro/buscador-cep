import re
import sqlite3
import requests

DB = "historico.db"


def criar_tabela(conn: sqlite3.Connection) -> None:
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


def consultar_viacep(cep: str) -> dict | None:
    resposta = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=5)
    resposta.raise_for_status()
    dados = resposta.json()
    if dados.get("erro"):
        return None
    return dados


def consultar_brasilapi(cep: str) -> dict | None:
    resposta = requests.get(f"https://brasilapi.com.br/api/cep/v1/{cep}", timeout=5)
    if resposta.status_code == 404:
        return None
    resposta.raise_for_status()
    d = resposta.json()
    # converte para o mesmo formato da ViaCEP
    return {
        "cep": d.get("cep"),
        "logradouro": d.get("street"),
        "bairro": d.get("neighborhood"),
        "localidade": d.get("city"),
        "uf": d.get("state"),
    }


def buscar_cep(cep: str) -> dict | None:
    cep = re.sub(r"\D", "", cep)  # remove traço e pontos

    if len(cep) != 8:
        print("CEP inválido: precisa ter 8 dígitos.")
        return None

    for consulta in (consultar_viacep, consultar_brasilapi):
        try:
            dados = consulta(cep)
        except (requests.exceptions.RequestException, ValueError):
            continue  # essa API falhou, tenta a próxima

        if dados:
            return dados
        print("CEP não encontrado.")
        return None

    print("Erro de conexão com as APIs.")
    return None


def salvar_historico(dados: dict) -> None:
    with sqlite3.connect(DB) as conn:
        criar_tabela(conn)
        conn.execute(
            "INSERT INTO consultas (cep, logradouro, bairro, cidade, uf) VALUES (?, ?, ?, ?, ?)",
            (
                dados.get("cep"),
                dados.get("logradouro"),
                dados.get("bairro"),
                dados.get("localidade"),
                dados.get("uf"),
            ),
        )


def listar_historico() -> None:
    with sqlite3.connect(DB) as conn:
        criar_tabela(conn)
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