import socket
from threading import Thread
import sys,os

def sendForAll(msg, clientesOnline, clientes, sender):   
    online = list(clientesOnline.keys()) 
    #print(online)
    for key in online:
        if key != sender:
            #print(key)
            replyMsg(msg, clientes[key])

def isUsuarioCadastrado(nome):
    nomeArquivo = "usuarios.txt"
    file = open(nomeArquivo)
    boolean = nome in file.read()
    file.close()
    return boolean # nao fiz aqui um return direto para poder fechar o arquivo
    

def cadastrarUsuario(nome):
    nomeArquivo = "usuarios.txt"
    file = open(nomeArquivo,"a") # vai abrir com append, ou seja, adicionar
    file.write(nome+"\n") # escreve o nome e da quebra de linha
    file.close()
    return True

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
    return con.send(bytes(msg, 'utf-8'))

def clientThread(con,port, clientes):
    clienteIn = False
    inChat = False
    usuarioNome = ""
    
    while True:
        msg = con.recv(1024)        
        msg = msg.decode("utf-8")
        #print(msg)
        if msg == 'sair' or not msg: break
        
        if(clienteIn==False):          

            if msg == "cadastrar":
                msg = con.recv(1024) #aqui o servidor espera o cliente enviar o nickname do usuario
                msg = msg.decode("utf-8")
                #print(msg)

                if(isUsuarioCadastrado(msg)):
                    replyMsg("Servidor disse: Voce entrou no servidor, bem vindo!",con)
                    print("Cliente %s entrou no servidor" % msg)                    
                else:
                    cadastrarUsuario(msg)                
                    replyMsg("Servidor disse: Cadastrado!",con)
                    print("Cliente %s foi cadastrado" % msg)                    

                clienteIn = True
                usuarioNome = msg
            
                clientesOnline[msg] = port
                clientes[usuarioNome] = con #dicionario que mapeia socket - nome

                msgEnviar = usuarioNome + " se juntou ao servidor!"   
                sendForAll(msgEnviar, clientesOnline, clientes, usuarioNome) 
                
        else:
            if(inChat):
                if(msg=='quit'):
                    inChat=False
                    replyMsg("Servidor disse: Voce saiu do chat",con)
                else:
                # enviar msg aqui para a porta do receptor
                    msgEnviar = usuarioNome+" disse: "+msg
                    sendForAll(msgEnviar, clientesOnline, clientes, usuarioNome)
                    print("Broadcasting mensagem de {}: {}".format(usuarioNome, msg))
            else:
                if(msg=="conversar"):
                    replyMsg(list(clientesOnline.keys()),con)
                    print(clientesOnline)

                if(msg == "chat"):
                    inChat = True
                    #replyMsg("Servidor disse: você está na conversa.",con)
                    #print("O cliente {} entrou na conversa".format(usuarioNome))
                    
            """ indice = (list(clientesOnline.values())).index(port)
            nomeCliente = list(clientesOnline.keys())[indice] """            


        #print(clientes)      

        # reply_msg = "Recebi tua mensagem '" + msg +"'"
        # con.send(bytes(reply_msg, 'iso_8859_1'))
    
         
    print("Cliente", usuarioNome,"solicitou o fechamento da conexão...")
    con.close()
    print ("Cliente {} deixou o servidor.".format(port))
    del clientesOnline[usuarioNome]

    msgEnviar = usuarioNome + " deixou o servidor."   
    sendForAll(msgEnviar, clientesOnline, clientes, usuarioNome)
       
def getclientes():
    return clientes



clientes = {}
clientesOnline = {}

initServer(clientes)