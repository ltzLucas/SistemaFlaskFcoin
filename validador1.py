class Validador():
    count = 0
    def __init__(self):
        
        self.id = Validador.gerar_id()
        status:int
        valor:float

    @classmethod
    def gerar_id(cls):
        cls.count += 1
        return cls.count
    
    def validar(self,saldo,valor):
        if(saldo < valor):
            return 0
        else:
            return 1

validador1= Validador()
validador2 = Validador()


import requests

# Endpoint e dados para a solicitação '/select/<string:nome>'
select_url = 'http://localhost:5000/transacoes/1/2/100'

# Endpoint e dados para a solicitação '/validate'
validate_url = 'http://localhost:5000/validate'
validate_data = {'valor': 42}

# Envia a solicitação para '/validate/'
select_response = requests.post(select_url)
select_result = select_response.json()


x = select_result[0]
y = select_result[1]
valor = select_result[2]

result = validador1.validar(valor,50)

print(f"O validador {validador1.id} deu a resposta como: {result}")

# Envia a solicitação para '/validate'
validate_response = requests.post(validate_url, json=validate_data)
validate_result = validate_response.json()
print("Resposta de '/validate':", validate_result)



print(validador1.id)
print(validador2.id)

