# ИМПОРТ БИБЛИОТЕК
import re
from num2words import num2words

# КОНЕЦ ИМПОРТА БИБЛИОТЕК

# НАЧАЛО РАБОТЫ С ДАННЫМИ
digits_dict = {'ноль': 0, 'один': 1, 'два': 2, 'три': 3, 'четыре': 4, 'пять': 5, 'шесть': 6, 'семь': 7, 'восемь'
: 8, 'девять': 9, 'десять': 10, 'одиннадцать': 11, 'двенадцать': 12, 'тринадцать': 13, 'четырнадцать':
                   14, 'пятнадцать': 15, 'шестнадцать': 16, 'семнадцать': 17, 'восемнадцать': 18, 'девятнадцать': 19,
               'двадцать': 20, 'тридцать': 30, 'сорок': 40, 'пятьдесят': 50, 'шестьдесят': 60, 'семьдесят': 70,
               'восемьдесят':
                   80, 'девяносто': 90, 'сто': 100}
operation_dict = ['плюс', 'минус', 'умножить', 'разделить на']

adot_dict = {'одна десятая': 0.1, 'одна сотая': 0.01, 'одна тысячная': 0.001, 'одна десятитысячная': 0.0001,
             'одна стотысячная': 0.00001, 'одна миллионная': 0.000001}
adot_usual = {1: 'десятых', 2: 'сотых', 3: 'тысячных', 4: 'десятитысячных', 5: 'стотысячных', 6: 'миллионных'}

small_nums = ['ноль', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять']
big_nums = ['двадцать', 'тридцать', 'сорок', 'пятьдесят', 'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто']

eror_dict = ['десять', 'одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать', 'пятнадцать', 'шестнадцать',
             'семнадцать', 'восемнадцать', 'девятнадцать']  # СПИСОК ДЛЯ ПРОВЕРКИ


# КОНЕЦ РАБОТЫ С ДАННЫМИ

# ФУНКЦИЯ ДЕЛЕНИЯ

def division(numerator, denominator):
    if (numerator % denominator == 0):
        ans = str(numerator // denominator)
        return ans
    else:
        ans = str(numerator // denominator) + "."
        l = {}
        index = 0
        numerator = numerator % denominator
        l[numerator] = index
        flag = False
        while flag == False:
            if numerator == 0:
                break
            digit = numerator * 10 // denominator
            numerator = numerator * 10 - (numerator * 10 // denominator) * denominator
            if numerator not in l:
                ans += str(digit)
                index += 1
                l[numerator] = index
                flag = False
            else:
                ans += str(digit) + ")"
                ans = ans[:l.get(numerator) + len(ans[:ans.index(".") + 1])] + "(" + ans[l.get(numerator) + len(
                    ans[:ans.index(".") + 1]):]
                flag = True
        return ans


# ФУНКЦИЯ ДЕЛЕНИЯ
def usual_number(current_num):
    match = re.search(' ', current_num[0])  # ПРОВЕРКА НА СОСТАВНОЕ ЧИСЛО 1
    if match:
        current_num = current_num[0].split(' ')
        for string in eror_dict:
            if string == current_num[0] or string == current_num[1]:
                return -1

        first_flag = 0
        second_flag = 0
        for string in small_nums:
            if string == current_num[1]:
                first_flag += 1
        for string in big_nums:
            if string == current_num[0]:
                second_flag += 1

        if first_flag == 0 or second_flag == 0:
            return -1

        current_num = digits_dict[current_num[0]] + digits_dict[current_num[1]]
    else:
        current_num = digits_dict[current_num[0]]
    return current_num

def calc(main_str):  # ФУНКЦИЯ КАЛЬКУЛЯТОР, ЕСЛИ ВЫВОДИТСЯ ОТВЕТ "-1" - следовательно что-то сделано неверно!
####вСЕ ЕЩЕ НУЖНО СДЕЛАТЬ ПРОВЕРКУ ОБЯЗАТЕЛЬНО МОЛЮ СДЕЛАЙТЕ
    if not main_str:
        return -1
    current_operation = 'error'
    for string in operation_dict:  # ПОИСК ОПЕРАЦИИ В СТРОКЕ
        match = re.search(string, main_str)
        if match:
            current_operation = string  # ОПЕРАЦИЯ
    if current_operation == 'error':
        return -1

    tokens = main_str.split(' ' + current_operation + ' ')  # ДЕЛИМ ЧИСЛО УДАЛЯЯ ОПЕРАЦИЮ
    first_num, second_num = tokens[:-1], tokens[-1:]


    first_num = usual_number(first_num)
    second_num = usual_number(second_num)




    if first_num == -1 or second_num == -1:  #ПРОВЕРКА НА ОШИБКИ
        return -1

    if current_operation == "плюс":
        ans = first_num + second_num
    elif current_operation == "умножить" or current_operation == "умножит на":
        ans = first_num * second_num
    elif current_operation == "минус":
        ans = first_num - second_num
    elif current_operation == "разделить на" or current_operation == "поделить на":
        ans = division(first_num, second_num)
    print(ans)
    ans = str(ans)


    match = re.search('\.', ans)  #ПРОВЕРКА НА НАЛИЧИЕ ТОЧКИ
    if match:
        ans = ans.split('.')
        print(ans)
        before_dot = num2words(ans[1], lang='ru')
        after_dot = ans[2]
        match = re.search('\(\W\)', ans)
        if match:
            after_dot = after_dot
        else:
            rank_10 = adot_usual(len(after_dot))
            for i in after_dot:
                if i == '0':
                    after_dot = after_dot[1:]
                else:
                    break
            after_dot = num2words(int(after_dot), lang='ru')

            ans = before_dot + ' и ' + after_dot + rank_10


    else:       #ЕСЛИ ОБЫЧНОЕ ЧИСЛО
        ans = num2words(ans, lang='ru')

    #ЗДЕСЬ НУЖНО СДЕЛАТЬ ПРОВЕРКУ НА ПЕРИОДИЧНОСТЬ, ЕСЛИ ПЕРИОД ЕСТЬ - ВЫОДИМ ПО-ОСОБОМУ
    #ДАЛЬШЕ ДЕЛАЕМ ПРОВЕРКУ НА ЧИСЛО С ТОЧКОЙ МЕЖДУ ЧИСЛАМИ, ВКЛЮЧЕНО В ПРОВЕРКУ НА ВЫВОДЕ
    #СНАЧАЛА ПРОВЕРЯЕМ НА НАЛИЧИЕ ТОЧКИ(ДЕСЯТИЧНОСТЬ ТИПА) ПОТОМ ПРОВЕРЯЕМ НА НАЛИЧИЕ ПЕРИОДА(Т.Е. СКОБОК)3,3
    return ans


flag = True
while flag:
    line_main = input('Введите выражение: ')
    line_main = line_main.lower()

    ans = calc(line_main)
    if ans != -1:
        print('Ответ =', ans)
        flag = False
    else:
        flag = True
        print('Вы ввели неверное выражение!')

