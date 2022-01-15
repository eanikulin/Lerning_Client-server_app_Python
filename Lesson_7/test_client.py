from client import server_process_answer
import unittest
import yaml
# import variables as variables

with open('config.yaml', encoding='utf-8') as conf_file:
    data = yaml.load(conf_file, Loader=yaml.FullLoader)

ACTION_GOOD = data['PRESENCE']
USER_GOOD = 'Evgeny'
TIME = 1.1
RESPONSE_GOOD = {data['RESPONSE']: 200}
PORT = data['DEFAULT_PORT']
MESSAGE_GOOD = '200 : OK'

USER_BAD = 'Igor'
MESSAGE_BAD = '400 : Bad Request'
RESPONSE_BAD = {data["ERROR"]: 'Bad Request'}
EXPECTED_EXCEPTION = ValueError


class TestClass(unittest.TestCase):

    def test_process_answer_good(self):
        #   Тест ответа сервера, статус 200
        self.assertEqual(server_process_answer(RESPONSE_GOOD), MESSAGE_GOOD)

    def test_process_answer_bad(self):
        #   Тест ответа сервера, статус 400
        self.assertEqual(server_process_answer(RESPONSE_BAD), MESSAGE_BAD)

    def test_process_answer_error(self):
        #   Тест исключение при ошибке от сервера
        self.assertRaises(EXPECTED_EXCEPTION, server_process_answer, RESPONSE_BAD)


if __name__ == '__main__':
    unittest.main()