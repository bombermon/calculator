# ИМПОРТ БИБЛИОТЕК
import re
from num2words import num2words

from googletrans import Translator
from word2number.w2n import word_to_num
from word2number import w2n

# КОНЕЦ ИМПОРТА БИБЛИОТЕК




# НАЧАЛО РАБОТЫ С ДАННЫМИ

operation_dict = ['плюс', 'минус', 'умножить', 'разделить на', 'поделить на', 'умножить на']

adot_dict = {'десятых': 0.1, 'сотых': 0.01, 'тысячных': 0.001, 'десятитысячных': 0.0001,
             'стотысячных': 0.00001, 'миллионных': 0.000001}

adot_usual = {1: 'десятых', 2: 'сотых', 3: 'тысячных', 4: 'десятитысячных', 5: 'стотысячных', 6: 'миллионных'}


# КОНЕЦ РАБОТЫ С ДАННЫМИ

#ПЕРЕВОД ЧИСЕЛ В
translator = Translator()
def translate_to_letter(word):

    second_rank = None
    for string in adot_dict:  # ПОИСК ОПЕРАЦИИ В СТРОКЕ
        match2 = re.search(string, word)
        if match2:
            second_rank = string
    main_letter_adot = ' '

    match = re.search(r' и ', word)
    if match:
        full_str = word.split(' и ')
        before_dot = translator.translate(full_str[0], src='ru', dest='en').text
        before_dot = w2n.word_to_num(before_dot)

        after_dot = full_str[1]

        if after_dot[-1] == ' ':
            after_dot = after_dot[:-1]

        after_dot = after_dot.split(' ')
        rank = after_dot[-1]
        del after_dot[-1]

        main_letter_adot = ' '.join(after_dot)

        main_letter_adot = translator.translate(main_letter_adot, src='ru', dest='en').text
        main_letter_adot = w2n.word_to_num(main_letter_adot)

        rank = adot_dict[rank]


        word = before_dot + main_letter_adot*rank
    elif(second_rank != None):

        if word[-1] == ' ':
            word = word[:-1]

        word = word.split(' ')
        rank = word[-1]
        del word[-1]


        main_letter_adot = ' '.join(word)


        main_letter_adot = translator.translate(main_letter_adot, src='ru', dest='en').text
        main_letter_adot = w2n.word_to_num(main_letter_adot)

        rank = adot_dict[rank]


        word =  main_letter_adot * rank
    else:

        word = translator.translate(word, src='ru', dest='en').text
        word = w2n.word_to_num(word)
    return word


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
    first_num, second_num = first_num[0] , second_num[0]


    first_num = translate_to_letter(first_num)
    second_num = translate_to_letter(second_num)


    if current_operation == "плюс":
        ans = first_num + second_num
    elif current_operation == "умножить" or current_operation == "умножить на":
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
        before_dot = num2words(ans[0], lang='ru')
        after_dot = ans[1]
        match = re.search(r'\(', ans)
        if match:
            after_dot_parts = re.split(r'\(', after_dot)
            after_dot_parts[1] = after_dot_parts[1][:-1]
            num_of_zeroes_in_period = 0
            for i in after_dot_parts[1]:
                if i == '0':
                    num_of_zeroes_in_period += 1
                else:
                    break
            after_dot_parts[1] = num2words(after_dot_parts[1][num_of_zeroes_in_period :], lang='ru')

            ans = before_dot

            if len(after_dot_parts[0]) != 0:
                rank_10 = adot_usual[len(after_dot_parts[0])]
                for i in after_dot_parts[0]:
                    if i == '0':
                        after_dot_parts[0] = after_dot_parts[0][1:]
                    else:
                        break
                after_dot_parts[0] = num2words(int(after_dot_parts[0]), lang='ru')
                ans += ' и ' + after_dot_parts[0] + ' ' + rank_10

            ans += ' и ' + "ноль "*num_of_zeroes_in_period + after_dot_parts[1] + " в периоде"

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

