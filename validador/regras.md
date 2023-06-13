• O remetente deve ter um valor em saldo maior que o valor da transação para a mesma ser válida;

• O horário da transação deve ser menor ou igual ao horário atual do sistema e deve ser maior que o horário da última transação para ser válida;

• Caso o remetente tenha feito mais que 1000 transações no último segundo, as transações no próximo minuto devem ser invalidas;
    ▪ Opcional: Aumentar o tempo de recusa, caso o problema persista;

• Na hora do cadastro o validador recebe uma chave única do seletor. Em toda transação, o validador deve retornar a chave única que recebeu no cadastro. Caso as chaves sejam iguais, a transação é concluída, caso contrário, a transação não é concluída;

• Status da Transação (Servem da camada “Validador” para a camada “Seletor”, assim como da camada “Seletor” para a camada “Banco”):
    • 1 = Concluída com Sucessoo 
    • 2 = Não aprovada (erro)
    • 0 = Não executada
        ▪ Códigos opcionais podem existir, mas devem ser descritos para implementação na camada “Banco”