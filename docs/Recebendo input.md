# Rebendo input dos usuarios

## Verificando os campos do layout

Fazendo um GET /layout/{layout_id} retorna as informações do layout, inclusive os campos.

Atualmente os campos são `datas`, `numdocs`, `valores` e `historicos`

### Exemplo de informações de layout:

layout com campo nomeado:

```json
{
  "layout": 57,
  "tipo": "BANCO",
  "descricao": "ITAÚ",
  "detalhe": "EMPRESAS",
  "solicitapassword": false,
  "solicitainput": false,
  "tituloinput": "",
  "datas": [
    {
      "titulo": "Ano",
      "campo": "data",
      "solinput": true,
      "inputtitulo": "Informe o ano dos lançamentos, contendo 4 dígitos.",
      "rotulo": "Exemplo: 2026"
    }
  ]
}
```

layout com campo genérico:

```json
{
  "layout": 6311,
  "tipo": "Softwares",
  "descricao": "RAD INFORMATICA",
  "detalhe": "CONTAS A PAGAR",
  "solicitapassword": false,
  "solicitainput": true,
  "tituloinput": "Informe a data dos registros."
}
```

Os campos são um array com informações de campo.

Na informação do campo, tem o `solinput` que caso esteja `true`, é para soliciar ao o usuario aquela informação.

Tambem tem o `solicitainput`, que é para uma solicitação mais generica.

## Enviando para API

Dentro do um campo `input`, deve enviar um array, com o nome do campo e o valor.

Caso seja o `solicitainput`, deve enviar o nome do campo como `valor`

### Exemplo de como enviar:

Com campo nomeado:

```json
input: {
    "data": "2020"
}
```

Com campo genérico:

```json
input: {
    "valor": "12/12/2020"
}
```

## Pegando o input do usuario nos Layouts

Dentro da classe `Arquivo`, tem um dict `input_val`, como os inputs recebidos, para pegar basta usar o `.get([nome_do_campo])`, que se tiver vai retornar.

Caso não tiver o `.get()` vai retornar `None`

Exemplo:

``` py
ano = file_obj.input_val.get('data')
```
