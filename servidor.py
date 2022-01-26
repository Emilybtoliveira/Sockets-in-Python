import socket
from threading import Thread
import sys,os

#MULTI-THREAD

listaUsuarios = ['felipe','emily']
clientes = {}
clientesOnline = {}

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
        #print(con.getpeername()) #pegar as informações do cliente        
        ip, port = str(cliente[0]), str(cliente[1])
        print ("O cliente {} se conectou ao servidor.".format(port))

        Thread(target=clientThread, args=(con,port, clientes)).start()   
    tcp.close()  


def serverThread():
    while True:
        awaits = input()
        if awaits == 'quit':
            print("Finalizando execução do servidor...")
            os._exit(0) #ver se funciona no windows
            #ou sys.exit()      


def replyMsg(msg,con):
    msg = str(msg)
    return con.send(bytes(msg, 'iso_8859_1'))

def clientThread(con,port, clientes):
    clienteIn = False
    inChat = False
    
    while True:
        msg = con.recv(1024)
        if msg == 'sair': break
        msg = msg.decode("utf-8") 
        if(clienteIn==False):
            if(msg in listaUsuarios):
                replyMsg("Voce entrou no servidor, bem vindo!",con)
                print("Cliente %s entrou no servidor" % msg)
                clienteIn = True
                
                clientesOnline[msg] = port
                
            else:
                replyMsg("Voce nao esta cadastrado!",con)
        else:
            if(inChat):
                # enviar msg aqui para a porta do receptor
                print("esta em chat")
                pass
            else:
                if(msg=="listar"):
                    replyMsg(list(clientesOnline.keys()),con)
                    print(clientesOnline)
                # elif(msg in clientesOnline and inChat==False):
                #     replyMsg("voces está num chat",con)
                #     portaConversa = clientesOnline[msg]
                #     inChat = True
            


            indice = (list(clientesOnline.values())).index(port)
            nomeCliente = list(clientesOnline.keys())[indice]
            print("Cliente {} disse: {}".format(nomeCliente, msg))


        clientes[con] = msg #dicionario que mapeia socket - nome
        #print(clientes)      

        # reply_msg = "Recebi tua mensagem '" + msg +"'"
        # con.send(bytes(reply_msg, 'iso_8859_1'))
           
        
    print("Cliente", port,"solicitou o fechamento da conexão...")
    con.close()
    print ("Cliente {} deixou o servidor.".format(port))
       


initServer(clientes)


