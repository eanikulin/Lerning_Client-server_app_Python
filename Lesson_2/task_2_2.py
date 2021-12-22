# 2.	Задание на закрепление знаний по модулю json. Есть файл orders в формате JSON с информацией о заказах.
# Написать скрипт, автоматизирующий его заполнение данными. Для этого:

# a.	Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item),
# количество (quantity), цена (price), покупатель (buyer), дата (date).
# Функция должна предусматривать запись данных в виде словаря в файл orders.json.
# При записи данных указать величину отступа в 4 пробельных символа;

# b.	Проверить работу программы через вызов функции write_order_to_json()
# с передачей в нее значений каждого параметра.


import json


def write_order_to_json(item, quantity, price, buyer, date):
    my_dict = {'item':item, 'quantity':quantity, 'price':price, 'buyer':buyer, 'date':date}
    with open('orders.json') as json_file:
        data = json.load(json_file)
    data['orders'].append(my_dict)
    with open('orders.json', 'w', encoding='utf-8') as file_n:
        json.dump(data, file_n, indent=4, ensure_ascii=False)



write_order_to_json('молоко', 5, 352, 'Евгений', '12.12.2011')

with open('orders.json', encoding='utf-8') as f_n:
    print(f_n.read())
