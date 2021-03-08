from tkinter import *
import threading
import socket
import time
import re
from tkinter import scrolledtext


class Client():

    def __init__(self, username, server, port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, port))
        self.username = username
        self.send("USERNAME {0}".format(username))
        self.listening = True

    def listener(self):
        while self.listening:
            data = ""
            try:
                data = self.socket.recv(1024).decode('UTF-8')
            except socket.error:
                messagesConsole.insert("Unable to receive data")
                print("Unable to receive data")
            self.handle_msg(data)
            time.sleep(0.1)

    def listen(self):
        self.listen_thread = threading.Thread(target=self.listener)
        self.listen_thread.daemon = True
        self.listen_thread.start()

    def send(self, message):
        try:
            username_result = re.search('^USERNAME (.*)$', message)
            if not username_result:
                message = "{0}: {1}".format(self.username, message)
            self.socket.sendall(message.encode("UTF-8"))
        except socket.error:
            messagesConsole.insert("unable to send message")
            print("unable to send message")

    def tidy_up(self):
        self.listening = False
        self.socket.close()

    def handle_msg(self, data):
        if data == "QUIT":
            self.tidy_up()
        elif data == "":
            self.tidy_up()
        else:
            messagesConsole.insert(data)
            print(data)



def sendMessage():
    #Only for tests
    #print(messageText.get())
    if messageText.get()=="":
        print("Empty message")
    else:
        #add message to the chat and delete the textin the message field
        messagesConsole.insert(END,str(messageText.get()) + "\n")
        #messagesConsole.delete(0, 'end')

#Trying to connect the client to the server
def valideConnection():
    client = Client(username, server, port)
    client.listen()
    message = ""
    while message != "QUIT":
        message = messageText.get()
        #message = input()
        client.send(message)

#UI Elements
root = Tk(className='Messagerie Python')
root.title('Simple exemple')
root.geometry("1000x680")

#UI connection entries
coUsername = Entry(root, bd=3, width=25)
coServer = Entry(root, bd=3, width=25)
coServer.config(show="*")
coPort = Entry(root, bd=3, width=25)
coPort.config(show="*")
coButton = Button(root, text="Connection", command=valideConnection)
#UI chat
messagesConsole = scrolledtext.ScrolledText(root, height=30, width=100)
# messagesConsole.configure(state='enable')

#UI message entries
messageText = Entry(root, bd=3, width=100)
sendButon = Button(root,  command=sendMessage, text="Send")
#UI display
coUsername.pack()
coServer.pack()
coPort.pack()
coButton.pack()

# E.pack(side="left", size="300")
messagesConsole.pack()
messageText.pack();sendButon.pack()
#UI launch window
root.mainloop() 


# def sendMessage():
#     if messageText.get()!=0:
#         messagesConsole.insert(END, messageText.get())

if __name__ == "__main__":
    username = coUsername.get()
    server = coServer.get()
    port = coPort.get()
    int(input("port: "))
    client = Client(username, server, port)
    client.listen()
    message = ""
    while message != "QUIT":
        message = messageText.get()
        #message = input()
        client.send(message)



##########################################################################################################
##########################################################################################################
##########################################################################################################


# import tkinter as tk
# from tkinter import scrolledtext


# class ClientApp(tk.Tk):
#     def __init__(self, *args, **kwargs):
#         tk.Tk.__init__(self, *args, **kwargs)

#         container = tk.Frame(self)
#         container.pack(side="top", fill="both", expand=True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)

#         self.frames = {}
#         for F in (StartPage, PageMain):
#             page_name = F.__name__
#             frame = F(parent=container, controller=self)
#             self.frames[page_name] = frame
#             frame.grid(row=0, column=0, sticky="nsew")

#         self.show_frame("StartPage")

#     def show_frame(self, page_name):
#         frame = self.frames[page_name]
#         frame.tkraise()


# class StartPage(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         tk.Label(self, text="Messagerie config:").grid(row=0, column=0)
#         tk.Label(self, text="username:").grid(row=1, column=0)
#         tk.Label(self, text="server:").grid(row=2, column=0)
#         tk.Label(self, text="port:").grid(row=3, column=0)

#         self.entryUsername = tk.Entry(self)
#         self.entryUsername.grid(row=1, column=1)
#         self.entryServer = tk.Entry(self)
#         self.entryServer.grid(row=2, column=1)
#         self.entryPort = tk.Entry(self)
#         self.entryPort.grid(row=3, column=1)
#         button = tk.Button(self, text="validate", command=self.validateConfig)
#         button.grid(row=4, column=0, columnspan=2)

#     def validateConfig(self):
#         self.controller.show_frame("PageMain")


# class PageMain(tk.Frame):
#     def __init__(self, parent, controller):
#         tk.Frame.__init__(self, parent)
#         self.controller = controller
#         tk.Label(self, text="Messagerie config:").grid(row=0, column=0)

#         self.entryText = tk.Entry(self)
#         self.entryText.grid(row=1, column=1, sticky="o")
#         self.entryServer = tk.Entry(self)
#         self.entryServer.grid(row=2, column=1)
#         self.entryPort = tk.Entry(self)
#         self.entryPort.grid(row=3, column=1)
#         button = tk.Button(self, text="validate")
#         # , command=self.validateConfig
#         button.grid(row=4, column=0, columnspan=2)


# if __name__ == "__main__":
#     app = ClientApp()
#     app.mainloop()
