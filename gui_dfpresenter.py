import tkinter as tk
import pandas as pd
from distance_calculations import *

class WDfPresenter(tk.Frame):
    def __init__(self, root=None):
        "Menampilkan dataframe input"
        tk.Frame.__init__(self, root)
        self.root = root
        self.createWidget()

    def createWidget(self):
        label = tk.Label(self.root, text="DataFrame Input")
        label.config(font=("Courier", 14))
        label.pack()
        self.vsb = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.hsb = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.hsb.pack(fill=tk.X, side=tk.BOTTOM)

        self.textDF=tk.Text(self, wrap=tk.NONE, width=50, height=10)
        self.textDF['yscrollcommand']=self.vsb.set
        self.textDF["xscrollcommand"]=self.hsb.set
        self.textDF.config(state=tk.DISABLED)
        
        self.vsb.config(command=self.textDF.yview)
        self.hsb.config(command=self.textDF.xview)
        self.textDF.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    def onNewCsvEvent(self, event):
        print("onNewCsvEvent")
        new_csv = event.widget.getDF()
        self.df = add_distances(new_csv)
        self.textDF.config(state=tk.NORMAL)
        self.textDF.delete("0.0", tk.END)
        self.textDF.insert(tk.END, self.df)
        self.textDF.config(state=tk.DISABLED)
        self.event_generate("<<UpdateParams>>")
        

    def getParams(self):
        return self.df


if __name__ == "__main__":
    
    class Appli(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)

        def getDF(self):
            df = pd.read_csv("input.csv")
            return df

    def sendNewCsvEvent():
        print("new CSV event")
        root.event_generate("<<NewCSV>>")
        root.after(2000, sendNewCsvEvent)

    def onUpdateParamsEvent(event):
        params = event.widget.getParams()
        print(params)

    print("in main")
    root = Appli()
    wpres = WDfPresenter(root)
    wpres.pack()
    wpres.bind_all("<<NewCSV>>", wpres.onNewCsvEvent)
    root.bind_all("<<UpdateParams>>", onUpdateParamsEvent)
    root.after(2000, sendNewCsvEvent)

    root.mainloop()