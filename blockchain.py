import hashlib
import json
from time import time

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        #Criação do bloco genesis
        self.new_block(previous_hash=1, proof=100)

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
            'transaction': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []

        self.chain.append(block)
        return block

        
    def new_transaction(self, sender, recipient, amount):
        
        """ 
        Adiciona uma nova transação para a lista de transações em um próximo Bloco minado
        
        :param sender: <str> Endereço do emissor
        :param recipient: <str> Endereço do recebedor
        :param amount: <int> Quantidade
        :return: <int> Index do bloco que irá armazenar a transação
        """
        self.current_transactions.append({
            'sender':sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1
        
    
    
    @property
    def last_block(self):
        #Retorna o ultimo bloco na cadeia
        return self.chain[-1]

    @staticmethod
    def hash(block):
        """
        Cria um hash SHA-256 de um bloco
        :param block: <dict> Bloco
        :return: <str> hash
        """

        # Nos devemos ter certeza que nosso dicionário está ordenado, ou nós poderemos ter hashes incorretos
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
