import json
from collections import Counter
from time import time

import requests
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
from datetime import date, datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@dataclass
class Cliente(db.Model):
    id: int
    nome: str
    senha: int
    qtdMoeda: int

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    senha = db.Column(db.String(20), unique=False, nullable=False)
    qtdMoeda = db.Column(db.Integer, unique=False, nullable=False)

@dataclass
class Seletor(db.Model):
    id: int
    nomeSeletor: str
    ipSeletor: str

    id = db.Column(db.Integer, primary_key=True)
    nomeSeletor = db.Column(db.String(20), unique=False, nullable=False)
    ipSeletor = db.Column(db.String(150), unique=False, nullable=False)

@dataclass
class Transacao(db.Model):
    id: int
    remetente: int
    recebedor: int
    valor: int
    status: int
    horario: db.DateTime


    id = db.Column(db.Integer, primary_key=True)
    remetente = db.Column(db.Integer, unique=False, nullable=False)
    recebedor = db.Column(db.Integer, unique=False, nullable=False)
    valor = db.Column(db.Integer, unique=False, nullable=False)
    horario = db.Column(db.DateTime, unique=False, nullable=False)
    status = db.Column(db.Integer, unique=False, nullable=False)


    def to_dict(self):
        return {
            'id': self.id,
            'remetente': self.remetente,
            'recebedor': self.recebedor,
            'valor': self.valor,
            'status': self.status
        }


# @app.before_first_request
# def create_tables():
#    db.create_all()

@app.route("/")
def index():
    return render_template('api.html')


@app.route('/cliente', methods=['GET'])
def ListarCliente():
    if (request.method == 'GET'):
        clientes = Cliente.query.all()
        return jsonify(clientes)


@app.route('/cliente/<string:nome>/<string:senha>/<int:qtdMoedas>', methods=['POST'])
def InserirCliente(nome, senha, qtdMoedas):
    if request.method == 'POST' and nome != '' and senha != '' and qtdMoedas != '':
        objeto = Cliente(nome=nome, senha=senha, qtdMoeda=qtdMoedas)
        db.session.add(objeto)
        db.session.commit()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/cliente/<int:id>', methods=['GET'])
def UmCliente(id):
    if (request.method == 'GET'):
        # objeto = Cliente.query.get(id)
        objeto = db.session.get(Cliente, id)

        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/cliente/<int:id>/<int:qtdMoedas>', methods=['POST'])
def EditarCliente(id, qtdMoedas):
    if request.method == 'POST':
        try:
            varId = id
            varqtdMoedas = qtdMoedas
            cliente = Cliente.query.filter_by(id=id).first()
            db.session.commit()
            cliente.qtdMoedas = qtdMoedas
            db.session.commit()
            return jsonify(cliente)
        except Exception as e:
            data = {
                "message": "Atualização não realizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/cliente/<int:id>', methods=['DELETE'])
def ApagarCliente(id):
    if (request.method == 'DELETE'):
        objeto = Cliente.query.get(id)
        db.session.delete(objeto)
        db.session.commit()

        data = {
            "message": "Cliente Deletado com Sucesso"
        }

        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/seletor', methods=['GET'])
def ListarSeletor():
    if (request.method == 'GET'):
        produtos = Seletor.query.all()
        return jsonify(produtos)


@app.route('/seletor/<string:nome>/<string:ip>', methods=['POST'])
def InserirSeletor(nome, ip):
    if request.method == 'POST' and nome != '' and ip != '':
        objeto = Seletor(nomeSeletor=nome, ipSeletor=ip)
        db.session.add(objeto)
        db.session.commit()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/seletor/<int:id>', methods=['GET'])
def UmSeletor(id):
    if (request.method == 'GET'):
        produto = Seletor.query.get(id)
        return jsonify(produto)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/seletor/<int:id>/<string:nome>/<string:ip>', methods=['POST'])
def EditarSeletor(id, nome, ip):
    if request.method == 'POST':
        try:
            varNome = nome
            varIp = ip
            validador = Seletor.query.filter_by(id=id).first()
            db.session.commit()
            validador.nome = varNome
            validador.ip = varIp
            db.session.commit()
            return jsonify(validador)
        except Exception as e:
            data = {
                "message": "Atualização não realizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/seletor/<int:id>', methods=['DELETE'])
def ApagarSeletor(id):
    if (request.method == 'DELETE'):
        objeto = Seletor.query.get(id)
        db.session.delete(objeto)
        db.session.commit()

        data = {
            "message": "Seletor Deletado com Sucesso"
        }

        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])


