import socket
from threading import Thread

#MULTI-THREAD
def initServer(clients):
    host = "localhost"
    port = 5000 #arbitrary non-privileged port
    
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Socket pronto.")
    
    tcp.bind((host, port))    
    tcp.listen()
    print("Socket está à escuta na porta 5000...\n")
    
    #infinite loop - do not reset for every requests
    while True:
        con, cliente = tcp.accept()
        ip, port = str(cliente[0]), str(cliente[1])
        print ("O cliente {} se conectou ao servidor.".format(port))
        clients.append(port)
        Thread(target=clientThread, args=(con, cliente, ip, port)).start()      
    tcp.close()

def clientThread(con, cliente, ip, port):
    while True:
        msg = con.recv(1024)
        if not msg: break
        msg = msg.decode("utf-8") 
        print("Cliente {} disse: {}".format(port, msg))
        #print (msg)    
        
    print("Cliente", port,"solicitou o fechamento da conexão...")
    con.close()
    print ("Cliente {} deixou o servidor.".format(port))
       

clients = []
initServer()



""" #SINGLE-THREAD

host = "localhost"
port = 5000 #arbitrary non-privileged port

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Socket pronto")

tcp.bind((host, port))    
tcp.listen()
print("Socket está à escuta na porta 5000...\n")

while True:
    con, cliente = tcp.accept()
    print ('Conectado por', cliente)

    while True:
        msg = con.recv(1024)
        if not msg: break
        msg = msg.decode("utf-8") 
        print (cliente, msg)

    print ('Finalizando conexao do cliente', cliente)
    con.close()  """
