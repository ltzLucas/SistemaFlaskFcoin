from time import time
from flask import Flask, request, redirect, render_template, jsonify, Response
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
from datetime import date, datetime
import requests
import cliente

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///validador.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route("/")
def index():
    return render_template('api.html')




def hora_sistema():
    url = f'http://127.0.0.1:5000/hora'
    response = requests.get(url)

    if response.status_code == 200:
        dados = response.json()
        print('Hora recebida com sucesso!')
        return dados
    else:
        print('Falha ao enviar a mensagem.')


@app.route('/validar/<int:id>/<int:valorRem>/<int:valorTrans>/<string:horario>', methods=['POST'])
def receberTransacao(id,valorRem, valorTrans,horario):
    agora = datetime.now()

    #HORARIO SISTEMA Prizyada
    # data = hora_sistema()
    # dt = datetime.strptime(data, "%a, %d %b %Y %H:%M:%S %Z")

    horario = datetime.strptime(horario, '%Y-%m-%d %H:%M:%S.%f')


    if valorRem >= valorTrans and horario <= agora:
        response_data = {'id': id, 'status': 1 }  #PODE
    else:
        response_data = {'id': id, 'status': 2}  #NÃO PODE

    return jsonify(response_data)








@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

app.run(host='0.0.0.0',port=5002, debug=True)