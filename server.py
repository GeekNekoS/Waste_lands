import socket

SERVER_HOST = '0.0.0.0'  # Указываем адрес, на котором будет слушать сервер (0.0.0.0 означает все доступные интерфейсы)
SERVER_PORT = 8889  # Порт, на котором будет запущен сервер


def start_server():
    # Создаем сокет
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Привязываем сокет к адресу и порту
        server_socket.bind((SERVER_HOST, SERVER_PORT))
        print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

        # Ожидаем входящее соединение
        server_socket.listen(1)

        # Принимаем входящее соединение
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        # Получаем данные от клиента и отправляем ответ
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Received data: {data.decode()}")
            client_socket.sendall("Data received".encode())

    except KeyboardInterrupt:
        print("Server stopped.")

    finally:
        # Закрываем соединение и сокет
        client_socket.close()
        server_socket.close()


if __name__ == "__main__":
    start_server()
