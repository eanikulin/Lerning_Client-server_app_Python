# server

import socket
import sys
import json
import argparse
import yaml
import logs.server_logs_config
from decors import Log
from utils import get_message, send_message
import logging
from collections import deque
import time
import select

with open('config.yaml', encoding='utf-8') as conf_file:
    data = yaml.load(conf_file, Loader=yaml.FullLoader)

log_server = logging.getLogger('server')


@Log(log_server)
def process_client_msg(client_message, messages_list, client):
    if data['ACTION'] in client_message and data['TIME'] in client_message and data['USER'] in client_message and data['PORT'] in client_message:
        if client_message[data['ACTION']] == data['PRESENCE'] and client_message[data['USER']][data['ACCOUNT_NAME']] == 'Evgeny':
            send_message(client, {data['RESPONSE']: 200})
            return
        if client_message[data['ACTION']] == data['MESSAGE'] and data['MESSAGE_TEXT'] in client_message:
            messages_list.append((client_message[data['USER']][data['ACCOUNT_NAME']], client_message[data['MESSAGE_TEXT']]))
            return
    send_message(client,
                 {
                     data['RESPOND_FAULT_IP_ADDRESS']: 400,
                     data['ERROR']: 'Bad Request'
                 })
    return
# @Log(log_server)
# def process_client_msg(client_message):
#     if data['ACTION'] in client_message and client_message[data['ACTION']] == data['PRESENCE'] and data[
#         'TIME'] in client_message \
#             and data['USER'] in client_message and client_message[data['USER']][data['ACCOUNT_NAME']] == 'Evgeny':
#         return {data['RESPONSE']: 200}
#     return {
#         data['RESPOND_FAULT_IP_ADDRESS']: 400,
#         data['ERROR']: 'Bad Request'
#     }


def server_main():
    print('Сервер запущен')
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-p', type=int, default=data['DEFAULT_PORT'])
    arg_parser.add_argument('-a', type=str, default='')
    args = arg_parser.parse_args()

    try:
        listen_port = args.p
        if not (1024 < listen_port < 65535):
            raise ValueError
    except ValueError:
        # print(
        #     'В качастве порта может быть указано только число в диапазоне от 1024 до 65535.')
        log_server.critical(f'Ошибка порта {args.listen_port}: Недопустимое значение')
        sys.exit(1)

    address_listen = args.a

    clients_list = []

    messages_deque = deque()

    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((address_listen, listen_port))
    transport.settimeout(0.2)

    transport.listen(data['MAX_CONNECTIONS'])
    log_server.info(f'Сервер запущен. Порт : {listen_port}, адрес: {address_listen}')

    while True:
        try:
            client, client_address = transport.accept()
        except OSError:
            pass
        else:
            log_server.info(f'Установлено соедение с клиентом {client_address}')
            clients_list.append(client)

        receive_data_list = []
        send_data_list = []
        errors_list = []

        try:
            if clients_list:
                receive_data_list, send_data_list, errors_list = select.select(clients_list, clients_list, [], 0)
        except OSError:
            pass

        for client_with_message in receive_data_list:
            try:
                process_client_msg(get_message(client_with_message), messages_deque, client_with_message)
            except Exception:
                log_server.info(f'Клиент {client_with_message.getpeername()} ')
                clients_list.remove(client_with_message)

        if messages_deque and send_data_list:
            message_data = messages_deque.popleft()
            message = {
                data['ACTION']: data['MESSAGE'],
                data['SENDER']: message_data[0],
                data['TIME']: time.time(),
                data['MESSAGE_TEXT']: message_data[1]
            }

            for waiting_client in send_data_list:
                try:
                    send_message(waiting_client, message)
                except Exception:
                    log_server.info(f'Клиент {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients_list.remove(waiting_client)


if __name__ == '__main__':
    server_main()


        # client, client_address = transport.accept()
        # log_server.info(f'Соединение установлено с - {client_address}')
        # try:
        #     message_from_client = get_message(client)
        #     print(message_from_client)
        #     response = process_client_msg(message_from_client)
        #     send_message(client, response)
        #     client.close()
        # except (ValueError, json.JSONDecodeError):
        #     # print('Принято некорретное сообщение от клиента.')
        #     log_server.error(f'Не удалось декодировать сообщение от клиента {client_address}.')
        #     client.close()
