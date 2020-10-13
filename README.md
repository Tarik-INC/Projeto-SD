# Projeto-SD
Protótipo que simula a blockchain, apresentado como trabalho prático para a disciplina de SD

## Guia de instalação

1.  Na pasta ./projeto-SD/ inicie a API da blockchain

```
python  app.py
```

2. Registre todos os nós da rede manualmente no arquivo registrar_nos.py e inicie o arquivo:

```
python registrar_nos.py
```

3. O programa já esta pronto para receber requisições,  como exemplo, digite no seu browser:

```
http://{ip_da_máquina}:5000/
```

4. (opcional) Inicie a aplicação web para mineração e listagem de transações verificadas, indo para a pasta /chain_explorer e utilize os seguintes comandos (NPM 8.6+):

```
npm install
npm start
```

![](/documents/instalacao.gif)

## Descrição

Nesse trabalho prático, foi proposto a criação de um sistema de transações financeiras baseado no funcionamento da blockchain, que se compõem como um  registro de transações  totalmente descentralizado, que configura  a base do funcionamento da  famosa moeda virtual bitcoin. Nesse contexto, objetivamos a criação da nossa própria moeda virtual, a llibertatem (do latim liberdade),  através da criação de um sistema completo de transações em uma rede P2P, ao qual é eliminada a entidade central, responsável por validar  e armazenar as transações , presente em sistemas tradicionais como TEDS, Paypal, cartões de crédito, etc. em que a responsabilidade desta entidade é transferida para cada nó na rede, formalizando um sistema descentralizado de transações.

Contudo, devido a complexidade de conhecimento apresentadas pela blockchain e limitações impostas de tempo a apresentação do projeto a disciplina, foi determinada a criação de um protótipo mais simples que se comporta de maneira semelhante, mas não igual, a uma implementação real da blockchain, de forma a lançar os primeiros passos para construção e publicação de uma moeda virtual totalmente funcional.

#### O que foi feito
- Implementação da  simulação da blockchain em python
- Implementação da API em flask, que disponibiliza os serviços e recursos da blockchain na rede.
- Implementaçao em python de um pequeno programa auxiliar para registro de nós de uma rede, armazenado por um nó.
- Implemntação do front-end para realizar transações válidas utilizando Javacsript, Css e React.
- Implementação do front-end, em React, para visualização das transações validadas seus respectivos blocos, além de ser utilizada para acionar o algoritmo de mineração.

### O que faltou fazer

- Determinar um meio mais inteligente de cadastro de nós conhecidos na rede, bem como seu gerenciamento.
- Criação de um algoritmo de distribuição de transações para todos os nós, atualmente ele é apenas local.
- Desenvolvimento de apenas uma aplicação front-end responsavel por todas as interfaces já criadas e com capacidade de explorar novas funcionalidades.
- Melhoria do algoritmo de mineração e consenso de nós em uma rede, é ncessario um estudo mais profundo sobre como a blockchain delega tais funções, já que o protótipo possui algumas disparidades em relação ao ideal.
-  Utilização do protótipo em redes maiores. (testado apenas com dois nodos)

#### Arquitetura geral do sistema
 
![Arquitetura do projeto](documents/arquitetura.png?raw=true "Arquitetura geral do sistema")

