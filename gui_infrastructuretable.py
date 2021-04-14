from db_functions import *
import tkinter as tk
import pandas as pd

class WInfraPresenter(tk.Frame):
    def __init__(self, root=None):
        "Menampilkan infrastruktur (pabrik dan gudang)"
        tk.Frame.__init__(self, root)
        self.root = root
        self.createWidget()

    def createWidget(self):
        conn = create_connection(r"database/pythonsqlite.db")
        factories = select_all_factories(conn)
        warehouses = select_all_warehouses(conn)
        conn.close()
        
        f_df = pd.DataFrame(factories)
        f_df.columns = ["Index", "Name", "Latitude", "Longitude"]
        w_df = pd.DataFrame(warehouses)
        w_df.columns = ["Index", "Name", "Latitude", "Longitude"]

        self.vsb = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.vsb.pack(fill=tk.Y, side=tk.RIGHT)
        self.hsb = tk.Scrollbar(self, orient=tk.HORIZONTAL)
        self.hsb.pack(fill=tk.X, side=tk.BOTTOM)

        self.textDF=tk.Text(self, wrap=tk.NONE, width=50, height=10)
        self.textDF['yscrollcommand']=self.vsb.set
        self.textDF["xscrollcommand"]=self.hsb.set
        self.textDF.insert(tk.END, "FACTORY\n")
        self.textDF.insert(tk.END, f_df)
        self.textDF.insert(tk.END, "\n\nWAREHOUSE\n")
        self.textDF.insert(tk.END, w_df)
        self.textDF.config(state=tk.DISABLED)
        
        self.vsb.config(command=self.textDF.yview)
        self.hsb.config(command=self.textDF.xview)
        self.textDF.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

if __name__ == "__main__":
    class Appli(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)

    print("in main")
    root = Appli()
    wweights = WInfraPresenter(root)
    wweights.pack()

    root.mainloop()