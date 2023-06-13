import requests

def cadastrar_seletor(nome,ip):
    url = f'http://127.0.0.1:5000/seletor/{nome}/{ip}'  # URL do endpoint Flask
    response = requests.post(url)

    if response.status_code == 200:
        dados = response.json()
        print('Seletor cadastrado com sucesso!!')
        print('Resposta do servidor:')
        print(dados)
    else:
        print('Falha ao enviar a mensagem.')

def visualizar_seletor():
    url = f'http://127.0.0.1:5000/seletor'
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        print('Mensagem enviada com sucesso!')
        print('Resposta do servidor:')
        print(dados)
    else:
        print('Falha ao enviar a mensagem.')

def visualizar_seletor_id(id):
    url = f'http://127.0.0.1:5000/seletor/{id}'
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        print('Mensagem enviada com sucesso!')
        print('Resposta do servidor:')
        print(dados)
    else:
        print('Falha ao enviar a mensagem.')

def deletar_seletor(id):
    url = f'http://127.0.0.1:5000/cliente/{id}'
    response = requests.delete(url)

    if response.status_code == 200:
        dados = response.json()
        print('Mensagem enviada com sucesso!')
        print('Resposta do servidor:')
        print(dados)
    else:
        print('Falha ao enviar a mensagem.')

cadastrar_seletor('Seletor','192.168.1.2:5001')
# visualizar_seletor()
# visualizar_seletor_id(1)
# deletar_seletor(2)

