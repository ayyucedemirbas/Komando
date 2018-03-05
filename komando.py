# coding: cp1254

import socket,sys,os,threading,subprocess
from core.colorama import Fore,Style,Back,init
init(autoreset = True)

try:
    import dbm
except:
    import anydbm as dbm
    
class Komando: # :)
    def __init__(self,host = "localhost",port = 8088,mode = "server"):
        self.badCommand = ["cmd",
                           "gnome-terminal",
                           "lxterminal",
                           "terminal",
                           "start",
                           "python",
                           "edit",
                           "netsh"]
        
        self.mode = mode
        self.host = host
        self.port = port
        self.machine = False



    def start(self):
        if(self.mode == "server"):
            self.startServer()
        elif(self.mode == "client"):
            self.startClient()

        
    
    def startServer(self):
        self.server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.server.bind((self.host,self.port))
        self.server.listen(1)
        
        print(Fore.GREEN+Style.BRIGHT+"[+] "+Style.RESET_ALL+"Server is start on {} port {}".format(self.host,self.port))

        while True:
            self.machine,self.info = self.server.accept()
            break

        print(Fore.GREEN+Style.BRIGHT+"[!] "+Style.RESET_ALL+"Guest is connect: {0}:{1}".format(self.info[0],self.info[1]))

        self.n = threading.Thread(target = self.recvMSG,args = (),)
        self.n.start()

        self.msgConsole()

    def startClient(self):
        self.client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print(Fore.YELLOW+"[~] "+Style.RESET_ALL+"Connect...")
        self.client.connect((self.host,self.port))
        print(Fore.GREEN+Style.BRIGHT+"[!] "+Style.RESET_ALL+"Connection established")
        self.machine = self.client

        self.n = threading.Thread(target = self.recvMSG,args = (),)
        self.n.start()        

        self.msgConsole()        
        

    def recvMSG(self): # Mesajları bekliyor
        while(True):
            try:
                mesaj = self.machine.recv(1024)
                if(mesaj == "q"):
                    print(Fore.RED+Style.BRIGHT+"\n\t[-] "+Style.RESET_ALL+"client send close message")
                    if(self.mode == "server"):
                        self.machine.close()
                        sys.exit(0)
                    else:
                        self.machine.close()
                        sys.exit(0)
                    break
                elif len(mesaj)>0:
                    print("\n"+Fore.YELLOW+"-"*50)
                    print(Fore.GREEN+Style.BRIGHT+"\n[MSG] "+Style.RESET_ALL+"{}\n".format(mesaj))
                    if(self.mode == "server"):
                        self.execute(mesaj)
                    print("\n"+Fore.YELLOW+"-"*50)
                else:
		    self.machine.close()
                    break
            except Exception as e:
                print(Fore.RED+"[-] Error: {}".format(e.message))
    def msgConsole(self):
        if(self.mode == "client"):
            while(True):
                mesaj = raw_input(Fore.GREEN+"[~] "+Style.RESET_ALL+"your command: ")
                if(mesaj == "exit" or mesaj == "q"):
                    self.machine.send("q")
                    sys.exit(0)
                    break
                else:
                    print(Fore.GREEN+"[+] "+Style.RESET_ALL+"send: {}".format(mesaj))
                    self.machine.send(mesaj)
        else:
            print(Fore.YELLOW+"\n[...] "+Style.RESET_ALL+"Listen messages")

    def execute(self,command):
        if(len(command) > 0):
            if(command not in self.badCommand):
                print(Fore.GREEN+Style.BRIGHT+"\n\t[EXEC] "+Style.RESET_ALL+"{}".format(command))
                parse = command.split(" ") or command
                try:
                    os.system(command)
                    output = subprocess.check_output(parse,shell = True)
                except:
                    output = False
                    
                if(output):
                    self.machine.send(output)
                else:
                    self.machine.send("False")
            else:
                print(Fore.RED+"\n\t[-] Not exec. It's a bad command: {}".format(command))
                self.machine.send("Bad command")
        else:
            print(Fore.YELLOW+Style.BRIGHT+"\n\t[-] "+Style.RESET_ALL+"Command not valid: {}".format(command))


    def close(self):
        if(self.mode == "server"):
            self.server.close()
        else:
            self.client.close()
            
        sys.exit(0)

port = 8087

if(sys.argv[1] in ["-c","--client"]):
    Komando(mode = "client",port = port).start()
elif(sys.argv[1] in ["-s","--server"]):
    Komando(port = port).start()



    
