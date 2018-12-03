import requests
import json



if __name__ == 'main':

    # Manualmente deve ser inserida na lista todos os outros nós que compõem a rede,
    # na qual sera enviada a API para o registro completo da rede de um determinado nó
    known_nodes = ['http://teste.com.br']

    nodes = {'nodes': known_nodes}

    # É utilziada a api em endereço local em sua devida porta
    requests.post('http://localhost:5000', json=json.dumps(nodes))
