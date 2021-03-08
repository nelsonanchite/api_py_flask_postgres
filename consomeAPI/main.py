import os
import requests
import json

def consomeApi():
    for arquivo in os.listdir("jsons"):
        with open('jsons/{0}'.format(arquivo), 'r') as arq_json:
            arq = json.loads(arq_json.read())
            headers = {'Content-Type': 'application/json'}
            response = requests.post('http://127.0.0.1:5000/api/pedidoExame', data=json.dumps(arq), headers=headers)
            if response.status_code == 200:
                resposta = json.loads(response.content)
                if resposta['codigo'] == 0:
                    print(resposta['mensagem'])
                else:
                    print("Erro: " + resposta['mensagem'])
            else:
                print('Ocorreu um erro na requisição')

if __name__ == '__main__':
    consomeApi()
