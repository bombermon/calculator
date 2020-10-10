#ИМПОРТ БИБЛИОТЕК
import re
from num2words import num2words
#КОНЕЦ ИМПОРТА БИБЛИОТЕК

#КОД СЛОВАМИ
#СНАЧАЛА ПИШЕМ СЛОВАРИ С ЦИФРАМИ
#РАБОТА СО СТРОКАМИ: ПЕРВЫМ ДЕЛОМ ДЕЛИМ СТРОКУ ПО ПРОБЕЛАМ
#ВТОРЫМ ДЕЛОМ СОЕДИНЯЕМ ЧИСЛА ДО И ПОСЛЕ ЗНАКА ОПЕРАЦИИ и записываем операцию в переменную Operation
#ИМЕЕМ ПЕРЕМЕННЫЕ first_number и second_number, в которых есть числа, с которыми работаем
#ПРОИЗВОДИМ ОПЕРАЦИЮ В ЗАВИСИМОСТИ ОТ ПЕРЕМЕННОЙ Operation И ЗАПИСЫВАЕМ РЕЗУЛЬТАТ В ПЕРЕМЕННУЮ ANS
#ОБРАЩАЕМСЯ К ПЕРЕМЕННОЙ ANS И К СЛОВАРЮ, ПЕРЕВОДЯ ЧИСЛО В ТЕКСТОВЫЙ ФОРМАТ

digits_dict = {'ноль': 0,'один': 1,'два': 2,'три': 3, 'четыре': 4, 'пять': 5, 'шесть': 6, 'семь': 7,'восемь'
                  :8, 'девять': 9,'десять':10, 'одиннадцать': 11, 'двенадцать': 12, 'тринадцать': 13, 'четырнадцать':
                  14,'пятнадцать': 15, 'шестнадцать': 16, 'семнадцать': 17, 'восемнадцать': 18, 'девятнадцать':19,
                  'двадцать': 20,'тридцать': 30,'сорок': 40,'пятьдесят': 50, 'шестьдесят': 60, 'семьдесят': 70, 'восемьдесят':
                  80, 'девяносто': 90}
operation_dict = ['плюс', 'минус', 'умножить']



def calc(main_str):

	#ЗДЕСЬ КОГДА ТО БУДЕТ ПРОВЕРКА
	#
	#РЕАЛЬНО БУДЕТ
	for string in operation_dict:
		match = re.search(string, main_str)
		if match:
			print('Найдено "{}" в "{}"'.format(string, main_str))
			text_pos = match.span()
			print(main_str[match.start():match.end()])
			current_operation = string
		else:
			print('Не найдено "{}"'.format(string))

	tokens = main_str.split(' ' + current_operation + ' ')
	first_num, second_num = tokens[:-1], tokens[-1:]
	print(first_num,' ',second_num)



#    if (main_str.index('плюс') == 2) or (main_str.index('умножить') == 2) or (main_str.index('минус') == 2):
 #   	first_number = main_str[0]+main_str[1]
  #  	if(len(main_str) = )
   # elif (main_str.index('плюс') == 1) or (main_str.index('умножить') == 1) or (main_str.index('минус') == 1):


	if current_operation == "плюс":
		ans = first_num + second_num
	elif current_operation == "умножить":
		ans = first_num * second_num
	elif current_operation == "минус":
		ans = first_num - second_num

	ans = num2words(ans, lang='ru')
	return ans

line_main = input('Введите выражение: ')
line_main = line_main.lower()

ans = calc(line_main)

print(ans)

