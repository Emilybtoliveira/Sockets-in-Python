import socket
from threading import Thread
import sys,os

#MULTI-THREAD
def initServer(clientes):
    host = "localhost"
    port = 5000 #arbitrary non-privileged port
    
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    print("Socket pronto.")
    
    tcp.bind((host, port))    
    tcp.listen()
    print("Socket está à escuta na porta 5000...")
    print("Digite 'quit' para finalizar a execução do servidor a qualquer momento.\n")
    Thread(target=serverThread, args=()).start() 

    #infinite loop - do not reset for every requests
    while True:
        con, cliente = tcp.accept()
        #print("con:",con)
        ip, port = str(cliente[0]), str(cliente[1])
        print ("O cliente {} se conectou ao servidor.".format(port))
        clientes.append(con)
        Thread(target=clientThread, args=(con,port)).start()   
    tcp.close()  


def serverThread():
    while True:
        awaits = input()
        if awaits == 'quit':
            print("Finalizando execução do servidor...")
            os._exit(0) #ver se funciona no windows
            #ou sys.exit()      


def clientThread(con,port):
    while True:
        msg = con.recv(1024)
        
        if not msg: break
        msg = msg.decode("utf-8") 
        print("Cliente {} disse: {}".format(port, msg))
        
        reply_msg = "Recebi tua mensagem '" + msg +"'"
        con.send(bytes(reply_msg, 'iso_8859_1'))
        #print (msg)    
        
    print("Cliente", port,"solicitou o fechamento da conexão...")
    con.close()
    print ("Cliente {} deixou o servidor.".format(port))
       

clientes = []
initServer(clientes)



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
