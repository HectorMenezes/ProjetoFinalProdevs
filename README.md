## Introdução


Nosso projeto final consiste no desenvolvimento de uma API que atuará como gateway para um serviço externo. Ela será responsável por receber um ou mais pedidos, validar a informação, efetuar a chamada na API externa, armazenar o resultado da operação e retornar o status para o originador. Esta API deve ser capaz de "plugar" mais serviços externos futuramente.


Os usuários de nosso sistema irão utilizar o sistema para enviar solicitações de compra e iremos direcionar, após validação, para a API externa. O processo de compra feito pelos clientes segue as seguintes regras:

 - Um cliente deve efetuar um cadastro prévio para que possa solicitar a compra.
 - Um cliente pode mandar um ou mais itens de compra.
 - Um cliente pode solicitar o cancelamento de um item que foi comprado (Necessário enviar uma solicitação para a API externa).
 - Uma operação somente deve ser considerada sucesso se **todos** itens enviados forem processados com sucesso pela api externa.
 - Todas operações devem ficar registradas no sistema.


### Estrutura de dados

#### Cliente

Os clientes deverão fornecer os seguintes dados para cadastro:

 - Nome: String de até 100 caracteres
 - CPF: Apenas digitos. (Se possível aplicar [validação](https://www.geradorcpf.com/algoritmo_do_cpf.htm))
 - Email: String de até 200 caracteres que respeite a estrutura básica para um e-mail
 - Data de nascimento: Date
 - Telefone: String de 13 caracteres (DDI + DDD + NNNNNNNNN)


 Exemplo:

 ```json
 {
    "nome": "José da Silva",
    "cpf": "00112345600",
    "email": "jose.silva@gmail.com",
    "data_nascimento": "1990-01-01",
    "telefone": "5511999999999"
 }

 ```

#### Item para compra


Um item de compra deve ser composto pelos seguintes atributos:

 - Código: String de até 200 caracteres com o código do produto que será comprado.
 - Nome: String de até 100 caracteres.
 - Quantidade: Inteiro positivo

No payload eles enviarão o identificador único, que é o CPF, juntamente com uma lista de itens.

Exemplo
```json
{
    "cliente": "00112345600",
    "itens": [
        {
            "codigo": "abcdo1344123",
            "quantidade": 2
        }
    ]
}

```

### Retornos

Nossa API deverá sempre retornar o status da operação respeitando as regras descritas acima. Os retornos deverão seguir as recomendações de código de retorno HTTP juntamente com um `status` com os seguintes valores possíveis:

 - SUCESSO: A operação foi realizada com sucesso no sistema. Quando uma compra for realizada com sucesso, deve-se retornar o código da mesma.
 - FALHA_NO_PARCEIRO: Quando a requisição foi enviada para o parceiro, este retornou algo inesperado.
 - FALHA_INTERNA: Ocorreu um erro inesperado na API.
 - REQUISICAO_INVALIDA: A chamada possui uma condição inválida para o sistema. Exemplo: Tentar comprar algo com um CPF não cadastrado. Neste caso, a resposta deve conter o atributo `descricao` que conterá o motivo.

 Também retornaremos os erros de falha de validação do schema do pydantic.


Exemplo de cadastro realizado com sucesso:
```json
{
  "status": "SUCESSO"
}
```

Exemplo de compra efetuada com sucesso:
```json
{
    "status": "SUCESSO",
    "pedido": "ABCD1234",
    "valor_total": 100.00,
    "itens": [
      {
            "codigo": "12341asdbas",
            "nome": "Super Avião submarino",
            "valor": 250.00,
            "quantidade": 2,
            "total": 500.00
        },
        {
            "codigo": "0010aL188",
            "nome": "Lango-Lango",
            "preco": 80.00,
            "quantidade": 1,
            "total": 80.00
        }
    ]
}
```


### Rotas da API


 - `GET /produtos`: Deve pesquisar e retornar o catálogo de produtos na API externa.
 - `GET /compras/{cpf}`: Retorna a lista de compras feitas pelo cliente.
 - `POST /compras`: Solicita a compra de itens
 - `DELETE /compras/{cpf}/{pedido}/{item}`: Cancela a compra de um produto na API local e na API externa.
 - `POST /clientes`: Efetua o cadastro do cliente na API
 - `GET /clientes/{cpf}`: Retorna os dados cadastrais do cliente
 - `PATCH /clientes/{cpf}`: Atualiza os dados de um cliente, exceto o CPF.
 - `DELETE /clientes/{cpf}`: Cancela o cadastro de um cliente no sistema (Não necessariamente o remove)



### API Externa



Nossa API parceira é relativamente simples e possui as rotas listadas abaixo para consumo, todas as rotas irão requerer a autenticação através de um token que será compartilhado juntamente com os dados de acesso a API.

A API externa não segue as convenções de código de retorno HTTP, então teremos que efetuar um trabalho adicional de validação dos status. Esta API sempre retorna 200 e em seu payload consta o campo booleano `status` que descreve o resultado da operação.


`GET /produtos`: Retorna uma lista de produtos disponíveis para compra

Exemplo:

```json
{
    "status": true,
    "produtos": [
        {
            "codigo": "12341asdbas",
            "nome": "Super Avião submarino",
            "preco": 250.00,
            "quantidade": 100
        },
        {
            "codigo": "0010aL188",
            "nome": "Lango-Lango",
            "preco": 80.00,
            "quantidade": 20
        }
    ]
}
```

`DELETE /compras/{pedido}/{codigo}`: Cancela a compra de um produto do cliente.

```json
{
  "status": true
}
```


`POST /compras`: Recebe e computa um pedido de compra

Payload de entrada:

```json
{
  "cliente": "00112345600",
  "itens":[
    {
        "codigo": "12341asdbas",
        "quantidade": 2
    },
    {
        "codigo": "0010aL188",
        "quantidade": 1
    }
  ]
}
```


Exemplo de retorno:
```json
{
    "status": true,
    "pedido": "abcasd1233",
    "itens": [
        {
            "codigo": "12341asdbas",
            "nome": "Super Avião submarino",
            "valor": 250.00,
            "quantidade": 2,
            "total": 500.00
        },
        {
            "codigo": "0010aL188",
            "nome": "Lango-Lango",
            "preco": 80.00,
            "quantidade": 1,
            "total": 80.00
        }
    ]
}
```


Quando ocorre um erro no processamento, a API retorna uma estrutura semelhante a exibida abaixo, porém é sabido que a mesma tem um comportamento instável e nem sempre respeita o especificado na documentação.

```json
{
	"status": false,
	"mensagem": "Erro ao tentar registrar a compra"
}
```

### Objetivos


Para que a API seja considerada pronta, ela deve:

 - Ser executada no Docker
 - Possuir um banco de dados para persistência das informações
 - Utilizar migrações para criação da estrutura de dados
 - Todas as rotas devem apresentar a documentação e descrição dos atributos utilizando `redoc` (https://fastapi.tiangolo.com/tutorial/metadata/?h=redoc#docs-urls)
 - A cobertura mínima é de 85% do código
 - A pontuação do pylint deve ser no mínimo de 9.00
 - Nenhuma classe ou método deve possuir uma pontuação de complexidade do código inferior a `B` (`radon cc src/*`)

Será considerado um plus se a API utilizar `aiohttp` e um super ultra blaster plus se utilizar `asyncpg` (Sei que não vimos este conteúdo, por isso não se sinta pressionado em utilizar, mas é um desafio bem bacana.)


Também ficam algumas perguntas:

 - Como poderíamos conectar mais de uma API externa em nosso sistema ?
 - Como poderíamos fornecer uma interface transparente para os clientes efetuarem compras ?
 - Quão complexo seria criar um mecanismo que permita o cliente efetuar a compra de produtos de APIs externas distintas em um mesmo pedido ?
 - Como foi o processo de consumo da API externa ? Poderia ser melhor? Se sim, como ?