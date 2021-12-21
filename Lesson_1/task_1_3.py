# Кириллические символы нельзя записать в байтовом виде, можно применить encode

str1 = b'attribute'
str2 = 'класс'.encode('utf-8')
str3 = 'функция'.encode('utf-8')
str4 = b'type'

print(type(str1), type(str2), type(str3), type(str3))
print(str1, str2, str3, str4)
