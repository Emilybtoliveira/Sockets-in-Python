import socket

HOST = 'localhost'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
tcp.connect(dest)
print ('Para sair pressione Enter')

msg = ''

while (msg != b''):       
    msg = bytes(input(), 'iso_8859_1')
    print(msg)
    tcp.sendall(msg)    

print("Fechando conexão...")
tcp.close()