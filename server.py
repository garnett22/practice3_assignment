import os
import time
import json
import socket
import struct

def traversal(path):
    traversal_result = []
    for path, directories, files in list(os.walk(path)):
        for file in files:
            file_path = os.path.join(path, file)
            time_modified = os.path.getmtime(file_path)
            local_time = time.localtime(time_modified)
            result_time = time.strftime('%d.%m.%y %H:%M:%S', local_time)
            size = str(os.path.getsize(file_path)) + ' bytes'
            file_info = {
                'Path': file_path,
                'Last modified': result_time,
                'Size': size,
                'Object type': ' File'
            }
            traversal_result.append(file_info)

        for directory in directories:
            dir_path = os.path.join(path, directory)
            time_modified = os.path.getmtime(dir_path)
            local_time = time.localtime(time_modified)
            result_time = time.strftime('%d.%m.%y %H:%M:%S', local_time)
            dir_info = {
                'Path': dir_path,
                'Last modified': result_time,
                'Object type': 'Directory'
            }
            traversal_result.append(dir_info)

    return traversal_result




def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 9090
    sock.bind((host, port))
    sock.listen(3)

    connection, client_address = sock.accept()
    with connection:
        data = connection.recv(struct.calcsize('i'))
        path_length, = struct.unpack('i', data)
        path = connection.recv(path_length).decode()
        result = traversal(path)
        result_length = len(json.dumps(result))

        connection.sendall(struct.pack('i', result_length))
        connection.sendall(json.dumps(result).encode())


if __name__ == '__main__':
    main()
