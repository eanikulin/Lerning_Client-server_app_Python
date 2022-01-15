from server import process_client_msg
import unittest
import yaml

with open('config.yaml', encoding='utf-8') as conf_file:
    data = yaml.load(conf_file, Loader=yaml.FullLoader)

ACTION_GOOD = data['PRESENCE']
USER_GOOD = 'Evgeny'
RESPONSE_GOOD = {data['RESPONSE']: 200}
PORT = data['DEFAULT_PORT']
TIME = 1.1

USER_BAD = 'Igor'
RESPONSE_BAD = {
    data['RESPONSE']: 400,
    data['ERROR']: 'Алерт! Ошибка'
}

class TestServer(unittest.TestCase):

    def test_process_client_msg_not_port(self):
        # Тест ответа на сообщение клиента без параметра port
        client_message = {
            data['ACTION']: ACTION_GOOD,
            data['TIME']: TIME,
            data['USER']: {
                data['ACCOUNT_NAME']: USER_BAD
            }
        }
        self.assertEqual(process_client_msg(client_message), RESPONSE_BAD)

    def test_process_client_msg_port(self):
        # Тест ответа на сообщение клиента c некорректным портом
        client_message = {
            data['ACTION']: ACTION_GOOD,
            data['TIME']: TIME,
            data['PORT']: 8080,
            data['USER']: {
                data['ACCOUNT_NAME']: USER_BAD
            }
        }
        self.assertEqual(process_client_msg(client_message), RESPONSE_BAD)

if __name__ == '__main__':
    unittest.main()