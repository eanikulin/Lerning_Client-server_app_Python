# client

import sys
import json
import socket
import time
import argparse
import yaml
import logs.client_logs_config
from decors import logs
# from decors import Log
import errors as errors_user
from utils import get_message, send_message
import logging

log_client = logging.getLogger('client')

with open('config.yaml', encoding='utf-8') as conf_file:
    data = yaml.load(conf_file, Loader=yaml.FullLoader)

CLIENT_MODE = {
    'send': 'sending messages',
    'listen': 'receiving messages'
}

@logs(log_client)
def create_presence_msg(message=None, action=data['PRESENCE'], port=data['DEFAULT_PORT'], acc_name='Evgeny'):
    message_output = {
        data['ACTION']: action,
        data['TIME']: time.time(),
        data['PORT']: port,
        data['USER']: {
            data['ACCOUNT_NAME']: acc_name
        }
    }
    if message and action == data['MESSAGE']:
        message_output[data['MESSAGE_TEXT']] = message
    return message_output

@logs(log_client)
def input_message(client_socket):
    while True:
        message = input('Введите сообщение для отправки (для выхода введите exit):')
        if message.strip():
            break
        else:
            print('Сообщение не может быть пустым!')
    if message == 'exit':
        client_socket.close()
        exit(0)
    return message

@logs(log_client)
def server_process_answer(message_server):
    if data['RESPONSE'] in message_server:
        if message_server[data["RESPONSE"]] == 200:
            log_client.info(f'Успешно 200 : OK')
            return '200 : OK'
        log_client.critical(f'Ошибка 400 {message_server[data["RESPONSE"]]}')
        return f'400 : {message_server[data["RESPONSE"]]}'
    log_client.critical(f'Ошибка: невверное значение')
    raise ValueError

@logs(log_client)
def message_from_server(server_message):
    if data['ACTION'] in server_message and server_message[data['ACTION']] == data['MESSAGE'] and data['SENDER'] in server_message \
            and data['MESSAGE_TEXT'] in server_message:
        print(f'Получено сообщение от пользователя {server_message[data["SENDER"]]}: {server_message[data["MESSAGE_TEXT"]]}')
        log_client.info(f'Получено сообщение от пользователя {server_message[data["SENDER"]]}:{server_message[data["MESSAGE_TEXT"]]}')
    else:
        log_client.error(f'Получено некорректное сообщение с сервера: {server_message}')


@logs(log_client)
def mainloop(client_mode, transport, server_address, server_port):
    print(f'Режим работы - {CLIENT_MODE[client_mode]}')
    while True:
        try:
            if client_mode == 'send':
                message = create_presence_msg(input_message(transport), data['MESSAGE'], server_port)
                send_message(transport, message)
                log_client.info(f'Отправлено сообщение {message["action"]} '
                              f'от пользователя {message[data["USER"]][data["ACCOUNT_NAME"]]}')
            elif client_mode == 'listen':
                message_from_server(get_message(transport))
        except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
            log_client.error(f'Соединение с сервером {server_address} было потеряно.')
            sys.exit(1)

def client_main():

    for_parse = argparse.ArgumentParser()
    for_parse.add_argument('port', nargs='?', type=int, default=data['DEFAULT_PORT'])
    for_parse.add_argument('address', nargs='?', type=str, default=data['DEFAULT_IP_ADDRESS'])
    for_parse.add_argument('-m', '--mode', type=str, default='send')

    args_parse = for_parse.parse_args()

    server_port = args_parse.port
    server_address = args_parse.address
    client_mode = args_parse.mode

    try:
        if not (1024 < server_port < 65535):
            raise errors_user.PortError
        if client_mode not in CLIENT_MODE:
            raise errors_user.ClientModeError
    except errors_user.PortError as port_error:
        log_client.critical(f'Ошибка порта {args_parse.server_port}: {port_error}. Завершение соединения...')
        sys.exit(1)
    except errors_user.ClientModeError as error:
        log_client.critical(f'Ошибка режима {server_port}: {error}. Завершение соединения...')
        sys.exit(1)

    trans_port = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    trans_port.connect((server_address, server_port))
    message_to_server = create_presence_msg(server_port)
    send_message(trans_port, message_to_server)
    log_client.info(f'Сообщение отправлено {message_to_server[data["ACTION"]]} '
                  f'от пользователя {message_to_server[data["USER"]][data["ACCOUNT_NAME"]]} '
                  f'для сервера {server_address}')
    try:
        answer = server_process_answer(get_message(trans_port))
        print(f"Ответ => {answer}")
    except json.JSONDecodeError:
        log_client.error(f'Не удалось декодировать сообщение сервера: {server_address}')
    except errors_user.IncorrectDataRecivedError as incorrect_data:
        log_client.error(f'Принято некорректное сообщение от удалённого компьютера. {server_address}: {incorrect_data}')
    except errors_user.NoResponseInServerMessageError as error:
        log_client.error(f'Ошибка сообщения сервера {server_address}: {error}')
    except ConnectionRefusedError:
        log_client.critical(f'Не удалось подключиться к серверу {server_address}:{server_port}')
        sys.exit(1)
    else:
        mainloop(client_mode, trans_port, server_address, server_port)


if __name__ == '__main__':
    client_main()
