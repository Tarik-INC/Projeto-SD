from flask import Flask, jsonify, request, render_template
from flask_cors import CORS, cross_origin
from blockchain import Blockchain
from carteira import Carteira
from uuid import uuid4
from time import time
from flask import send_file
import json

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

    print('Iniciando mineração....')
    # Executa o algoritimo de proof of work de forma a obter a proxima prova
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)

    # Recompensa por achar a prova.
    # Colocando o sender como zero evidencia que o nó esta recebendo uma recompensa
    blockchain.new_transaction(
        sender='0',
        recipient=node_id,
        amount=1,
    )

    #Pode acontecer da cadeia do nó ser substituída, nesse caso as transações são armazenadas
    # e enviadas para o metódo notify_nodes
    backup_transactions = blockchain.current_transactions
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    resp = {
        'message': 'Novo bloco criado',
        'index': block['index'],
        'transactions': block['transactions'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }

    # Em caso de substituição da cadeia as transações são mantidas
    blockchain.notify_nodes(previous_transactions=backup_transactions)

    print('Mineração completa!')

    return jsonify(resp), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Checa se os dados estao presentes na requisição POST
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required) or values['sender'] == ''\
            or values['recipient'] == '' or values['amount'] == '':
        return 'Faltam valores', 400

    # Verifica se o pagador de fato possui saldo
    # para realizar a transação
    saldo = Carteira.saldo(values['sender'], blockchain)
    print("\nSaldo de " + str(values['sender']) + " = " + str(saldo))

    if saldo < float(values['amount']):
        return 'Saldo insuficiente', 400

    # Cria uma nova transação
    index = blockchain.new_transaction(
        values['sender'], values['recipient'], values['amount'])

    response = {'message': f'A transacao sera adicionada ao bloco {index}'}
    return jsonify(response), 201


@app.route('/transaction')
def transacao():
    return render_template('carteira.html')

# Metódo incompleto


@app.route('/carteira/saldo', methods=['GET', 'POST'])
def get_saldo():
    values = request.get_json()
    saldo = Carteira.saldo(values['sender'], blockchain)
    response = {
        'saldo': blockchain.chain
    }

    # return jsonify()

@app.route('/chain', methods=['GET'])
def full_chain():
    # metódo retorna uma cadeia inteira de blocos em formato json
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    # Recebe  uma lista de novos nós conhecidos
    values = request.get_json()
    values = json.loads(values)
    nodes = values['nodes']

    if nodes is None:
        return "Erro: Por favor, entre com um lista valida de nos", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'Novos nos foram adicionados',
        'total_nodes': list(blockchain.nodes)
    }
    return jsonify(response), 201

@app.route('/nodes', methods=['GET'])
def get_all_nodes():

    response = {
        'nodes': list(blockchain.nodes)
    }

    return jsonify(response),200

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    # Verifica se é necessário substituir a cadeia atual
    replaced = blockchain.resolve_conflicts()

    print("Iniciando algoritimo de consenso...")

    if replaced:
        response = {
            'message': 'Nossa blockchain foi substituida',
            'new_chain': blockchain.chain
        }
        print("Nossa cadeia foi substituida")
    else:
        response = {
            'message': 'Nossa blockchain é autoritativa',
            'chain': blockchain.chain
        }
        print("Nossa cadeia é autoritativa")

    return jsonify(response), 200


if __name__ == '__main__':

    app.run('0.0.0.0', port=5000)
