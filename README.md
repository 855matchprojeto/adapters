# Universidade Estadual de Campinas
# Instituto da Computação

## Disciplina: MC855-2s2021

#### Professor e Assistente

| Nome                     | Email                   |
| ------------------------ | ------------------------|
| Professora Juliana Borin | jufborin@unicamp.br     |
| Assistente Paulo Kussler | paulo.kussler@gmail.com |

#### Equipe

| Nome               | RA               | Email                  | ID Git                |
| ------------------ | ---------------- | ---------------------- |---------------------- |
| Gustavo Henrique Libraiz Teixeira                   | 198537                 | g198537@dac.unicamp.br                     |   nugnu                    |
| Lucas Henrique Machado Domingues                   | 182557                 | l182557@dac.unicamp.br                    |   lhmdomingues                   ||                    |                  |                        |                       |
| Matheus Vicente Mazon                   | 203609                | m203609@dac.unicamp.br                     |   matheusmazon                    |
| Pietro Pugliesi                   | 185921               | p185921@dac.unicamp.br                     |   pietro1704                   |
| Caio Lucas Silveira de Sousa                  | 165461                | c165461@dac.unicamp.br                     |   caiolucasw                    |
| Thomas Gomes Ferreira                  | 224919                | t224919@dac.unicamp.br                     |   Desnord                   |

## Específico sobre esse repositório:
Esse repositório faz parte do projetos da plataforma de Match de Projetos desenvolvido no 2s/2021 para a disciplina MC-855 na Unicamp.

# Visão geral da arquitetura

A arquitetura do back-end será definida em microsserviços. Ao contrário de uma arquitetura convencional monolítica, a aplicação em microsserviços é desmembrada em partes menores e independentes entre si.

Ao fazer o login pelo autenticador, o usuário receberá um token de acesso, com um tempo de expiração bem definido. No token, estarão disponíveis informações como 'username', 'email' e as funções desse usuário no sistema. Ao se comunicar com outros microsserviços, será necessário um header de autenticação, contendo esse token. Cada microsserviço será responsável por descriptografar e validar o token. 

Apesar do microsserviço de autenticação ser responsável pela criação de usuários e suas funções, cada microsserviço implementará seu próprio sistema de permissões, com base nas funções do usuário que fez a requisição. Note que as funções do usuário estarão disponíveis no token de acesso decodificado.

# Descrição

Este serviço de "adapter" é um worker com o objetivo de transmitir mensagens entre serviços.
Para isso, a rotina é definida da seguinte maneira:

- O worker recupera as mensagens de filas SQS
- Essas filas SQS representam mensagens entre serviços. Por exemplo, a fila "SQS_USER_PERFIS" representam mensagens do serviço de autenticação
para o serviço de perfis. 
- Essas mensagens possuem um campo que representam o tipo de evento. Com o tipo de evento, é possível saber do que se trata a mensagem e realizar as regras de negócio ncessárias. Então, o adapter é responsável por executar as regras de negócio ao detectar um evento em que é capaz de lidar. Por exemplo, na criação de perfis, é criado um perfil para o usuário que acabara de ser criado.

**Note que não há um link para esse serviço, pois não se trata de uma API!**

## Estrutura do código

### configuration

Essa pasta é responsável por definir módulos responsáveis por: 

- Conexão com o banco de dados assíncrono
- Variáveis de ambiente
- Exceções customizadas
- Constantes
- Logging

### message_handlers

Classes responsáveis pelas tratativas de mensagens

### repository

Define os métodos que atuam diretamente com banco de dados=

### models

Define as classes que representam o banco de dados, suas tabelas e campos

