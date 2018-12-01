from flask import Flask, jsonify, request
from blockchain import Blockchain
from uuid import uuid4
from time import time

# Instancia o nodo
app = Flask(__name__)

# Gera um endereço global e único para esse nodo G
node_identifier = str(uuid4()).replace('-', '')

# Instancia a blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():

    # Executa o algoritimo de proof of work de forma a obter a proxima prova
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Recompensa por acha a prova.
    # Colocando o sender como zero evidencio que o no esta recebendo uma recompensa
    blockchain.new_transaction(
        sender = '0',
        recipient=node_identifier,
        amount=1,
    )

    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    resp = {
        'message': 'new block created',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(resp), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Checa se os dados estao presentes na requisição POST
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Cria uma nova transação
    index = blockchain.new_transaction(
        values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

if __name__ == 'main':
    app.run('0.0.0.0', 5000)