@app.route('/hora', methods=['GET'])
def horario():
    if (request.method == 'GET'):
        objeto = datetime.now()
        return jsonify(objeto)


@app.route('/transacoes', methods=['GET'])
def ListarTransacoes():
    if (request.method == 'GET'):
        transacoes = Transacao.query.all()
        return jsonify(transacoes)


# @app.route('/transacoes/<int:rem>/<int:reb>/<int:valor>', methods=['POST'])
# def CriaTransacao(rem, reb, valor):
#     if request.method == 'POST':
#         objeto = Transacao(remetente=rem, recebedor=reb, valor=valor, status=0, horario=datetime.now())
#         db.session.add(objeto)
#         db.session.commit()
#
#         seletores = Seletor.query.all()
#         for i in seletores:
#             url = f'http://'+i.ipSeletor+'/transacao/'
#             print(url)
#             # url = 'http://127.0.0.1:5001/transacao/1'
#             # requests.post(url,data=jsonify(object))
#             data = json.dumps(objeto.to_dict())
#             requests.post(url,data=data)
#             print(objeto)
#         return jsonify(objeto)
#     else:
#         return jsonify(['Method Not Allowed'])

#----------------------------------------------------------MUDEI GRANDE PARTE DO Código------------------------------------------------------------------------------------
@app.route('/transacoes/<int:rem>/<int:reb>/<int:valor>', methods=['POST'])
def CriaTransacao(rem, reb, valor):
    if request.method == 'POST':
        objeto = Transacao(remetente=rem, recebedor=reb, valor=valor, status=0, horario=datetime.now())
        db.session.add(objeto)
        db.session.commit()

        print(objeto.horario)

        seletores = Seletor.query.all()
        resultado_json = []
        for i in seletores:
            url = f'http://{i.ipSeletor}/transacao/{objeto.id}/{objeto.remetente}/{i.id}/{objeto.valor}/{objeto.horario}'
            response = requests.post(url)
            resultado_json.append(response.json())
        # Contar a ocorrência de cada valor de status
        contagem_status = Counter(objeto["status"] for objeto in resultado_json)

        # Identificar o valor com maior contagem
        valor_mais_frequente = contagem_status.most_common(1)[0][0]

        print(valor_mais_frequente)

        editaTransacao(objeto.id,valor_mais_frequente)

        for obj in resultado_json:
            editaTransacaoSeletor(obj['id_transacao'],obj['status'])

        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/transactions/<int:id>/<int:status>', methods=['POST'])
def EditaTransacao(id, status):
    if request.method == 'POST':
        try:
            objeto = Transacao.query.filter_by(id=id).first()
            db.session.commit()
            objeto.id = id
            objeto.status = status
            db.session.commit()
            return jsonify(objeto)
        except Exception as e:
            data = {
                "message": "transação não atualizada"
            }
            return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])
def editaTransacao(id,status):
    url = f'http://127.0.0.1:5000/transactions/{id}/{status}'  # URL do endpoint Flask
    response = requests.post(url)

    if response.status_code == 200:
        dados = response.json()
        print('Resposta do servidor:')
        print(dados)
    else:
        print('Falha ao enviar a mensagem.')

def editaTransacaoSeletor(id,status):
    url = f'http://127.0.0.1:5001/trans/{id}/{status}'  # URL do endpoint Flask
    response = requests.post(url)

    if response.status_code == 200:
        dados = response.json()
        print('Resposta do servidor:')
        print(dados)
    else:
        print('Falha ao enviar a mensagem.')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

app.run(host='0.0.0.0', debug=True)