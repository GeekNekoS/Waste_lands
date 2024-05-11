import socket

SERVER_HOST = 'localhost'  # Адрес сервера
SERVER_PORT = 8889  # Порт сервера


def connect_to_server():
    # Создаем сокет для клиента
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Подключаемся к серверу
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to server {SERVER_HOST}:{SERVER_PORT}")

        # Отправляем данные на сервер
        message = "Hello, server!"
        client_socket.sendall(message.encode())

        # Получаем ответ от сервера
        data = client_socket.recv(1024)
        print(f"Received from server: {data.decode()}")

    except Exception as e:
        print(f"Error connecting to server: {e}")

    finally:
        # Закрываем соединение
        client_socket.close()


if __name__ == "__main__":
    connect_to_server()
