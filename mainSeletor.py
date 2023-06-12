from random import random
from time import time
from flask import Flask, request, redirect, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dataclasses import dataclass
from datetime import date, datetime
import requests
import cliente
import random
import time

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testeSeletor12.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@dataclass
class Validador(db.Model):
    id: int
    nome: str
    ip: int
    flag: int
    FCoins: int
    percent: int

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(20), unique=False, nullable=False)
    ip = db.Column(db.String(50), unique=False, nullable=False)
    flag = db.Column(db.Integer, unique=False, nullable=False)
    FCoins = db.Column(db.Integer, unique=False, nullable=False)
    percent = db.Column(db.Integer, unique=False, nullable=False)

@app.route("/")
def index():
    return render_template('api.html')

@app.route('/validador', methods=['GET'])
def ListarCliente():
    if (request.method == 'GET'):
        clientes = Validador.query.all()
        return jsonify(clientes)

@app.route('/validador/<string:nome>/<string:ip>/<int:FCoins>', methods=['POST'])
def Cadastro_dos_Validadores(nome, ip,FCoins):
    if request.method == 'POST' and nome != '' and ip != '':
        objeto = Validador(nome=nome, ip=ip,flag=0,FCoins=FCoins,percent=0)
        db.session.add(objeto)
        db.session.commit()

        calcular_percent()
        return jsonify(objeto)
    else:
        return jsonify(['Method Not Allowed'])

def calcular_percent():
    validadores = Validador.query.all()

    totalFCoins = 0
    for v in validadores:
        totalFCoins = totalFCoins + v.FCoins

    for v in validadores:
        percentual = int((v.FCoins / totalFCoins) * 100)
        if percentual < 5:
            percent = 5
        elif percentual > 40:
            percent = 40
        else:
            percent = percentual

        validadorObjeto = Validador.query.filter_by(id=v.id).first()
        db.session.commit()
        validadorObjeto.percent = percent
        db.session.commit()
        # print(f'Validador {v.id} está com o percentual de {percent}')


@app.route('/validador/<int:id>', methods=['GET'])
def UmSeletor(id):
    if (request.method == 'GET'):
        produto = Validador.query.get(id)
        return jsonify(produto)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/validador/<int:id>', methods=['DELETE'])
def ApagarValidador(id):
    if (request.method == 'DELETE'):
        objeto = Validador.query.get(id)
        db.session.delete(objeto)
        db.session.commit()

        data = {
            "message": "Validador Deletado com Sucesso"
        }
        return jsonify(data)
    else:
        return jsonify(['Method Not Allowed'])

@app.route('/transacao/<int:id>/<int:remetente>/<int:recebedor>/<int:valor>/<int:status>', methods=['POST'])
def receberTransacao(id,remetente,recebedor,valor,status):
    if request.method == 'POST':
        Validadores = Validador.query.all()
        rem = cliente.visualizar_Cliente_id(remetente)

        escolhe_validadores()

        saldoRem = rem['qtdMoeda']
        for v in Validadores:
            url = f'http://{v.ip}/validar/{saldoRem}/{valor}'
            response = requests.post(url)

        print(response.text)

        return 'retorno mainSeletor transacao'
    else:
        return jsonify(['Method Not Allowed'])

    return 'ola'

def escolhe_validadores():
    Validadores = Validador.query.all()

    if len(Validadores) < 3:
        print('Transação em espera aguarde 1 min')
        time.sleep(60)
        Validadores = Validador.query.all()
        if len(Validadores) < 3:
            print('Não foi possivel concluir a transação por falta de validadores')
            #COLOCAR UM RETURN PARA MOSTRAR Q FALHOU A OPERAÇÃO
    if len(Validadores) >= 5:
        validadoresID = []
        pesos = []
        for v in Validadores:
            validadoresID.append(v.id)
            pesos.append(v.percent)

        v1 = random.choices(validadoresID, pesos)[0]
        #limpa as listas
        validadoresID.clear()
        pesos.clear()

        for v in Validadores:
            if v.id != v1:
                validadoresID.append(v.id)
                pesos.append(v.percent)

        v2 = random.choices(validadoresID, pesos)[0]
        # limpa as listas
        validadoresID.clear()
        pesos.clear()
        for v in Validadores:
            if v.id != v1 and  v.id != v2:
                validadoresID.append(v.id)
                pesos.append(v.percent)

        v3 = random.choices(validadoresID, pesos)[0]
        # limpa as listas
        validadoresID.clear()
        pesos.clear()
        for v in Validadores:
            if v.id != v1 and  v.id != v2 and v.id != v3:
                validadoresID.append(v.id)
                pesos.append(v.percent)

        v4 = random.choices(validadoresID, pesos)[0]
        # limpa as listas
        validadoresID.clear()
        pesos.clear()
        for v in Validadores:
            if v.id != v1 and  v.id != v2 and v.id != v3 and v.id != v4:
                validadoresID.append(v.id)
                pesos.append(v.percent)

        v5 = random.choices(validadoresID, pesos)[0]

        print(v1,v2,v3,v4,v5)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

app.run(host='0.0.0.0',port=5001, debug=True)