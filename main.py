#ИМПОРТ БИБЛИОТЕК
import re
from num2words import num2words
#КОНЕЦ ИМПОРТА БИБЛИОТЕК

#НАЧАЛО РАБОТЫ С ДАННЫМИ
digits_dict = {'ноль': 0,'один': 1,'два': 2,'три': 3, 'четыре': 4, 'пять': 5, 'шесть': 6, 'семь': 7,'восемь'
                  :8, 'девять': 9,'десять':10, 'одиннадцать': 11, 'двенадцать': 12, 'тринадцать': 13, 'четырнадцать':
                  14,'пятнадцать': 15, 'шестнадцать': 16, 'семнадцать': 17, 'восемнадцать': 18, 'девятнадцать':19,
                  'двадцать': 20,'тридцать': 30,'сорок': 40,'пятьдесят': 50, 'шестьдесят': 60, 'семьдесят': 70, 'восемьдесят':
                  80, 'девяносто': 90}
operation_dict = ['плюс', 'минус', 'умножить']
#КОНЕЦ РАБОТЫ С ДАННЫМИ


###НУЖНО ОБЯЗАТЕЛЬНО СДЕЛАТЬ ПРОВЕРКУ ВВЕЛ ЛИ ПОЛЬЗОВАТЕЛЬ ЧИСЛА В ВИДЕ "ПЯТНАДЦАТЬ ПЯТЬ ПЛЮС ОДИН" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

def calc(main_str):

	#ЗДЕСЬ КОГДА ТО БУДЕТ ПРОВЕРКА
	#
	#РЕАЛЬНО БУДЕТ
	for string in operation_dict:   #ПОИСК ОПЕРАЦИИ В СТРОКЕ
		match = re.search(string, main_str)
		if match:
			current_operation = string   #ОПЕРАЦИЯ


	tokens = main_str.split(' ' + current_operation + ' ')   #ДЕЛИМ ЧИСЛО УДАЛЯЯ ОПЕРАЦИЮ
	first_num, second_num = tokens[:-1], tokens[-1:]


	match = re.search(' ', first_num[0])    #ПРОВЕРКА НА СОСТАВНОЕ ЧИСЛО 1
	if match:
		first_num = first_num[0].split(' ')
		first_num = digits_dict[first_num[0]] + digits_dict[first_num[1]]
	else:
		first_num = digits_dict[first_num[0]]

	match = re.search(' ', second_num[0])  #ПРОВЕРКА НА СОСТАВНОЕ ЧИСЛО 2
	if match:
		second_num = second_num[0].split(' ')
		second_num = digits_dict[second_num[0]] + digits_dict[second_num[1]]
	else:
		second_num= digits_dict[second_num[0]]




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

