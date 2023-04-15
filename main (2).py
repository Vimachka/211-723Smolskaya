import socket
import sys
import threading

def read_message(sock):
    """
    Handler for messages from server.
    """
    # Бесконечный цикл для чтения сообщений от сервера
    while True:
        try:
            buf = sock.recv(1024)
        except socket.error as e:
            # В случае ошибки выводим сообщение и выходим из цикла
            print("Exception caught: ", e)
            break

        if not buf:
            # Если длина буфера равна 0, то соединение разорвано и выходим из цикла
            print("Server disconnected.")
            break

        # Декодируем байты в текст без символа переноса строки
        message = buf.decode().rstrip()
        print("Received message:", message)

def on_online_command(sock):
    """
    Handler for "online" command.
    """
    try:
        # Отправляем серверу запрос на получение списка пользователей онлайн
        sock.sendall("online\n".encode())
        data = sock.recv(1024)
        # Выводим полученные данные на экран
        print("Online users:\n" + data.decode())
    except Exception as e:
        # В случае ошибки выводим сообщение
        print("Exception caught: ", e)

def main(argv):
    try:
        if len(argv) != 3:
            # Если количество аргументов командной строки не равно 3, то выводим сообщение об использовании и выходим
            print(f"Usage: {argv[0]} <host> <port>")
            return

        # Создаем объект сокета и подключаемся к серверу по указанному хосту и порту
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((argv[1], int(argv[2])))

        print(f"Connected to {argv[1]}:{argv[2]}")

        # Создаем поток для чтения сообщений от сервера
        read_message_thread = threading.Thread(target=read_message, args=(sock,))
        read_message_thread.daemon = True
        read_message_thread.start()

        # Бесконечный цикл для обработки введенных команд
        while True:
            try:
                # Получаем введенную команду от пользователя
                command = input()

                if command.startswith("send "):
                    # Если команда начинается с "send ", то отправляем сообщение указанному получателю
                    parts = command.split(" ", 2)
                    if len(parts) == 3:
                        recipientId = parts[1]
                        message = parts[2]

                        fullMessage = f"send {recipientId} {message}\n"
                        sock.sendall(fullMessage.encode())
                    else:
                        print("Invalid send command format.")
                elif command.startswith("online"):
                    # Если команда начинается с "online", то запрашиваем список пользователей онлайн
                    on_online_command(sock)
                else:
                    # Если команда не начинается с "send " или "online", то отправляем ее на сервер
                    sock.sendall(f"{command}\n".encode())
            except Exception as e:
                # В случае ошибки выводим сообщение и выходим из цикла
                print("Exception caught: ", e)
                break

        sock.close()
    except Exception as e:
        # В случае ошибки выводим сообщение
        print("Exception caught: ", e)

if __name__ == "__main__":
    main(sys.argv)
