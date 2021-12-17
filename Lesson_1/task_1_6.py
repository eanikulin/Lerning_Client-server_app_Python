import locale

def_encoding = locale.getpreferredencoding()
print(def_encoding)

with open('test_file.txt', 'r', encoding='UTF-8') as test_file:
    print(f'{test_file.encoding} - кодировка по умолчанию')
    for line in test_file:
        print(line)

with open('test_file.txt', 'r', encoding='cp1251') as test_file:
    print(f'{test_file.encoding} - кодировка по умолчанию')
    for line in test_file:
        print(line)
