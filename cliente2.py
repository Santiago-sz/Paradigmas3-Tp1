import socket

def send_scrape_request(host, port, requests):
    try:
        # Crear un socket TCP/IP
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Formatear la solicitud de scraping
        message = 'scrape ' + ','.join([f"{req['page']}:{req['query']}" for req in requests])
        client_socket.sendall(message.encode())

        # Recibir la respuesta del servidor
        response = b""
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            response += data

        print("Respuesta del servidor:")
        print(response.decode())

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client_socket.close()

if _name_ == '_main_':  # Corregido el nombre del módulo principal
    host = '192.168.0.123'  # Dirección IP del servidor
    port = 8786  # Puerto del servidor

    # Ejemplo de solicitudes de scraping
    requests = [
        {'page': 'ml', 'query': 'laptop'},
        {'page': 'fv', 'query': 'smartphone'},
        {'page': 'mm', 'query': 'televisor'}
    ]

    send_scrape_request(host, port, requests);