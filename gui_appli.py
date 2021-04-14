import tkinter as tk
from gui_menu import *
from gui_map import *
from gui_dfpresenter import *
from gui_resultpresenter import *

if __name__ == "__main__":
    print("in main")
    root = tk.Tk()
    #menu
    wmen = WMenu(root)
    wmen.pack()

    #tampilan gui dari atas ke bawah
    wmap = WMap(root)
    wmap.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    view = tk.Frame()
    wpres = WDfPresenter(view)
    wpres.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    wres = WResultPresenter(view)
    wres.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
    view.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

    root.bind_all("<<NewCSV>>", wpres.onNewCsvEvent)
    root.bind_all("<<UpdateParams>>", wres.onUpdateParamsEvent, add="+")
    root.bind_all("<<UpdateParams>>", wmap.onUpdateParamsEvent, add="+")
    root.bind_all("<<UpdateWeights>>", wres.onUpdateWeightsEvent)

    root.mainloop()