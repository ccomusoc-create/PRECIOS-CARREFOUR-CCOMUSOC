import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import os

PRODUCTOS = {
    "leche": "https://www.carrefour.com.ar/leche-entera-la-serenisima-1-lt/p",
    "cafe": "https://www.carrefour.com.ar/cafe-instantaneo-nestle-dolca-170-gr/p",
    "yerba": "https://www.carrefour.com.ar/yerba-mate-playadito-1-kg/p",
    "azucar": "https://www.carrefour.com.ar/azucar-ledezma-1-kg/p",
    "dulce_de_leche": "https://www.carrefour.com.ar/dulce-de-leche-la-serenisima-400-gr/p",
    "pan": "https://www.carrefour.com.ar/pan-lactal-bimbo-400-gr/p",
    "harina": "https://www.carrefour.com.ar/harina-0000-pureza-1-kg/p",
    "huevos": "https://www.carrefour.com.ar/maple-huevo-blanco-12-unidades/p",
    "sal": "https://www.carrefour.com.ar/sal-fina-celusal-500-gr/p",
    "aceite": "https://www.carrefour.com.ar/aceite-girasol-cocinero-1-5-lts/p",
    "asado": "https://www.carrefour.com.ar/corte-asado/p",
    "pollo": "https://www.carrefour.com.ar/pollo-fresco/p",
    "arroz": "https://www.carrefour.com.ar/arroz-gallo-oro-1-kg/p",
    "fideos": "https://www.carrefour.com.ar/fideos-matarazzo-spaghetti-500-gr/p",
    "papa": "https://www.carrefour.com.ar/papa-1-kg/p",
    "zanahoria": "https://www.carrefour.com.ar/zanahoria-1-kg/p",
    "cebolla": "https://www.carrefour.com.ar/cebolla-1-kg/p",
    "banana": "https://www.carrefour.com.ar/banana-1-kg/p",
    "manzana": "https://www.carrefour.com.ar/manzana-roja-1-kg/p",
    "naranja": "https://www.carrefour.com.ar/naranja-1-kg/p",
    "lechuga": "https://www.carrefour.com.ar/lechuga-francesa/p",
    "tomate": "https://www.carrefour.com.ar/tomate-redondo-1-kg/p",
    "pañales": "https://www.carrefour.com.ar/panales-pampers-supersec-x60/p",
    "papel_higienico": "https://www.carrefour.com.ar/papel-higienico-elite-12-rollos/p",
    "jabon_tocador": "https://www.carrefour.com.ar/jabon-de-tocador-dove-90-gr/p",
    "shampoo": "https://www.carrefour.com.ar/shampoo-sedal-340-ml/p",
    "acondicionador": "https://www.carrefour.com.ar/acondicionador-sedal-340-ml/p",
    "maquina_afeitar": "https://www.carrefour.com.ar/maquina-de-afeitar-gillette-blue-3-x2/p",
    "pasta_dental": "https://www.carrefour.com.ar/pasta-dental-colgate-90-gr/p",
    "detergente": "https://www.carrefour.com.ar/detergente-ala-750-ml/p",
    "lavandina": "https://www.carrefour.com.ar/lavandina-ayudin-1-l/p",
    "jabon_polvo": "https://www.carrefour.com.ar/jabon-en-polvo-ala-3kg/p",
    "caldo": "https://www.carrefour.com.ar/caldo-de-verduras-knorr-12-cubitos/p",
    "agua": "https://www.carrefour.com.ar/agua-mineral-villavicencio-2-25-lts/p",
    "perros": "https://www.carrefour.com.ar/alimento-para-perro-dog-chow-21-kg/p",
    "gatos": "https://www.carrefour.com.ar/alimento-para-gato-cat-chow-15-kg/p",
    "leche_formula": "https://www.carrefour.com.ar/nutrilon-1-800gr/p"
}

def obtener_precio(url):
    r = requests.get(url, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    precio = soup.find("span", {"class": "valtech-carrefourar-product-price-0-x-sellingPriceValue"})
    if precio:
        return float(precio.text.replace("$", "").replace(".", "").replace(",", ".").strip())
    return None

def main():
    filas = []
    fecha = datetime.now().strftime("%Y-%m-%d")

    for producto, url in PRODUCTOS.items():
        precio = obtener_precio(url)
        filas.append([fecha, producto, precio])

    df = pd.DataFrame(filas, columns=["fecha", "producto", "precio"])

    # cargar histórico
    archivo = "data/precios.csv"
    if os.path.exists(archivo):
        historial = pd.read_csv(archivo)
        df = pd.concat([historial, df], ignore_index=True)

    df.to_csv(archivo, index=False)

    # generar gráfico
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10,5))
    df_plot = df[df["producto"] == "leche"]
    plt.plot(df_plot["fecha"], df_plot["precio"])
    plt.xticks(rotation=90)
    plt.title("Evolución del precio - Leche")
    plt.tight_layout()
    plt.savefig("charts/grafico.png")

if __name__ == "__main__":
    main()
