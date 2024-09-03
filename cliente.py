import socket

def start_client():
    host = '172.17.3.125'
    port = 8786

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Enviar comando para realizar scraping
    queries = "televisores, celulares"  # Consulta para buscar diferentes productos
    print(f"Enviando consulta al servidor: scrape {queries}")
    client_socket.sendall(f"scrape {queries}".encode())

    # Recibir el resultado del scraping
    result = b""
    try:
        while True:
            data = client_socket.recv(4096)
            if not data:
                break
            result += data
    except Exception as e:
        print(f"Error al recibir datos del servidor: {e}")
    finally:
        # Mostrar el resultado
        print(f"Resultado del servidor:\n{result.decode()}")
        client_socket.close()

if __name__ == '__main__':
    start_client()
