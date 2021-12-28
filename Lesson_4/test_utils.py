import yaml
from utils import get_message
import sys
import os
import unittest
import json
sys.path.append(os.path.join(os.getcwd(), '..'))

with open('config.yaml', encoding='utf-8') as conf_file:
    data = yaml.load(conf_file, Loader=yaml.FullLoader)


class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.received_message = None

    def recv(self, max_len):
        #   Получаем данные из сокета
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(data['ENCODING'])


class TestUtils(unittest.TestCase):
    #   Тестовый класс, собственно выполняющий тестирование.
    test_dict_send = {
        data['ACTION']: data['PRESENCE'],
        data['TIME']: 111111.111111,
        data['USER']: {
            data['ACCOUNT_NAME']: 'Sergey'
        }
    }
    test_dict_recv_ok = {data['RESPONSE']: 200}
    test_dict_recv_err = {
        data['RESPONSE']: 400,
        data['ERROR']: 'Bad Request'
    }

    def test_get_message(self):
        #   Тест функции приёма сообщения
        test_sock_ok = TestSocket(self.test_dict_recv_ok)
        test_sock_err = TestSocket(self.test_dict_recv_err)
        # тест корректной расшифровки корректного словаря
        self.assertEqual(get_message(test_sock_ok), self.test_dict_recv_ok)
        # тест корректной расшифровки ошибочного словаря
        self.assertEqual(get_message(test_sock_err), self.test_dict_recv_err)


if __name__ == '__main__':
    unittest.main()
