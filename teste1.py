from flask import Flask, request, jsonify

app = Flask(__name__)


# Função para seleção
def select_validators(data):
    validators = ['Validator 1', 'Validator 2', 'Validator 3', data]
    return validators


# Função para validação
def validate_data(data):
    # Implemente a lógica de validação aqui
    # Retorna o resultado da validação
    result = 'Data is valid'
    return result


@app.route('/')
def index():
    return "Seletor e Validador"


@app.route('/transacoes/<int:rem>/<int:reb>/<int:valor>', methods=['GET'])
def select(rem, reb, valor):
    return jsonify(rem, reb, valor)


@app.route('/validate', methods=['POST'])
def validate():
    data = request.json  # Obtém os dados enviados no corpo da requisição
    result = validate_data(data)
    return jsonify(result)


if __name__ == '__main__':
    app.run()
