import pykka
import socket
import threading
import requests
from bs4 import BeautifulSoup
import time

# Definición de actores para cada tienda
class ScraperMercadoLibre(pykka.ThreadingActor):
    def on_receive(self, mensaje):
        url = mensaje.get("url")
        result_handler = mensaje.get('result_handler')
        if url:
            print(f"Scraping en URL: {url}")  # Mensaje de depuración
            result = self.scrapear_producto(url)
            if result_handler:
                print(f"Enviando resultado al handler: {result}")  # Mensaje de depuración
                result_handler.tell(result)
        else:
            if result_handler:
                result_handler.tell("URL no proporcionada")

    def scrapear_producto(self, url):
        time.sleep(0.1)  # Simula la limitación de CPU
        try:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                sopa = BeautifulSoup(respuesta.text, 'lxml')
                productos = sopa.find_all('li', class_='ui-search-layout__item')
                resultados = []
                min_precio = float('inf')
                min_producto = None
                for producto in productos:
                    titulo = producto.find('h2', class_='poly-box')
                    precio = producto.find('span', class_='andes-money-amount__fraction')
                    if titulo and precio:
                        precio_texto = precio.text.strip().replace('.', '').replace(',', '.').replace('$', '')
                        try:
                            precio_valor = float(precio_texto)
                            if precio_valor < min_precio:
                                min_precio = precio_valor
                                min_producto = f"{titulo.text.strip()} - ${precio.text.strip()}"
                            resultados.append(f"{titulo.text.strip()} - ${precio.text.strip()}")
                        except ValueError:
                            resultados.append(f"Error al convertir el precio: {precio.text.strip()}")
                    else:
                        resultados.append("Información incompleta para un producto.")
                if min_producto:
                    resultados.append(f"\nProducto más barato: {min_producto}")
                if resultados:
                    return "\n".join(resultados)
                else:
                    return "No se encontraron productos."
            else:
                return f"Error al acceder a {url}: {respuesta.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

class ScraperFravega(pykka.ThreadingActor):
    def on_receive(self, mensaje):
        url = mensaje.get("url")
        result_handler = mensaje.get('result_handler')
        if url:
            print(f"Scraping en URL: {url}")  # Mensaje de depuración
            result = self.scrapear_producto(url)
            if result_handler:
                print(f"Enviando resultado al handler: {result}")  # Mensaje de depuración
                result_handler.tell(result)
        else:
            if result_handler:
                result_handler.tell("URL no proporcionada")

    def scrapear_producto(self, url):
        time.sleep(0.1)  # Simula la limitación de CPU
        try:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                sopa = BeautifulSoup(respuesta.text, 'lxml')
                productos = sopa.find_all('article', class_='sc-812c6cb5-2')
                resultados = []
                min_precio = float('inf')
                min_producto = None
                for producto in productos:
                    titulo = producto.find('span', class_='sc-ca346929-0')
                    precio = producto.find('span', class_='sc-1d9b1d9e-0')
                    if titulo and precio:
                        precio_texto = precio.text.strip().replace('.', '').replace(',', '.').replace('$', '')
                        try:
                            precio_valor = float(precio_texto)
                            if precio_valor < min_precio:
                                min_precio = precio_valor
                                min_producto = f"{titulo.text.strip()} - ${precio.text.strip()}"
                            resultados.append(f"{titulo.text.strip()} - ${precio.text.strip()}")
                        except ValueError:
                            resultados.append(f"Error al convertir el precio: {precio.text.strip()}")
                    else:
                        resultados.append("Información incompleta para un producto.")
                if min_producto:
                    resultados.append(f"\nProducto más barato: {min_producto}")
                if resultados:
                    return "\n".join(resultados)
                else:
                    return "No se encontraron productos."
            else:
                return f"Error al acceder a {url}: {respuesta.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

