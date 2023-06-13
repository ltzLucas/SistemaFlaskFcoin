import requests

def cadastrar_transacao(rem, reb,valor):
    url = f'http://127.0.0.1:5000/transacoes/{rem}/{reb}/{valor}'  # URL do endpoint Flask
    response = requests.post(url)

    if response.status_code == 200:
        # dados = response.json()
        print('Mensagem enviada com sucesso!')
        print('Resposta do servidor:')
        # print(dados)
    else:
        print('Falha ao enviar a mensagem.')


def visualizar_transacoes():
    url = f'http://127.0.0.1:5000/transacoes'
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        print('Mensagem enviada com sucesso!')
        print('Resposta do servidor:')
        print(dados)
    else:
        print('Falha ao enviar a mensagem.')

def visualizar_transacoes_id(id):
    url = f'http://127.0.0.1:5000/transacoes/{id}'
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        print('Mensagem enviada com sucesso!')
        print('Resposta do servidor:')
        print(dados)
    else:
        print('Falha ao enviar a mensagem.')



def deletar_cliente(id):
    url = f'http://127.0.0.1:5000/cliente/{id}'
    response = requests.delete(url)

    if response.status_code == 200:
        dados = response.json()
        print('Mensagem enviada com sucesso!')
        print('Resposta do servidor:')
        print(dados)
    else:
        print('Falha ao enviar a mensagem.')


# cadastrar_transacao(1,2,100)
#
# visualizar_transacoes()

