import requests
import json



if __name__ == 'main':
    
    # Manualmente deve ser inserida na lista todos os outros nós que compõem a rede,
    # na qual sera enviada a API para o registro completo da rede de um determinado nó
    known_nodes = ['http://teste.com.br']

    nodes = {'nodes': known_nodes}

    # É utilizada a api em endereço local em sua devida porta
    req = requests.post('http://localhost:5000/nodes/register', json=json.dumps(nodes))

    if(req.status_code == 201):
        print("All known nodes has been registered!")
    else:
        print("there was a error with the request")

