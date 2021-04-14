from db_functions import *
import tkinter as tk
from tkinter import messagebox

class WWeightsUpdate(tk.Frame):
    def __init__(self, root=None):
        "Menampilkan weights"
        tk.Frame.__init__(self, root)
        self.root = root
        self.createWidget()

    def createWidget(self):
        conn = create_connection(r"database/pythonsqlite.db")
        self.weights = select_all_weights(conn)
        conn.close()
        self.entry_list = []
        for i in range(len(self.weights)):
            exec("self.names_{} = tk.Label(self, text=self.weights[i][1])".format(i))
            exec("self.entry_{} = tk.Entry(self)".format(i))
            exec("self.entry_{}.insert(0, self.weights[i][2])".format(i))

            exec("self.names_{}.grid(row=0+i, column=0)".format(i))
            exec("self.entry_{}.grid(row=0+i, column=1)".format(i))
            exec("self.entry_list.append(self.entry_{})".format(i))

        self.update = tk.Button(self, text="Update Weights")
        self.update["command"] = self.update_weights
        self.update.grid(row=1+len(self.weights), columnspan=2)
    
    def update_weights(self):
        new_weights = []
        for i in range(len(self.weights)):
            new_val = self.entry_list[i].get()
            try:
                new_val = int(new_val)
            except ValueError:
                messagebox.showerror("Error", "Ada input yang salah!")
                return
            new_weights.append(new_val)

        conn = create_connection(r"database/pythonsqlite.db")
        update_weights(conn, new_weights)
        conn.close()
        print("Weights Updated")
        self.event_generate("<<UpdateWeights>>")

if __name__ == "__main__":
    class Appli(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)

    print("in main")
    root = Appli()
    wweights = WWeightsUpdate(root)
    wweights.pack()

    root.mainloop()
