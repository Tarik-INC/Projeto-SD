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
    pass


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    pass

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200
