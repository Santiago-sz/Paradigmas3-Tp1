import pykka
import socket
import threading
import requests
from bs4 import BeautifulSoup

# Definición del actor para el scraping
class ScraperMercadoLibre(pykka.ThreadingActor):
    def on_receive(self, mensaje):
        url = mensaje.get("url")
        result_handler = mensaje.get('result_handler')
        idx = mensaje.get('idx')
        if url:
            print(f"Scraping en URL: {url}")  # Mensaje de depuración
            result = self.scrapear_precio_producto(url)
            if result_handler:
                print("\n" f"Enviando resultado al handler: {result}")  # Mensaje de depuración
                result_handler.tell({'idx': idx, 'result': result})
        else:
            if result_handler:
                result_handler.tell({'idx': idx, 'result': "URL no proporcionada"})

    def scrapear_precio_producto(self, url):
        try:
            respuesta = requests.get(url)
            if respuesta.status_code == 200:
                sopa = BeautifulSoup(respuesta.content, "html.parser")
                
                # Buscar el precio del producto
                productos = sopa.find_all('li', class_='ui-search-layout__item')
                resultados = []
                for producto in productos:
                    titulo = producto.find('h2', class_='poly-box')
                    precio = producto.find('span', class_='andes-money-amount__fraction')
                    if titulo and precio:
                        resultados.append(f"{titulo.text.strip()}: ${precio.text.strip()}")
                
                if resultados:
                    return "\n".join(resultados)
                else:
                    return "No se encontró información del producto."
            else:
                return f"Error al acceder a {url}: {respuesta.status_code}"
        except Exception as e:
            return f"Error: {str(e)}"

# Definición del actor para manejar la conexión y el envío de resultados
class ClientRequestActor(pykka.ThreadingActor):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.results = {}
        self.requests_count = 0

    def on_receive(self, mensaje):
        if isinstance(mensaje, dict) and mensaje.get('type') == 'scrape_requests':
            requests_list = mensaje.get('requests')
            self.requests_count = len(requests_list)
            for idx, request in enumerate(requests_list):
                query = request.get('query')
                url_producto = f"https://listado.mercadolibre.com.ar/{query}#D[A:{query}]"
                scraper = ScraperMercadoLibre.start()
                scraper.tell({'url': url_producto, 'result_handler': self.actor_ref.proxy().result_handler(idx), 'idx': idx})

    def result_handler(self, idx):
        class ResultHandler(pykka.ThreadingActor):
            def __init__(self, parent_actor, idx):
                super().__init__()
                self.parent_actor = parent_actor
                self.idx = idx

            def on_receive(self, mensaje):
                idx = mensaje.get('idx')
                result = mensaje.get('result')
                self.parent_actor.results[idx] = result
                if len(self.parent_actor.results) == self.parent_actor.requests_count:
                    final_result = "\n\n".join(f"Request {idx + 1}:\n{result}" for idx, result in sorted(self.parent_actor.results.items()))
                    try:
                        self.parent_actor.connection.sendall(final_result.encode())
                    except Exception as e:
                        print(f"Error al enviar resultados al cliente: {e}")
                    finally:
                        try:
                            self.parent_actor.connection.close()
                        except Exception as e:
                            print(f"Error al cerrar la conexión: {e}")
        
        return ResultHandler(self, idx).start()

# Definición del actor del servidor
class ServerActor(pykka.ThreadingActor):
    def on_receive(self, mensaje):
        if isinstance(mensaje, dict) and mensaje.get('type') == 'handle_connection':
            conn = mensaje.get('connection')
            client_request_actor = ClientRequestActor.start(conn)
            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode()
                    if message.startswith('scrape'):
                        queries = message[len('scrape '):].split(',')
                        requests = [{'query': query.strip()} for query in queries]
                        client_request_actor.tell({'type': 'scrape_requests', 'requests': requests})
                except Exception as e:
                    print(f"Error en la recepción de datos: {e}")
                    break
            conn.close()

# Servidor TCP/IP
def start_server():
    host = '192.168.1.15'
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
            server_actor.tell({'type': 'handle_connection', 'connection': conn})

        client_thread = threading.Thread(target=handle_client, args=(conn,))
        client_thread.start()

if __name__ == '__main__':
    start_server()
