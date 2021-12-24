import argparse
import json
import time
from socket import socket, AF_INET, SOCK_STREAM

parser = argparse.ArgumentParser(description='Server connection setting')
parser.add_argument('addr', type=str, help='Server connection IP')
parser.add_argument('-port', type=int, default=7777, help='Server connection port')
args = parser.parse_args()

client_msg = {"action": "presence",
              "time": f"{time.ctime(time.time())}",
              "type": "status",
              "user": {
                  "account_name": "Evgeny",
                  "status": "Yep, I am here!"
              }
              }

socket_client = socket(AF_INET, SOCK_STREAM)
socket_client.connect((args.addr, args.port))


def send_msg(msg):
    message = json.dumps(msg)
    socket_client.send(message.encode('utf-8'))
    data = socket_client.recv(1000000).decode('utf-8')
    data = json.loads(data)
    socket_client.close()
    return f"Сообщение от сервера: Код: {data['response']}, время ответа сервера: {data['time']}"


print(send_msg(client_msg))
