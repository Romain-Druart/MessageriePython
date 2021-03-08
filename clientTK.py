import tkinter as tk
from tkinter import scrolledtext
from client import Client


class ClientApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageMain):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Messagerie config:").grid(row=0, column=0)
        tk.Label(self, text="username:").grid(row=1, column=0)
        tk.Label(self, text="server:").grid(row=2, column=0)
        tk.Label(self, text="port:").grid(row=3, column=0)

        self.entryUsername = tk.Entry(self)
        self.entryUsername.grid(row=1, column=1)
        self.entryServer = tk.Entry(self)
        self.entryServer.grid(row=2, column=1)
        self.entryPort = tk.Entry(self, show="*")
        self.entryPort.grid(row=3, column=1)
        button = tk.Button(self, text="validate", command=lambda: self.validateConfig({
            'username': self.entryUsername.get(),
            'server': self.entryServer.get(),
            'port': int(self.entryPort.get())
        }))
        button.grid(row=4, column=0, columnspan=2)
        button.grid(row=4, column=0, columnspan=2)

    def validateConfig(self, data):
        Client.receiveData(data)
        self.controller.show_frame("PageMain")


class PageMain(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        tk.Label(self, text="Messagerie config:").grid(row=0, column=0)

        self.scrolledText = scrolledtext.ScrolledText(self)
        self.scrolledText.grid(row=1, column=1, sticky="w")
        self.userMessage = tk.Entry(self)
        self.userMessage.grid(row=2, column=1)
        button = tk.Button(self, text="send", command=lambda: self.sendMessage({
            'message': self.userMessage.get()
            # 'username': StartPage.entryUsername.get(),
            # 'server': StartPage.entryServer.get(),
            # 'port': int(self.entryPort.get())
        }))
        # , command=self.validateConfig
        button.grid(row=4, column=0, columnspan=2)

    def sendMessage(self, data):
        Client.sendData(data)
        self.scrolledText.insert(self.userMessage.get())

if __name__ == "__main__":
    app = ClientApp()
    app.mainloop()
