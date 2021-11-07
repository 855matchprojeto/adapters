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

