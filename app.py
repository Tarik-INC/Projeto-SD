from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from blockchain import Blockchain
from carteira import Carteira
from uuid import uuid4
from time import time

# Instancia o nodo
app = Flask(__name__)
CORS(app, support_credentials=True)

# Gera um endereço global e único para esse nodo G
node_id = str(uuid4()).replace('-', '')

# Instancia a blockchain
blockchain = Blockchain()

@app.route('/')
@cross_origin()
def origin():
   return "The begginning of everything"


@app.route('/mine', methods=['GET'])
def mine():

    # Executa o algoritimo de proof of work de forma a obter a proxima prova
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Recompensa por achar a prova.
    # Colocando o sender como zero evidencia que o nó esta recebendo uma recompensa
    blockchain.new_transaction(
        sender = '0',
        recipient= node_id,
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

    blockchain.notify_nodes()

    return jsonify(resp), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Checa se os dados estao presentes na requisição POST
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Verifica se o pagador de fato possui saldo
    # para realizar a transação
    saldo = Carteira.saldo(values['sender'], blockchain)
    print("\nSaldo de " + str(values['sender']) + " = " + str(saldo))
    if saldo < values['amount']:
        return 'Insufficient funds ', 400

    # Cria uma nova transação
    index = blockchain.new_transaction(
        values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    # metódo retorna uma cadeia inteira de blocos em formato json
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register',methods=['POST'])
def register_nodes():
    # Recebe  uma lista de novos nós conhecidos
    values = request.data

    nodes = values.get('nodes')
    if nodes is None:
       return "Error: Please supply a complete list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    # Verifica se é necessário substituir a cadeia atual
    replaced = blockchain.resolve_conflicts()

    print("Initiating consensus algorithm...")

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
        print("Our chain was replaced")
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
        print("Our chain is authoritative")

    return jsonify(response), 200

if __name__ == 'main':
    
    app.run('0.0.0.0', 5000)





