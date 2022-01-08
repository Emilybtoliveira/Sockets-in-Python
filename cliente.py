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
    tcp.sendall(msg) 
    
    msg_servidor = tcp.recv(1024)
    print("Servidor disse: ", msg_servidor.decode("utf-8"))
       

print("Fechando conexão...")
tcp.close()