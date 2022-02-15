import socket
from threading import Thread
import tkinter as tk
import os

def closeConnection():
    print("Conexão fechada.\nExecução finalizada.")
    tcp.close()
    window.destroy()
    os._exit(0)

def sendMessage(msg):
    #print(msg)
    entryMsg.delete(0,'end')
    tcp.sendall(bytes(msg, 'utf-8'))
    print("Enviando a mensagem: {}".format(msg))
    
    if msg not in ['cadastrar', 'chat'] and msg != username.get():
        msg = "Você disse: " + msg
        textCons.config(state = 'normal') 
        textCons.insert('end', msg+"\n\n") 
        textCons.config(state = 'disabled') 
        textCons.see('end')     


def receiveMessages():
    while True:
        try:
            msg_servidor = tcp.recv(1024)
            if not msg_servidor: break
        except ConnectionAbortedError:
            break
        except ConnectionResetError:
            print("O servidor solicitou o fechamento da conexão.")
            break
       
        msgDecodificada = msg_servidor.decode("utf-8")
        print(msgDecodificada)

        textCons.config(state = 'normal') 
        textCons.insert('end', msgDecodificada+"\n\n") 
        textCons.config(state = 'disabled') 
        textCons.see('end')        
    tcp.close()
    
def chatting():
    frame2.destroy()
    sendMessage("chat")
    
    labelHead.place(relwidth = 1) 
    buttonQuit.place(relx = 0.70) 

    textCons.place(relheight = 0.745,relwidth = 1, rely = 0.08)    
   

    labelBottom.place(relwidth = 1, rely = 0.825) 
    
    entryMsg.place(relwidth = 0.74, relheight = 0.05, rely = 0.020, relx = 0.011)
    
    #entryMsg.focus()    

    buttonMsg.place(relx = 0.77, rely = 0.020, relheight = 0.05, relwidth = 0.22) 
  
    textCons.config(cursor = "arrow") 


    scrollbar.place(relheight = 1, relx = 0.974) 
    scrollbar.config(command = textCons.yview)     

    textCons.config(state = 'disabled')


def onlineClients(currentframe, username):
    currentframe.destroy()
        
    welcome = tk.Label(master = frame2 ,text="Hello, {}!".format(username))
    welcome.pack()  

    sair = tk.Button(master = frame2, text = 'Sair', command=closeConnection) 
    chat = tk.Button(master = frame2, text = 'Entrar no chat', command=chatting) 

    sair.pack()
    chat.pack()

def getUsername():
    if(username.get() == ""):
        error = tk.Label(master = frame1, text="Poxa, essa informação não pode ser vazia.")
        error.pack()
        return
    else:
        sendMessage("cadastrar")
        sendMessage(username.get())
        onlineClients(frame1, username.get())
        
    
#INIT SERVER
# mudar a porta, mudar o tcp para o novo socket que vem do servidor
HOST = 'localhost'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
dest = (HOST, PORT)
on = False

try:
    tcp.connect(dest)
    on = True    
    Thread(target=receiveMessages, args=()).start()
except ConnectionRefusedError:
    print("servidor off")

if(on):
    #GUI
    window = tk.Tk()
    window.geometry('500x550')

    frame1 = tk.Frame()
    frame2 = tk.Frame()
    frame3 = tk.Frame()

    username = tk.StringVar()
    message = tk.StringVar()

    type_name = tk.Label(master = frame1, text="Digite o nome do seu usuário:")
    entry = tk.Entry(master = frame1, textvariable=username)
    resultButton = tk.Button(master = frame1, text = 'Entrar', command=getUsername)

    labelHead = tk.Label(window, text = "Chat com todos",font = "Helvetica 13", pady = 12) 
    buttonQuit = tk.Button(labelHead, text="Sair do programa", font = "Helvetica 11", pady = 12, command=closeConnection)   
    textCons = tk.Text(window, width = 20, height = 2, font = "Helvetica 14", padx = 5, pady = 5) 
    labelBottom = tk.Label(window, height = 50) 
    entryMsg = tk.Entry(labelBottom, textvariable=message,  font = "Helvetica 13") 
    buttonMsg = tk.Button(labelBottom, text = "Enviar", font = "Helvetica 11", width = 20, command=lambda: sendMessage(message.get()))
    scrollbar = tk.Scrollbar(textCons) 


    type_name.pack()
    entry.pack()
    resultButton.pack()
    frame1.pack(anchor=tk.CENTER, expand=1)
    frame2.pack(anchor=tk.CENTER, expand=1)
    frame3.pack(anchor=tk.CENTER, expand=1)

    window.title("Discord da DeepWeb")
    window.mainloop()