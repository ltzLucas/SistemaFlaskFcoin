import requests


def cadastrar_validador(nome,ip):
    url = f'http://127.0.0.1:5001/validador/{nome}/{ip}'  # URL do endpoint Flask
    response = requests.post(url)

    if response.status_code == 200:
        dados = response.json()
        print('Validador cadastrado com sucesso!!')
    else:
        print('Falha ao enviar a mensagem.')


cadastrar_validador("Validador1","192.168.1.2:5002")

