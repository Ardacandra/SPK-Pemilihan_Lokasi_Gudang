import tkinter as tk
import tkinter.filedialog as tkf # python3
import pandas as pd
from gui_weightsupdate import *
from gui_infrastructuretable import *

class WMenu(tk.Frame):
    def __init__(self, root=None):
        "Konstruksi menu bar"
        tk.Frame.__init__(self, root)
        self.root = root
        self.menu = tk.Menu(root)
        self.createMenu()
        root.config(menu=self.menu)

    def createMenu(self):
        w = self.menu
        w.add_cascade(label="File", menu=self.createFileMenu())
        w.add_cascade(label="Tool", menu=self.createToolMenu())

    def createFileMenu(self):
        #=============================================File option
        m=tk.Menu(self, tearoff=0)
        m.add_command(label="Open CSV", command=self.cmdOpenCSV)
        m.add_command(label="Exit", command=self.root.quit)
        return m

    def createToolMenu(self):
        #=============================================Tool option
        m = tk.Menu(self, tearoff=0)
        m.add_command(label="Display infrastructure locations", command=self.displayTable)
        m.add_command(label="Change weights", command=self.changeWeights)
        return m

    def cmdOpenCSV(self):
        opts = {    'filetypes': (('CSV', '.csv'),
                              ('Text files', '.txt'),
                              ('All files', '.*'),)}
        opts['title'] = 'Select a file to open...'
        fn = tkf.askopenfilename(**opts)
        if len(fn)>0:
            self.df = pd.read_csv(fn)
            self.event_generate("<<NewCSV>>")

    def getDF(self):
        return self.df

    def displayTable(self):
        newWindow = tk.Toplevel(self)
        newWindow.title("Infrastructures")
        wweight = WInfraPresenter(newWindow)
        wweight.pack()
    
    def changeWeights(self):
        newWindow = tk.Toplevel(self)
        newWindow.title("Weights")
        wweight = WWeightsUpdate(newWindow)
        wweight.pack()


if __name__ == '__main__':
        
    def window(event):
        print("in window")
        print(event.widget.getDF())

    print("in main")
    root=tk.Tk()
    fm=WMenu(root)
    fm.pack()

    root.bind_all("<<NewCSV>>", window)
    
    root.mainloop()