class ScraperMusimundo(pykka.ThreadingActor):
    def on_receive(self, mensaje):
        url = mensaje.get("url")
        result_handler = mensaje.get('result_handler')
        if url:
            print(f"Scraping en URL: {url}")  # Mensaje de depuración
            result = self.scrapear_producto(url)
            if result_handler:
                print(f"Enviando resultado al handler: {result}")  # Mensaje de depuración
                result_handler.tell(result)
        else:
            if result_handler:
                result_handler.tell("URL no proporcionada")

    def scrapear_producto(self, url):
        time.sleep(0.1)  # Simula la limitación de CPU
        try:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                sopa = BeautifulSoup(respuesta.text, 'lxml')
                productos = sopa.find_all('div', class_='mus-product-box')
                resultados = []
                min_precio = float('inf')
                min_producto = None
                for producto in productos:
                    titulo = producto.find('h3', class_='mus-pro-name')
                    precio = producto.find('span', class_='mus-pro-price-number')
                    if titulo and precio:
                        precio_texto = precio.text.strip().replace('.', '').replace(',', '.').replace('$', '')
                        try:
                            precio_valor = float(precio_texto)
                            if precio_valor < min_precio:
                                min_precio = precio_valor
                                min_producto = f"{titulo.text.strip()} - ${precio.text.strip()}"
                            resultados.append(f"{titulo.text.strip()} - ${precio.text.strip()}")
                        except ValueError:
                            resultados.append(f"Error al convertir el precio: {precio.text.strip()}")
                    else:
                        resultados.append("Información incompleta para un producto.")
                if min_producto:
                    resultados.append(f"\nProducto más barato: {min_producto}")
                if resultados:
                    return "\n".join(resultados)
                else:
                    return "No se encontraron productos."
            else:
                return f"Error al acceder a {url}: {respuesta.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

# Definición del actor para manejar la conexión y el envío de resultados
class ServerActor(pykka.ThreadingActor):
    def _init_(self):
        super()._init_()
        self.connection = None
        self.results = []

    def on_receive(self, mensaje):
        if isinstance(mensaje, dict) and mensaje.get('type') == 'set_connection':
            self.connection = mensaje.get('connection')
            print("Conexión establecida en ServerActor")  # Mensaje de depuración
        elif isinstance(mensaje, dict) and mensaje.get('type') == 'scrape_requests':
            requests_list = mensaje.get('requests')
            self.results = [''] * len(requests_list)  # Inicializar la lista de resultados

            # Crear y enviar solicitudes a múltiples actores de scraping
            for idx, request in enumerate(requests_list):
                query = request.get('query')
                page = request.get('page')
                if page == 'ml':
                    url_producto = f"https://listado.mercadolibre.com.ar/{query}#D[A:{query}]"
                    scraper = ScraperMercadoLibre.start()
                elif page == 'fv':
                    url_producto = f"https://www.fravega.com/l/?keyword={query}"
                    scraper = ScraperFravega.start()
                elif page == 'mm':
                    url_producto = f"https://www.musimundo.com/search/?text={query}"
                    scraper = ScraperMusimundo.start()
                else:
                    continue
                scraper.tell({'url': url_producto, 'result_handler': self.actor_ref.proxy().result_handler(idx)})

    def result_handler(self, idx):
        class ResultHandler(pykka.ThreadingActor):
            def _init_(self, server_actor, idx):
                super()._init_()
                self.server_actor = server_actor
                self.idx = idx

            def on_receive(self, result):
                self.server_actor.results[self.idx] = result
                if all(self.server_actor.results):
                    final_result = "\n\n".join(self.server_actor.results)
                    self.server_actor.connection.sendall(final_result.encode())
                    self.server_actor.connection.close()
        
        return ResultHandler(self, idx).start()

# Servidor TCP/IP
def start_server():
    host = '192.168.0.123'
    port = 8786

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print("Servidor esperando conexión...")

    while True:
        conn, addr = server_socket.accept()
        print(f"Conectado a {addr}")

        def handle_client(conn):
            server_actor = ServerActor.start()
            server_actor.tell({'type': 'set_connection', 'connection': conn})
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                if message.startswith('scrape'):
                    parts = message[len('scrape '):].split(',')
                    requests = [{'query': part.split(':')[1].strip(), 'page': part.split(':')[0].strip()} for part in parts]
                    server_actor.tell({'type': 'scrape_requests', 'requests': requests})

        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()

if __name__ == '__main__':
    start_server()