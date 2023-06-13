import requests

def cadastrar_validador(nome,ip):
    url = f'http://127.0.0.1:5001/validador/{nome}/{ip}/1000'  # URL do endpoint Flask
    response = requests.post(url)

    if response.status_code == 200:
        print('Validador cadastrado com sucesso!!')
    else:
        print('Falha ao enviar a mensagem.')

def chama_validador():
    for x in range(2, 12):
        x_str = str(x).zfill(2)
        cadastrar_validador(f"Validador{x_str}",f"192.168.1.2:50{x_str}")
        
chama_validador()