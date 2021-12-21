# a.	Создать функцию get_data(), в которой в цикле осуществляется перебор файлов с данными,
# их открытие и считывание данных. В этой функции из считанных данных необходимо с помощью
# регулярных выражений извлечь значения параметров «Изготовитель системы»,  «Название ОС»,
# «Код продукта», «Тип системы». Значения каждого параметра поместить в соответствующий список.
# Должно получиться четыре списка — например, os_prod_list, os_name_list, os_code_list, os_type_list.
# В этой же функции создать главный список для хранения данных отчета — например, main_data — и поместить
# в него названия столбцов отчета в виде списка: «Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
# Значения для этих столбцов также оформить в виде списка и поместить в файл main_data (также для каждого файла);

# b.	Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл. В этой функции реализовать получение
# данных через вызов функции get_data(), а также сохранение подготовленных данных в соответствующий CSV-файл;

import csv


def get_data(text_files):
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    for file in text_files:
        handle = open(f'{file}', encoding='windows-1251')
        for line in handle:
            if 'Изготовитель системы' in line:
                os_prod_list.append(line.replace("\n", "").replace("Изготовитель системы:             ", ""))
            elif 'Название ОС' in line:
                os_name_list.append(line.replace("\n", "").replace("Название ОС:                      ", ""))
            elif 'Код продукта' in line:
                os_code_list.append(line.replace("\n", "").replace("Код продукта:                     ", ""))
            elif 'Тип системы' in line:
                os_type_list.append(line.replace("\n", "").replace("Тип системы:                      ", ""))
        handle.close()

    for i in range(len(text_files)):
        main_data.append([
            os_prod_list[i],
            os_name_list[i],
            os_code_list[i],
            os_type_list[i]
        ])
    return main_data


def write_to_csv(file, data):
    with open(file, 'w') as csv_file:
        f_n_writer = csv.writer(csv_file)
        for new_row in data:
            f_n_writer.writerow(new_row)


res_list = get_data(['info_1.txt', 'info_2.txt', 'info_3.txt'])
write_to_csv('output_file.csv', get_data(['info_1.txt', 'info_2.txt', 'info_3.txt']))

with open('output_file.csv') as csv_file:
    print(csv_file.read())
