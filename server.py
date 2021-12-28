import argparse
import json
import time
from socket import socket, AF_INET, SOCK_STREAM

parser = argparse.ArgumentParser(description='Server connection setting')
parser.add_argument('-addr', type=str, default='', help='Server connection IP')
parser.add_argument('-port', type=int, default=7777, help='Server connection port')
args = parser.parse_args()

msg_response = {
    "response": '200',
    "time": time.ctime(time.time())
}

socket_server = socket(AF_INET, SOCK_STREAM)
socket_server.bind((args.addr, args.port))
socket_server.listen(5)
print(f"Сервер запущен на порту: {args.port}")


def send_msg(msg):
    message = json.dumps(msg)
    while True:
        client, addr = socket_server.accept()
        data = client.recv(1000000).decode('utf-8')
        data = json.loads(data)
        print(
            f"Сообщение от клиента: Код: {data['action']}, было отправлено клиентом {data['user']['account_name']} c адресом: {addr}")
        client.send(message.encode('utf-8'))
        client.close()


print(send_msg(msg_response))
