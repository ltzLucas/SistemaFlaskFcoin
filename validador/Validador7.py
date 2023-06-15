
from flask import Flask, request, redirect, render_template, jsonify, Response
from datetime import date, datetime
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('api.html')

@app.route('/validar/<int:id>/<int:valorRem>/<int:valorTrans>/<string:horario>', methods=['POST'])
def receberTransacao(id,valorRem, valorTrans,horario):
    if request.method != 'POST' and id == '' and valorRem == '' and valorTrans == '' and horario == '':
        return jsonify(['Method Not Allowed'])
    
    agora = datetime.now()

    horario = datetime.strptime(horario, '%Y-%m-%d %H:%M:%S.%f')

    if valorRem >= valorTrans and horario <= agora:
        response_data = {'id': id, 'status': 1 }  #PODE
    else:
        response_data = {'id': id, 'status': 2}  #NÃO PODE

    return jsonify(response_data)

def hora_sistema():
    url = f'http://127.0.0.1:5000/hora'
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        print('Hora recebida com sucesso!')
        return dados
    else:
        print('Falha ao enviar a mensagem.')
        
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5007, debug=True)