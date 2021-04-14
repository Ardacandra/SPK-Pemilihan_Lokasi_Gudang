from numpy.core.fromnumeric import argmin
import pandas as pd
import numpy as np
from db_functions import *

def calculate_distance(lat1, long1, lat2, long2):
    return np.sqrt((lat1-lat2)**2 + (long1-long2)**2)

def get_shortest_distance(lat, long, coords):
    distances = []
    for cor in coords:
        lat2 = cor[2]
        long2 = cor[3]
        distances.append(calculate_distance(lat, long, lat2, long2))
    dist = min(distances)
    id = coords[argmin(distances)][0]
    return id, dist

def add_distances(df):
    conn = create_connection(r"database/pythonsqlite.db")
    factories = select_all_factories(conn)
    warehouses = select_all_warehouses(conn)
    conn.close()
    
    f_id_list = []
    f_dist_list = []
    w_id_list = []
    w_dist_list = []
    for i in range(len(df)):
        lat = df.loc[i, "latitude"]
        long = df.loc[i, "longitude"]
        f_id, f_dist = get_shortest_distance(lat, long, factories)
        w_id, w_dist = get_shortest_distance(lat, long, warehouses)
        f_id_list.append(f_id)
        f_dist_list.append(f_dist)
        w_id_list.append(w_id)
        w_dist_list.append(w_dist)
    df["jarak_pabrik"] = f_dist_list
    df["id_pabrik"] = f_id_list
    df["jarak_gudang"] = w_dist_list
    df["id_gudang"] = w_id_list

    return df

if __name__ == "__main__":
    df = pd.read_csv("input.csv")
    print(add_distances(df))