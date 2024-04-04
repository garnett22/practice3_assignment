import os
import time
import json
import subprocess
import asyncio
from asyncio import StreamReader, StreamWriter
import struct
import threading

programs = ["echo 1", "hostname"]  # список программ

def create_folders(programs):
    for program in programs:
        folder_name = program  # имя папки
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

# запуск программ
def run_programs(programs):
    for program in programs:
        folder_name = program
        file_name = f"{folder_name}/output.txt"  # имя файла
        with open(file_name, "a") as file:
            subprocess.run(program, stdout=file, shell=True)

# запись в JSON
def write_to_json(programs):
    data = {"programs": programs}
    with open("data.json", "w") as json_file:
        json.dump(data, json_file)

def load_from_json():
    try:
        with open("data.json", "r") as json_file:
            data = json.load(json_file)
            return data["programs"]
    except FileNotFoundError:
        return ''

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

async def handle_client1(reader: StreamReader, writer: StreamWriter):
    path_length = struct.unpack('i', await reader.read(struct.calcsize('i')))[0]
    path = (await reader.read(path_length)).decode()
    result = traversal(path)
    result_length = len(json.dumps(result))

    writer.write(struct.pack('i', result_length))
    await writer.drain()
    writer.write(json.dumps(result).encode())
    await writer.drain()
    await writer.wait_closed()


async def start_server():
    server_socket1 = await asyncio.start_server(handle_client1, "localhost", 9090)
    print("Ожидание первого клиента")

    server_socket2 = await asyncio.start_server(handle_client2, "localhost", 9091)
    print("Ожидание второго клиента")

    async with server_socket1, server_socket2:
        await server_socket1.serve_forever()
        await server_socket2.serve_forever()

write_to_json(programs)
asyncio.run(start_server())
