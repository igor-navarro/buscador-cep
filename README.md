# Buscador de CEP

Programa em Python que consulta o endereço de um CEP usando a API pública [ViaCEP](https://viacep.com.br/) (gratuita, sem chave). Se a ViaCEP estiver fora do ar, ele tenta automaticamente a [BrasilAPI](https://brasilapi.com.br/). Cada consulta fica salva em um histórico local.

## Funcionalidades

- Consulta de endereço por CEP (aceita `01001000` ou `01001-000`)
- Validação do CEP (8 dígitos)
- Fallback automático para a BrasilAPI se a ViaCEP falhar
- Tratamento de erros: CEP inexistente, falha de conexão, timeout e resposta inválida
- Histórico das últimas consultas salvo em SQLite (`historico.db`, criado automaticamente)

## Tecnologias

- Python 3.10+
- [requests](https://pypi.org/project/requests/)
- SQLite (já vem com o Python)

## Estrutura do projeto

```
buscador-cep/
├── buscador_cep.py   # código principal
├── requirements.txt  # dependências
├── README.md         # documentação
└── .gitignore        # ignora o historico.db
```

## Como rodar

1. Clone o repositório:

```
git clone https://github.com/igor-navarro/buscador-cep.git
cd buscador-cep
```

2. Instale as dependências:

```
pip install -r requirements.txt
```

3. Execute o programa:

```
python buscador_cep.py
```

4. Digite um CEP (ex: `01001000` ou `01001-000`) e veja o endereço.
5. Digite `h` para ver as últimas 10 consultas.

## Exemplo de uso

```
Digite o CEP (ou 'h' para ver o histórico): 01001-000
Praça da Sé, Sé - São Paulo/SP
```

```
Digite o CEP (ou 'h' para ver o histórico): 123
CEP inválido: precisa ter 8 dígitos.
```

## Como funciona

1. O CEP digitado é limpo (só números) e validado.
2. A consulta vai para a ViaCEP. Se der erro de conexão ou resposta inválida, tenta a BrasilAPI.
3. Se o endereço for encontrado, é exibido e salvo no `historico.db`.

## Próximos passos

- [x] Histórico de consultas em banco
- [x] Fallback com BrasilAPI
- [ ] Cache das consultas
- [ ] Testes com pytest
- [ ] Versão em Java
