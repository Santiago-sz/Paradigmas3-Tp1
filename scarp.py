import requests
from bs4 import BeautifulSoup

# Función para realizar el scraping
def scrapear_precio_producto(url):
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            sopa = BeautifulSoup(respuesta.content, "html.parser")

            # Buscar los productos según la tienda
            productos = []
            if "musimundo" in url:
               productos = sopa.find_all('div', class_='mus-product-box')
            elif 'mercadolibre' in url:
                productos = sopa.find_all('li', class_='ui-search-layout__item')

            resultados = []
            
            for producto in productos:
                # Para Musimundo
                if "musimundo" in url:
                    h3 = producto.find('h3', class_='mus-pro-name')
                    titulo = h3.text.strip() if h3 else 'Título no encontrado'                    
                    # Buscar el precio
                    span_tag = producto.find('span', class_='mus-pro-price-number')
                    precio = span_tag.text.strip() if span_tag else 'Precio no encontrado'
                
                # Para MercadoLibre
                elif 'mercadolibre' in url:
                    # Para Mercado Libre, las clases correctas son estas
                    titulo_tag = producto.find('h2', class_='poly-box')
                    precio_tag = producto.find('span', class_='andes-money-amount__fraction')
                    titulo = titulo_tag.text.strip() if titulo_tag else 'Título no encontrado'
                    precio = precio_tag.text.strip() if precio_tag else 'Precio no encontrado'
                
                # Guardar el resultado
                if titulo and precio:
                    resultados.append(f"{titulo}: {precio}")
            
            if resultados:
                return "\n".join(resultados)
            else:
                return "No se encontró información del producto."
        else:
            return f"Error al acceder a {url}: {respuesta.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

# Función para probar el scraping con diferentes páginas y productos
def funcion_prueba(pagina):
    message = "scrape enova n50, radio"  # Cambia esto según sea necesario
    queries = message[len('scrape '):].split(',')

    results = []
    for query in queries:
        query = query.strip().replace(' ', '-')
        if pagina == 'mm':
            url_producto = f"https://www.musimundo.com/search/?text={query}"
        elif pagina == 'ml':
            url_producto = f"https://listado.mercadolibre.com.ar/{query}#D[A:{query}]"
        
        print(f"Scraping en URL: {url_producto}")
        result = scrapear_precio_producto(url_producto)
        results.append(f"Resultados para '{query}':\n{result}")
    
    final_result = "\n\n".join(results)
    print(final_result)

if __name__ == '__main__':
    funcion_prueba('ml')
