from db_functions import *
import tkinter as tk
import folium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
from PIL import ImageTk, Image

def map_to_png(m, fname, path=None):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    if not path:
        path = os.getcwd()
    # save the map, open with selenium, wait for initial load
    m.save('{}/map.html'.format(path))
    browser.get('file://{}/map.html'.format(path))
    time.sleep(1)
    browser.save_screenshot('{}/{}.png'.format(path, fname))
    browser.quit()

class WMap(tk.Frame):
    def __init__(self, root=None):
        "Menampilkan peta"
        tk.Frame.__init__(self, root)
        self.root = root
        self.createWidget()

    def createWidget(self):
        label = tk.Label(self, text="Map")
        label.config(font=("Courier", 14))
        label.pack()

        self.map = folium.Map(
            location=[-7, 110],
            tiles="StamenWatercolor",
            zoom_start=6.5
        )
        conn = create_connection(r"database/pythonsqlite.db")
        self.factories = select_all_factories(conn)
        self.warehouses = select_all_warehouses(conn)
        conn.close()

        factory_txt = '\
            <svg display="inline", position="relative", height="1em" ,width="1em", margin-right="1px">\
                <rect x="0", y="0" width="10" height="10", fill="black", opacity="1"/>\
                <text dx="0" dy="0" x="20%" y="85%" text-anchor="middle">\
                    {txt}\
                </text>\
            </svg>'
        warehouse_txt = '\
            <svg display="inline", position="relative", height="1em" ,width="1em", margin-right="1px">\
                <polygon points="0,0 10,0 5,10", fill="blue"/>\
                <text dx="0" dy="0" x="20%" y="85%" text-anchor="middle">\
                    {txt}\
                </text>\
            </svg>'
        factories_group = folium.FeatureGroup(name = factory_txt.format( txt= "Factory", col= "black"))
        warehouses_group = folium.FeatureGroup(name= warehouse_txt.format( txt= "Warehouse"))

        for f in self.factories:
            folium.Marker(
                location=[f[2], f[3]],
                icon=folium.DivIcon(html=f"""
                    <div><svg>
                        <rect x="0", y="0" width="10" height="10", fill="black", opacity="1"/>
                    </svg>""")
            ).add_to(factories_group)

        for w in self.warehouses:
            folium.Marker(
                location=[w[2], w[3]],
                icon=folium.DivIcon(html=f"""
                    <div><svg>
                        <polygon points="0,0 10,0 5,10", fill="blue"/>
                    </svg>""")
            ).add_to(warehouses_group)

        self.map.add_child(factories_group)
        self.map.add_child(warehouses_group)
        self.map.add_child(folium.map.LayerControl(collapsed=False))

        map_to_png(self.map, "map")

        self.canvas = tk.Canvas(self, width=800, height=600)
        self.canvas.pack()
        self.img = ImageTk.PhotoImage(Image.open("map.png").resize((800, 600), resample=Image.BICUBIC))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)

    def onUpdateParamsEvent(self, event):
        print("onUpdateParamsEvent")
        new_map = self.map
        new_params = event.widget.getParams()
        self.df = new_params[["latitude", "longitude", "id_pabrik", "id_gudang", "nama_daerah"]]
        candidates = self.df.values
        
        for c in candidates:
            folium.Marker(
                location=[c[0], c[1]],
                icon=folium.Icon(
                    color="red"),
                popup=folium.Popup(
                    c[4],
                    show=True
                )
            ).add_to(new_map)

            f_indexes = [f[0] for f in self.factories]
            id_fact = f_indexes.index(c[2])
            folium.PolyLine(
                locations=[
                    (c[0], c[1]),
                    (self.factories[id_fact][2], self.factories[id_fact][3])
                ],
                color="black",
                weight=5,
                opacity=0.8
            ).add_to(new_map)

            w_indexes = [w[0] for w in self.warehouses]
            id_ware = w_indexes.index(c[3])
            folium.PolyLine(
                locations=[
                    (c[0], c[1]),
                    (self.warehouses[id_ware][2], self.warehouses[id_ware][3])
                ],
                color="blue",
                weight=5,
                opacity=0.8
            ).add_to(new_map)

        map_to_png(new_map, "map")

        self.canvas.delete("all")
        self.img = ImageTk.PhotoImage(Image.open("map.png").resize((800, 600), resample=Image.BICUBIC))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.img)


if __name__ == "__main__":
    class Appli(tk.Tk):
        def __init__(self):
            tk.Tk.__init__(self)

    print("in main")
    root = Appli()
    wmap = WMap(root)
    wmap.pack()

    root.mainloop()