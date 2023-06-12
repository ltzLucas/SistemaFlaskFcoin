from datetime import datetime
from time import sleep


# def pegarhora():
    # dados = transacoes.hora()


    # data = agora.date()
    # hora = agora.time()
    #
    # print("Data:", data)
    # print("Hora:", hora)
# pegarhora()


    #
    # data = datetime.strptime(hora,"%a, %d %b %Y %H:%M:%S %Z")
    #
    #
    # print(data)
    # dia = data.day
    # mes = data.month
    # ano = data.year
    # hora = data.hour
    # minutos = data.minute
    # segundos = data.second
    #
    # print("Dia:", dia)
    # print("Mês:", mes)
    # print("Ano:", ano)
    # print("Hora:", hora)
    # print("Minutos:", minutos)
    # print("Segundos:", segundos)
    #
    # data_atual = datetime.now()
    #
    # if data <= data_atual:
    #     print('Data é menor')
    # else:
    #     print('Data nao é menor')

# def percentual():
#     Validadores = Validador.query.all()
#
#     for x in Validadores:
#         print(x)


import random

# validadores = ["A", "B", "C"]
#
# percentual_A = 5
# percentual_B = 40
# percentual_C = 30
#
# peso_A = percentual_A
# peso_B = percentual_B
# peso_C = percentual_C
#
# total_pesos = peso_A + peso_B + peso_C
# probabilidade_A = peso_A / total_pesos
# probabilidade_B = peso_B / total_pesos
# probabilidade_C = peso_C / total_pesos
#
# numero_aleatorio = random.random()
#
#
# escolha1 = None
# escolha2 = None
#
# if numero_aleatorio < probabilidade_A:
#     escolha1 = "A"
# elif numero_aleatorio < probabilidade_A + probabilidade_B:
#     escolha1 = "B"
# else:
#     escolha1 = "C"
#
# # Remova o validador escolhido para a segunda escolha
# if escolha1 == "A":
#     probabilidade_B /= (1 - probabilidade_A)
#     probabilidade_C /= (1 - probabilidade_A)
# elif escolha1 == "B":
#     probabilidade_A /= (1 - probabilidade_B)
#     probabilidade_C /= (1 - probabilidade_B)
# else:
#     probabilidade_A /= (1 - probabilidade_C)
#     probabilidade_B /= (1 - probabilidade_C)
#
# # Gere um novo número aleatório para a segunda escolha
# numero_aleatorio2 = random.random()
#
# if numero_aleatorio2 < probabilidade_A:
#     escolha2 = "A"
# elif numero_aleatorio2 < probabilidade_A + probabilidade_B:
#     escolha2 = "B"
# else:
#     escolha2 = "C"
#
#
# print(escolha1)
#
# print(escolha2)
#


# import random
#
# validadores = ["A", "B", "C","D","E"]
# percentual_A = 5
# percentual_B = 40
# percentual_C = 30
# percentual_D = 35
# percentual_E = 20
# pesos = [percentual_A, percentual_B, percentual_C,percentual_D,percentual_E]
#
# escolha1 = random.choices(validadores, pesos)[0]
#
# validadores.remove(escolha1)
#
# escolha2 = random.choice(validadores)
#
# print(escolha1)
# print(escolha2)



# from collections import Counter
#
# json_data = [{'id': 2, 'status': 1}, {'id': 3, 'status': 0}, {'id': 4, 'status': 1},{'id': 1, 'status': 0},{'id': 5, 'status': 0}]
#
# status_counts = Counter(item['status'] for item in json_data)
#
# most_common_status = status_counts.most_common(1)[0][0]
#
# print(f"O valor de status que mais aparece é: {most_common_status}")
#
# ids_with_different_status = [item['id'] for item in json_data if item['status'] != most_common_status]
#
# print(f"IDs com valores de status diferentes da maioria: {ids_with_different_status}")

