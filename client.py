import socket
import os
import struct

def main():
    client_socket = socket.socket()
    client_socket.connect(('localhost', 9090))

    path = os.getcwd()

    path_length = len(path)
    client_socket.sendall(struct.pack('i', path_length))

    client_socket.sendall(path.encode())

    data = client_socket.recv(struct.calcsize('i'))
    size, = struct.unpack('i', data)
    result_data = ''
    while len(result_data) < size:
        tmp = client_socket.recv(1024).decode()
        if not tmp:
            break
        result_data += tmp


    client_socket.close()

    print(result_data)  # содержание директории в формате json объекта
    # Вывод: [{"Path": "C:\\Users\\danya\\Downloads\\Folder\\book.txt", "Last modified": "29.02.24 19:21:13",
    # "Size": "11424 bytes", "Object type": " File"}, {"Path": "C:\\ .......}]


if __name__ == '__main__':
    main()
