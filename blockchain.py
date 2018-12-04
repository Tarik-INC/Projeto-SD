import hashlib
import json
import requests
from time import time
from urllib.parse import urlparse
from datetime import datetime


class Blockchain(object):

    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Criação do bloco genesis
        self.new_block(previous_hash=1, proof=100)
        # Armazenar informações de nodos na rede
        self.nodes = set()

    def register_node(self, address):
        """
        Adiciona um novo nodo para a lista de nodos conhecidos

        :param addres: <str> Endereço de um nodo. Eg. 'http://192.168.0.12:5000'
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def notify_nodes(self):
        """
            Metódo responsável por automaticamente notificar os nós da rede,
            invocado apos um nó minerar um bloco, na qual se torna necessário
            saber quem possui a maior cadeia de blocos em uma rede
        """

        for node in self.nodes:
            response = requests.get(f'http://{node}/nodes/resolve')
            msg = response.json()['message']
            print(
                f'Notificando todos os nós da rede após minerar um bloco, o resultado é {msg} ')

    def proof_of_work(self, last_proof):
        """
        Algoritimo simples de uma prova de trabalho
            - Ache um número p' tal que o hash(pp') contenha 4 zeros seguidos, 
            onde p representa o número de prova anterior e p' o atual

            :param last_proof: <int>
            :return: <int>
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Valida a prova: Faz hash(last_proof, proof) contem 4 zeros seguidos?
        :param last_proof: <int> Prova anterior
        :param proof: <int> Prova atual
        :return: <bool> Verdadeiro se correto, Falso se não.
        """

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def new_block(self, proof, previous_hash=None):
        """
        Cria um novo bloco e adiciona a blockchain

        :param proof: <int> A prova disponibilizada pela Proof do algoritimo work 
        :param previous_hash: (Optional) <str> Hash do bloco anterior 
        :return: <ditc> novo bloco
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        block_time = datetime.utcfromtimestamp(
            block['timestamp']).strftime(' % d-%m-%Y % H: % M: % S')

        block_index = block['index']

        print(
            f'Um novo bloco#{block_index} foi criado\nhash:{Blockchain.hash(block)}')

        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """ 
        Adiciona uma nova transação para a lista de transações em um próximo bloco minado

        :param sender: <str> Endereço do emissor
        :param recipient: <str> Endereço do recebedor
        :param amount: <int> Quantidade
        :return: <int> Index do bloco que irá armazenar a transação
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        print(
            f"Nova transação adicionada. De {sender} para {recipient} com {amount} como quantidade")

        return self.last_block['index'] + 1

    @property
    def last_block(self):
        # Retorna o ultimo bloco na cadeia
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Cria um hash SHA-256 de um bloco
        :param block: <dict> Bloco
        :return: <str> hash
        """

        # Nós devemos ter certeza que nosso dicionário está ordenado, ou nós poderemos ter hashes incorretos
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def valid_chain(self, chain):
        """
        Determina se uma determinada cadeia de blocos(blockchain) é válida

        :param chain: <list> A blockchain
        :return: <bool> True se válido, False se não
        """

        last_block = chain[0]
        index = 1

        while index < len(chain):
            block = chain[index]

            if block['previous_hash'] != self.hash(last_block):
                return False

            if not(self.valid_proof(last_block['proof'], block['proof'])):
                return False

            last_block = block
            index += 1

        return True

    def resolve_conflicts(self):
        """
            Algoritmo de consenso, que resolve conflitos substituindo
            nossa cadeira pelo maior existente na rede

            :return: <bool> True se nossa cadeia foi substituida, False se não
        """

        neighbours = self.nodes
        new_chain = None

        # Garantirmos o interesse apenas por cadeias maiores que a nossa
        max_length = len(self.chain)

        # Pega e verifica as cadeias de todos os nós na rede
        for node in neighbours:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

        # Checa se o tamanho é maior e se a cadeia é valida
            if length > max_length and self.valid_chain(chain):
                max_length = length
                new_chain = chain

        if new_chain:
            self.chain = new_chain

            return True

        return False
