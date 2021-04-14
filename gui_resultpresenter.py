import tkinter as tk
import pandas as pd
from topsis.topsis_model import *
from gui_dfpresenter import *
from db_functions import *

class WResultPresenter(tk.Frame):
    def __init__(self, root=None):
        "Menampilkan dataframe hasil perhitungan TOPSIS"
        tk.Frame.__init__(self, root)
        self.root = root
        conn = create_connection(r"database/pythonsqlite.db")
        weights = select_all_weights(conn)
        conn.close()
        self.weights = [w[2] for w in weights]
        self.createWidget()

    def createWidget(self):
        label = tk.Label(self.root, text="TOPSIS Model Result")
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

    def onUpdateParamsEvent(self, event):
        print("onUpdateParamsEvent")
        new_params = event.widget.getParams()
        self.df = new_params[[
            "nama_daerah", "gaji_rata2", "kepadatan_penduduk", 
            "jarak_pabrik", "jarak_gudang", "harga_tanah"]]
        self.results = topsis(self.df, self.weights)

        self.textDF.config(state=tk.NORMAL)
        self.textDF.delete("0.0", tk.END)
        self.textDF.insert(tk.END, self.results)
        self.textDF.config(state=tk.DISABLED)

    def onUpdateWeightsEvent(self, event):
        print("onUpdateWeightsEvent")
        if self.df is None:
            return
        conn = create_connection(r"database/pythonsqlite.db")
        weights = select_all_weights(conn)
        conn.close()
        self.weights = [w[2] for w in weights]
        self.results = topsis(self.df, self.weights)

        self.textDF.config(state=tk.NORMAL)
        self.textDF.delete("0.0", tk.END)
        self.textDF.insert(tk.END, self.results)
        self.textDF.config(state=tk.DISABLED)

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

    print("in main")
    root = Appli()
    wpres = WDfPresenter(root)
    wpres.pack()
    wres = WResultPresenter(root)
    wres.pack()
    root.bind_all("<<NewCSV>>", wpres.onNewCsvEvent)
    root.bind_all("<<UpdateParams>>", wres.onUpdateParamsEvent)
    root.after(2000, sendNewCsvEvent)

    root.mainloop()

