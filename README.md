# Sistema de Transações Bancárias com Concorrência de Saldo

## Descrição

Este sistema é uma implementação de um sistema de contas bancárias utilizando Django e Django Rest Framework.
Ele permite criar contas, realizar depósitos, saques e transferências entre contas.

## Requisitos

- Python 3.8+
- Django 3.2+
- Django Rest Framework 3.12+

Instalação

## 1. Clone o repositório:

```bash
git clone git@github.com:lfstos/banco.git
```

## 1. Crie um ambiente virtual:

```bash
python -m venv .venv
```

## 1. Ative o ambiente virtual:

```bash
source .venv/bin/activate
```

## 1. Instale as dependências:

```bash
pip install -r requirements.txt
```

## 1. Rode as migrações:

```bash
python manage.py migrate
```

# Exemplo de Uso

## Criar Conta

- URL: http://localhost:8000/contas/
- Método: POST
- Corpo da requisição:

```json
{
    "numero": 123,
    "saldo": 100.00
}
```

- Resposta:

```json
{
    "numero": 123,
    "saldo": 100.00
}
```

## Realizar Depósito

- URL: http://localhost:8000/transacoes/
- Método: POST
- Corpo da requisição:

```json
{
    "tipo": "deposito",
    "conta": 123,
    "valor": 50
}
```

- Resposta:

```json
{
    "Saldo da Conta": 50.0
}
```

## Realizar Saque

- URL: http://localhost:8000/transacoes/
- Método: POST
- Corpo da requisição:

```json
{
    "tipo": "saque",
    "conta": 125,
    "valor": 100
}
```

- Resposta:

```json
{
    "Saldo da Conta": 50
}
```

## Realizar Transferência

- URL: http://localhost:8000/transacoes/
- Método: POST
- Corpo da requisição:

```json
{
    "tipo": "transferencia",
    "conta": 123,
    "destino": 456,
    "valor": 30.00
}
```

- Resposta:

```json
{
    "Saldo da Conta": [
        {
            "numero": 123,
            "saldo": 100.0
        },
        {
            "numero": 456,
            "saldo": 20
        }
    ]
}
```

## Realizar Sistema de Transações Bancárias com Concorrência de Saldo

- URL: http://localhost:8000/transacoes/
- Método: POST
- Corpo da requisição:

```json
{
  "contas": [
    {
        "numero": 123
    }
  ],
  "transacoes": [
    {"tipo": "deposito", "conta": 123, "valor": 500},
    {"tipo": "saque", "conta": 123, "valor": 30},
    {"tipo": "transferencia", "origem": 123, "destino": 456, "valor": 20}
  ]
}
```

- Resposta:

```json
{
    "Saldos das Contas": [
        {
            "numero": 123,
            "saldo": 450.0
        }
    ]
}
```

# Rodar o Sistema

## 1. Rode o servidor:

```bash
python manage.py runserver
```

1. Acesse o sistema em
```bash
http://localhost:8000/api/contas/
http://localhost:8000/api/transacoes/
```