from threading import Thread
import socket
import random

HOST = 'localhost'
PORT = 5600

# Deixa uma lista de registros aberta para identificação.
listaRegistros = []
# Lista com valores dos produtos   
valores = [10.50, 5.00, 7.50, 4.50, 8.00, 20.00]
# Variável global que atualiza o saldo do cliente
saldo_cliente = []


# Inicializa o servidor
def main():
    try:
        # Cria o Socket TCP
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
             # Realiza a associação entre a estrutura socket e o endereço/porta do servidor
            s.bind((HOST, PORT))
            # Coloca o socket em operação
            s.listen(5)
            while True:
                 # Aceita conexões de clientes, retornando uma tupla da conexão realizada.
                conn, addr = s.accept()
                threadEnviaMsg = Thread(target=trata_echo, args=[listaRegistros, conn, addr, len(saldo_cliente)])
                threadEnviaMsg.start()
    except:
        print("Erro em main!")


# Inicializa o saldo do cliente
def verificaSaldo():
    while True:
        saldo = random.uniform(50.00, 100.00)
        total = saldo - random.uniform(5.0, 15.00)
        total = round(total, 2)
        #print(total) 
        return total


# Mostra menu
def showMenu(indice):
    try:
        comprovante_saldo = "Seu saldo: " + str(saldo_cliente[indice])
        menu = comprovante_saldo + " Menu: 0. Hamburguer (10.50) - 1. Fritas (5.00) - 2. Pastel (7.50) - 3. Coca-Cola (4.50) - 4. Chocolate (8.00) - 5. Combo: Hamburguer + Fritas + Coca-Cola (20.00) - 6. Sair"
        return menu
    except:
        print("Erro em showMenu!")


# Efetua o cálculo do produto e atualiza a variável global saldo_cliente
def descontaSaldo(indice, op):
    try: 
        global saldo_cliente
        opcao = int(op)
        total = 0

        saldo = saldo_cliente[indice]
        produto = valores[opcao]
        total = saldo - produto

        if int(saldo_cliente[indice]) > int(total) and total >= 0:
            saldo_cliente[indice] = round(total,2)
        else:
            saldo_cliente[indice] = "Saldo insuficiente!"
    except:
        print("Erro em descontaSaldo!")


# Trata a mensagem enviada ao cliente
def trata_echo(listaRegistros, conn, addr, indice):
    print('Connected by', addr)
    while True:
        try:
            # Recebe os dados
            # 1024 - A quantidade máxima de dados a serem recebidos de uma só vez
            data = conn.recv(1024)        
            if not data: break

            listaRegistros.append(data)

            # Verifica se o dado recebido é um item do menu e não a matrícula do cliente
            if len(data.decode('utf-8')) == 1:
                #Efetua a compra se houver créditos disponíveis
                descontaSaldo(indice, data.decode('utf-8'))

            # Se o dado recebido é uma nova matrícula, gera um novo saldo
            if len(data.decode('utf-8')) > 1:
                saldo_cliente.append(verificaSaldo())

            menu = showMenu(indice)
            conn.sendall(menu.encode('utf-8'))
        except:
            print("Erro em trata_echo!")

main()