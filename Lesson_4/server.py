# server

import socket
import sys
import json
import argparse
import yaml
from utils import get_message, send_message
import logging

with open('config.yaml', encoding='utf-8') as conf_file:
    data = yaml.load(conf_file, Loader=yaml.FullLoader)

log_server = logging.getLogger('server')


def process_client_msg(client_message):
    if data['ACTION'] in client_message and client_message[data['ACTION']] == data['PRESENCE'] and data[
        'TIME'] in client_message \
            and data['USER'] in client_message and client_message[data['USER']][data['ACCOUNT_NAME']] == 'Evgeny':
        return {data['RESPONSE']: 200}
    return {
        data['RESPOND_FAULT_IP_ADDRESS']: 400,
        data['ERROR']: 'Bad Request'
    }


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
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((address_listen, listen_port))
    transport.listen(data['MAX_CONNECTIONS'])
    log_server.info(f'Сервер запущен. Порт : {listen_port}, адрес: {address_listen}')

    while True:
        client, client_address = transport.accept()
        log_server.info(f'Соединение установлено с - {client_address}')
        try:
            message_from_client = get_message(client)
            print(message_from_client)
            response = process_client_msg(message_from_client)
            send_message(client, response)
            client.close()
        except (ValueError, json.JSONDecodeError):
            # print('Принято некорретное сообщение от клиента.')
            log_server.error(f'Не удалось декодировать сообщение от клиента {client_address}.')
            client.close()


if __name__ == '__main__':
    server_main()
