import socket
import struct

# установка соединения с сервером программы 1
def connect_to_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(("localhost", 9091))
    return server_socket

# отправка команды на сервер
def send_command(server_socket, command):
    server_socket.send(command.encode())
    data = server_socket.recv(struct.calcsize('I'))
    size, = struct.unpack('I', data)
    response = ''
    while len(response) < size:
        tmp = server_socket.recv(1024).decode()
        if not tmp:
            break
        response += tmp
    return response

# добавление программы
def add_program(server_socket, program):
    command = f"add {program}"
    send_command(server_socket, command)

# получение файла для программы
def get_program_file(server_socket, program):
    command = f"get_file {program}"
    return send_command(server_socket, command)

# соединение с сервером и взаимодействие
def main():
    server_socket = connect_to_server()
    while True:
        command = input("Введите команду ('add' <program> или 'get_file' <program> или 'exit'): ")
        if command.lower() == "exit":
            break
        elif "add" in command:
            program = command.split("add ")[-1]
            add_program(server_socket, program)
            print("Команда успешно добавлена.")
        elif "get_file" in command:
            program = command.split("get_file ")[-1]
            output = get_program_file(server_socket, program)
            print(output)
        else:
            print("Неизвестная команда.")
    server_socket.close()

if __name__ == "__main__":
    main()