import json  
import requests

url = "https://amazon-reviews-api-g5ae.onrender.com/reviews"
todas = []
offset = 0
limit = 1000

respuesta = requests.get(url)     
datos = respuesta.json()           
total = datos["total_matching"]              

while offset < total:
    respuesta = requests.get(url, params={"offset": offset, "limit": limit})
    datos = respuesta.json()

    todas.extend(datos["data"])

    offset = offset + limit
    print(f"Llevo {len(todas)} reseñas")

with open("reviews_raw.json", "w", encoding="utf-8") as f:
    json.dump(todas, f, ensure_ascii=False)