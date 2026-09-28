from pathlib import Path

import requests
import pandas as pd

URL = "https://amazon-reviews-api-g5ae.onrender.com/reviews"
CARPETA_DATOS = Path(__file__).resolve().parent / "data"

def obtener_resenias(tamanio):
    lista_resenias = []
    offset = 0
    while True:
        parametros = {"limit": tamanio, "offset": offset}
        response = requests.get(URL, params=parametros)
        if response.status_code == 200:
            respuesta = response.json()
            resenias = respuesta.get("data")
            lista_resenias.extend(resenias)

            offset += respuesta.get("returned")

            if offset >= respuesta.get("total_matching"):
                break
        else:
            print('Error:', response.status_code)

    dataset = pd.DataFrame(lista_resenias)
    CARPETA_DATOS.mkdir(parents=True, exist_ok=True)
    dataset.to_csv(CARPETA_DATOS / "dataset.csv", index=False)
    print(dataset.describe())

obtener_resenias(tamanio=1000)
