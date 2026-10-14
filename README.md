# Buscador de CEP

Consulta o endereço de um CEP usando a API pública [ViaCEP](https://viacep.com.br/) (gratuita, sem chave).

## Funcionalidades

- Consulta de endereço por CEP (aceita `01001000` ou `01001-000`)
- Validação do CEP (8 dígitos)
- Tratamento de erros: CEP inexistente, falha de conexão e timeout
- Histórico das consultas salvo em SQLite (`historico.db`, criado automaticamente)

## Como rodar

1. Instale as dependências:

```
pip install -r requirements.txt
```

2. Execute o programa:

```
python buscador_cep.py
```

3. Digite um CEP (ex: `01001000` ou `01001-000`) e veja o endereço.
4. Digite `h` para ver as últimas 10 consultas.

> O SQLite já vem com o Python, não precisa instalar nada além do `requests`.

## Próximos passos

- [x] Histórico de consultas em banco
- [ ] Cache das consultas
- [ ] Fallback com BrasilAPI
- [ ] Testes com pytest
- [ ] Versão em Java