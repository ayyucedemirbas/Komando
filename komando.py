# coding: cp1254

import socket,sys,os,threading
from core.colorama import Fore,Style,Back,init
init(autoreset = True)

try:
    import dbm
except:
    import anydbm as dbm
    
class Komando: # :)
    def __init__(self,host = "localhost",port = 8088,mode = "server"):
        self.mode = mode
        self.host = host
        self.port = port
        self.machine = False
        self.configureDB()



    def start(self):
        if(self.mode == "server"):
            self.startServer()
        elif(self.mode == "client"):
            self.startClient()


    def configureDB(self): # veritabanı ayarlama
        print(Fore.YELLOW+"[~] "+Style.RESET_ALL+"Configuring db")
        self.vt = dbm.open("vt"+os.sep+"komut.db","c")

    def addDB(self,**command):
        self.vt[command["cmd"]] = command["value"]
        
    
    def startServer(self):
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((self.host,self.port))
        self.server.listen(1)
        
        print(Fore.GREEN+Style.BRIGHT+"[+] "+Style.RESET_ALL+"Server started on {} port {}".format(self.host,self.port))

        while True:
            self.machine,self.info = self.server.accept()
            break

        print(Fore.GREEN+Style.BRIGHT+"[!] "+Style.RESET_ALL+"Guest is connected: {0}:{1}".format(self.info[0],self.info[1]))

        self.n = threading.Thread(target = self.recvMSG,args = (),)
        self.n.start()

        self.msgConsole()

    def startClient(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print(Fore.YELLOW+"[~] "+Style.RESET_ALL+"Connecting...")
        self.client.connect((self.host,self.port))
        print(Fore.GREEN+Style.BRIGHT+"[!] "+Style.RESET_ALL+"Connection established")
        self.machine = self.client

        self.msgConsole()        
        

    def recvMSG(self): # Mesajları bekliyor
        while(True):
            mesaj = self.machine.recv(1024)
            if(mesaj == "q"):
                print(Fore.RED+Style.BRIGHT+"\n\t[-] "+Style.RESET_ALL+"client sent close message")
                self.vt.close()
                self.server.close()
                sys.exit(0)
                break
            else:
                print(Fore.GREEN+Style.BRIGHT+"\n\n\t[MSG] "+Style.RESET_ALL+"{}\n".format(mesaj))
                self.execute(mesaj)

    def msgConsole(self):
        if(self.mode == "client"):
            while(True):
                mesaj = raw_input(Fore.GREEN+"[~] "+Style.RESET_ALL+"your command: ")
                if(mesaj == "exit" or mesaj == "q"):
                    self.machine.send("q")
                    self.vt.close()
                    sys.exit(0)
                    break
                else:
                    print(Fore.GREEN+"[+] "+Style.RESET_ALL+"sent: {}".format(mesaj))
                    self.machine.send(mesaj)
        else:
            print(Fore.YELLOW+"\n[...] "+Style.RESET_ALL+"Listening messages...")

    def execute(self,command):
        if(len(command) > 0):
            print(Fore.GREEN+Style.BRIGHT+"\n\t[EXEC] "+Style.RESET_ALL+"{}".format(command))
            os.system(command)
        else:
            print(Fore.YELLOW+Style.BRIGHT+"\n\t[-] "+Style.RESET_ALL+"Command is not valid: {}".format(command))


    def close(self):
        if(self.mode == "server"):
            self.server.close()
        else:
            self.client.close()
            
        self.vt.close()
        sys.exit(0)

port = 8090

if(sys.argv[1] in ["-c","--client"]):
    Komando(mode = "client",port = port).start()
elif(sys.argv[1] in ["-s","--server"]):
    Komando(port = port).start()

liste = {"$cmd":"start",
         "$shell":"$TERM",
         "$clear":"cls"}


    
