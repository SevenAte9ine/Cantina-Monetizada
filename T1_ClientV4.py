import socket

HOST = 'localhost'
PORT = 5600

# Inicializa a conexão do cliente
def main():
    # Cria o Socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Ordena o socket do cliente que se conecte a um determinado socket no servidor
        s.connect((HOST, PORT))
        # Autenticação
        matricula = int(input('Informe sua matrícula: '))
        senha = str(input('Insira sua senha: '))
        # Junta a matrícula e senha para criar uma identificação única.
        total = str(matricula) + senha

        # Envia os dados para o servidor
        s.sendto(total.encode('utf-8'), (HOST, PORT))

        while True:
            data = s.recv(1024)
            print('Received', repr(data))
            # Faz um loop de escolhas de produtos até 6 for inserido e envia os resultados ao Server junto a lista do cadastro.
            escolha = input("Escolha um produto: ")
            if escolha == "6":
                break
            s.sendto(escolha.encode('utf-8'), (HOST, PORT))

main()