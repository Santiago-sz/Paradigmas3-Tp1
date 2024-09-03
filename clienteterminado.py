import socket

def start_client():
    host = '192.168.1.15'
    port = 8786

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Enviar comando para realizar scraping
    queries = "televisores, celulares"  # Consulta para buscar diferentes productos
    print(f"Enviando consulta al servidor: scrape {queries}")  # Mensaje de depuración
    client_socket.sendall(f"scrape {queries}".encode())

    # Recibir el resultado del scraping
    result = b""
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        result += data

    # Mostrar el resultado
    print(f"Resultado del servidor:\n{result.decode()}")

    client_socket.close()

if __name__ == '__main__':
    start_client()