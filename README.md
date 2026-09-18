# Buscador de CEP

Consulta o endereço de um CEP usando a API pública [ViaCEP](https://viacep.com.br/) (gratuita, sem chave).

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

## Próximos passos

- [ ] Histórico de consultas em banco
- [ ] Cache das consultas
- [ ] Fallback com BrasilAPI
- [ ] Testes com pytest
- [ ] Versão em Java
