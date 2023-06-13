import requests

def adicionar_Cliente(nome, senha,qtdMoedas):
    url = f'http://127.0.0.1:5000/cliente/{nome}/{senha}/{qtdMoedas}'  # URL do endpoint Flask
    response = requests.post(url)

    if response.status_code == 200:
        dados = response.json()
        # print('Mensagem enviada com sucesso!')
        # print('Resposta do servidor:')
        print(dados)
    else:
        print('Falha ao enviar a mensagem.')

def visualizar_Cliente():
    url = f'http://127.0.0.1:5000/cliente'
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        print('Mensagem enviada com sucesso!')
        print('Resposta do servidor:')
        print(dados)
    else:
        print('Falha ao enviar a mensagem.')

def visualizar_Cliente_id(id):
    url = f'http://127.0.0.1:5000/cliente/{id}'
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        return dados
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


adicionar_Cliente('teste Cliente', 'teste123',10000)
# visualizar_Cliente()
# visualizar_Cliente_id(2)
# deletar_cliente(2)

