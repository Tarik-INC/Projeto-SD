from flask import Flask, jsonify, request
from blockchain import Blockchain
from uuid import uuid4
from time import time

# Instancia o nodo
app = Flask(__name__)

# Gera um endereço global e único para esse nodo G
node_id = str(uuid4()).replace('-', '')

# Instancia a blockchain
blockchain = Blockchain()

@app.route('/mine', methods=['GET'])
def mine():
    pass


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.data

    #Checa se todas as propriedades paracem no objeto json
    required = ['sender', 'recipient', 'amount']

    if not all(k in values for k in required):
        return 'Invalid transaction data', 400

    #Cria nova transação
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    #Retorna uma mensagem de sucesso
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
    app.run(host='0.0.0.0', port=5000)