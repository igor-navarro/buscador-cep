import requests


def buscar_cep(cep):
    """Consulta um CEP na API ViaCEP.

    Retorna um dicionário com os dados do endereço,
    ou None se o CEP for inválido ou não existir.
    """
    # Remove hífen e espaços: "01001-000" -> "01001000"
    cep = cep.replace("-", "").strip()

    # CEP precisa ter exatamente 8 dígitos
    if len(cep) != 8 or not cep.isdigit():
        return None

    resp = requests.get(f"https://viacep.com.br/ws/{cep}/json/", timeout=10)
    resp.raise_for_status()
    dados = resp.json()

    # A ViaCEP responde {"erro": true} quando o CEP não existe
    if dados.get("erro"):
        return None

    return dados


if __name__ == "__main__":
    cep = input("Digite o CEP: ")

    try:
        dados = buscar_cep(cep)
    except requests.RequestException:
        print("Erro ao consultar a API. Verifique sua conexão e tente de novo.")
    else:
        if dados:
            print(f"{dados['logradouro']} - {dados['bairro']}")
            print(f"{dados['localidade']}/{dados['uf']}")
        else:
            print("CEP inválido ou não encontrado.")
