# НАЧАЛО ИМПОРТА БИБЛИОТЕК
import re
from num2words import num2words
from googletrans import Translator
from word2number.w2n import word_to_num
from word2number import w2n

# КОНЕЦ ИМПОРТА БИБЛИОТЕК

# НАЧАЛО РАБОТЫ СО СЛОВАРЯМИ

operation_dict = ['плюс', 'минус', 'умножить', 'разделить на', 'поделить на', 'умножить на']   # СЛОВАРЬ ОПЕРАЦИЙ

adot_dict = {'десятых': 0.1, 'сотых': 0.01, 'тысячных': 0.001, 'десятитысячных': 0.0001,       # СЛОВАРЬ РАЗРЯДОВ
             'стотысячных': 0.00001, 'миллионных': 0.000001,
             'десятая': 0.1, 'сотая': 0.01, 'тысячная': 0.001, 'десятитысячная': 0.0001,
             'стотысячная': 0.00001, 'миллионная': 0.000001
             }

adot_usual = {1: 'десятых', 2: 'сотых', 3: 'тысячных', 4: 'десятитысячных', 5: 'стотысячных', 6: 'миллионных'}
                            # СЛОВАРЬ РАЗРЯДОВ ДЛЯ ЧИСЕЛ С ТОЧКОЙ

# КОНЕЦ РАБОТЫ СО СЛОВАРЯМИ

"""
        Функция перевода входного числа из словестного формата в числовой
    Происходит путем перевода из русского языка в английский, и использования сторонней библиотеки word2number
    
"""
def translate_to_letter(word):
    try: # Пытаемся сделать))
        translator = Translator() # Инициализируем гугл переводчик
        second_rank = None # Будем здесь хранить стрепень десятичной дроби
        for string in adot_dict: # Тут мы ищем эту степень во входной строки
            match2 = re.search(string, word)
            if match2:
                second_rank = string
        main_letter_adot = ' '

        match = re.search(r' и ', word) # Проверяем на наличие десятичной части
        if match:
            full_str = word.split(' и ') # Делим текст на лист из слов
            before_dot = translator.translate(full_str[0], src='ru', dest='en').text # Переводим текст части до запятой на английский
            before_dot = w2n.word_to_num(before_dot) # с помощью сторонней библиотеки word2number переводим наш текст в числа

            after_dot = full_str[1] # Собираем часть после запятой

            if after_dot[-1] == ' ':
                after_dot = after_dot[:-1]

            after_dot = after_dot.split(' ') # превращаем текст после запятой в лист из слов
            rank = after_dot[-1] # Находим степень
            del after_dot[-1] # Удаляем степень

            main_letter_adot = ' '.join(after_dot)

            main_letter_adot = main_letter_adot.replace("одна", "один")  # ЗАМЕНА ОДИН НА ОДНА

            main_letter_adot = translator.translate(main_letter_adot, src='ru', dest='en').text # Переводим в английский
            main_letter_adot = w2n.word_to_num(main_letter_adot) # Переводим в число


            rank = adot_dict[rank] # Превращаем степень из слова в число


            word = before_dot + main_letter_adot*rank # Соединяем целую и дробную часть

        elif(second_rank != None): # Зайдем если есть только дробная часть (баш ватылды)

            if word[-1] == ' ':
                word = word[:-1]

            word = word.split(' ') # Делим текст на лист из слов
            rank = word[-1] # Находим степень
            del word[-1] # Удаляем степень


            main_letter_adot = ' '.join(word)  # Содираем для перевода

            main_letter_adot = main_letter_adot.replace("одна", "один")  # ЗАМЕНА ОДНА НА ОДИН


            main_letter_adot = translator.translate(main_letter_adot, src='ru', dest='en').text # Переводим в английский
            main_letter_adot = w2n.word_to_num(main_letter_adot) # Переводим в число

            rank = adot_dict[rank] # Превращаем степень из слова в число


            word =  main_letter_adot * rank # Записывем дробную часть
        else:  # Зайдем если дробной части нет, что и есть хорошо

            word = translator.translate(word, src='ru', dest='en').text # Переводим в английский
            word = w2n.word_to_num(word) # Переводим в число
        return word
    except ValueError: # Если какие-то ошибки сообщаем об этом
        return -1
    except AttributeError:
        return -1
    except KeyError:
        return -1

# КОНЕЦ ФУНКЦИИ ПЕРЕВОДА

# НАЧАЛО ФУНКЦИИ ДЕЛЕНИЯ
"""
        Функция деления с нахоженим десятичной дроби и периода.
    После нахожедения челой части путем обычного деления, для нахождения нецелой части программа меняет делимое
    на остаток от деления, домнажает на десять. Также с помощью словоря отслеживается текущие делители, чтобы они
    не повторялись. Если все же повторяются, то переводит их в период

"""
def division(numerator, denominator):
    # Делимое и делитель умножаются на 10.000.000 что бы они были целыми, т. к. алгоритм работает только с целыми числами
    numerator = int(numerator * 10000000)
    denominator = int(denominator * 10000000)
    if (numerator % denominator == 0): # Проверка на делимость нацело
        ans = str(numerator // denominator) # Делим, возвращаем, красота!!!
        return ans
    else:
        ans = str(numerator // denominator) + "." # Нахождение целой части
        l = {} # Словарь текущих делителей
        index = 0 # Переменная для отслеживания когда встречается текущее делимое
        numerator = numerator % denominator # Для нахождения дробной части делимое становиться остатком от деления
        l[numerator] = index
        flag = False
        while flag == False: # Проверка на зацикливания текущего делимого после запятой, т. е. периодичность
            if numerator == 0: # Если текущий делитель равен нулю, то мы получаем в ответе окончалеьное частное, выходим из цикла
                break
            digit = numerator * 10 // denominator # Находим текущую цифру после запятой
            numerator = numerator * 10 - (numerator * 10 // denominator) * denominator # Находим текущее делимое
            if numerator not in l: # Если текущее делимое еще не встречалось, то записываем его в словарь, с ключом index
                ans += str(digit)
                index += 1
                l[numerator] = index
            else: # Иначе мы получаем цикл делителей, значит получаем периодичность
                ans += str(digit) + ")"
                ans = ans[:l.get(numerator) + len(ans[:ans.index(".") + 1])] + "(" + ans[l.get(numerator) + len(
                    ans[:ans.index(".") + 1]):] # Зная начало периода с ключом index, можем записать в ans частное
                flag = True
        return ans


# КОНЕЦ ФУНКЦИИ ДЕЛЕНИЯ

def calc(main_str):  # ФУНКЦИЯ КАЛЬКУЛЯТОР, ЕСЛИ ВОЗВРАЩАЕТСЯ "-1" - следовательно что-то сделано неверно!
    pattern = re.compile(r'[а-яёА-ЯЁ]+')
    goon = re.match(pattern, main_str)
    if not goon:      # ПРОВЕРКА НА РУССКИЕ СИМВОЛЫ
        return -1
    if not main_str:   # ПРОВЕРКА НА ПУСТОЕ ЗНАЧЕНИЕ
        return -1
    current_operation = 'error'
    for string in operation_dict:  # ПОИСК ОПЕРАЦИИ В СТРОКЕ
        match = re.search(string, main_str)
        if match:
            current_operation = string  # ОПЕРАЦИЯ
    if current_operation == 'error':
        return -1
    try:
        tokens = main_str.split(' ' + current_operation + ' ')  # ДЕЛИМ ЧИСЛО УДАЛЯЯ ОПЕРАЦИЮ
        first_num, second_num = tokens[:-1], tokens[-1:]
        first_num, second_num = first_num[0], second_num[0]
    except IndexError:   # ПРОВЕРКА НА ПРАВИЛЬНОСТЬ ВВЕДЕНИЕ
        return -1


    first_num = translate_to_letter(first_num)   # ПЕРЕВОД ДВУХ ЧИСЕЛ ИЗ ТЕКСТА В ЧИСЛА
    second_num = translate_to_letter(second_num)

    if (first_num == -1) or (second_num == -1):  # ПРОВЕРКА НА ОШИБКУ (К ФУНКЦИЯМ ПЕРЕВОДА)
        return -1

    if current_operation == "плюс":   # ОПЕРАЦИЯ СЛОЖЕНИЯ
        ans = first_num + second_num
    elif current_operation == "умножить" or current_operation == "умножить на":   # ОПЕРАЦИЯ УМНОЖЕНИЯ
        ans = first_num * second_num
    elif current_operation == "минус":   # ОПЕРАЦИЯ ВЫЧИТАНИЯ
        ans = first_num - second_num
    elif current_operation == "разделить на" or current_operation == "поделить на":    # ОПЕРАЦИЯ ДЕЛЕНИЯ,
        ans = division(first_num, second_num)                                          # ВЫПОЛНЯЕМАЯ ОТДЕЛЬНОЙ ФУНКЦИЕЙ
                                                                                       # division
    ans = str(ans)

    match = re.search('\.', ans)  # ПРОВЕРКА НА НАЛИЧИЕ ТОЧКИ (ДЕСЯТИЧНОГО ЧИСЛА)
    if match:
        ans = ans.split('.')    # РАЗДЕЛЕНИЕ ЧИСЛА НА "ДО ТОЧКИ" и "ПОСЛЕ ТОЧКи"
        before_dot = num2words(ans[0], lang='ru') # ПЕРЕВОД ЧИСЛА ДО ТОЧКИ
        after_dot = ans[1]   # ЧИСЛО ПОСЛЕ ТОЧКИ

        match = re.search(r'\(', after_dot)     # ПРОВЕРКА ЧИСЛА НА НАЛИЧИЕ ПЕРИОДА
        if match:
            after_dot_parts = re.split(r'\(', after_dot)   # ДЕЛИМ СТРОКУ НА ПЕРИОД И ТО, ЧТО ДО ПЕРИОДА, НО ПОСЛЕ ТОЧКИ
            after_dot_parts[1] = after_dot_parts[1][:-1]
            if len(after_dot_parts[0]) + len(after_dot_parts[1]) > 6:   # ОГРАНИЧЕНИЕ НА ДЛИНУ ПЕРИОДА (6)
                after_dot = (after_dot_parts[0] + after_dot_parts[1])[:6]
            else:
                num_of_zeroes_in_period = 0
                for i in after_dot_parts[1]:
                    if i == '0':
                        num_of_zeroes_in_period += 1   # СЧЕТЧИК НУЛЕЙ В ПЕРИОДЕ ДО ОСНОВНОГО ЧИСЛА
                    else:
                        break
                after_dot_parts[1] = num2words(after_dot_parts[1][num_of_zeroes_in_period:], lang='ru') # ПЕРЕВОД ЧИСЛА

                ans = before_dot

                if len(after_dot_parts[0]) != 0:                       # ПРОВЕРКА ЕСТЬ ЛИ ВООБЩЕ ЧТО-ТО ДО ПЕРИОДА
                    rank_10 = adot_usual[len(after_dot_parts[0])]      # ДЛИНА ЧИСЛА ПОСЛЕ ТОЧКИ, НЕЯВЛЯЮЩИМСЯ ПЕРИОДОМ
                    for i in after_dot_parts[0]:
                        if i == '0':                                   # УКОРАЧИВАНИЕ ЧИСЛА ПО ПОСЛЕДНИМ НУЛЯМ
                            after_dot_parts[0] = after_dot_parts[0][1:]
                        else:
                            break
                    after_dot_parts[0] = num2words(int(after_dot_parts[0]), lang='ru') #
                    ans += ' и ' + after_dot_parts[0] + ' ' + rank_10

                ans += ' и ' + "ноль " * num_of_zeroes_in_period + after_dot_parts[1] + " в периоде"
        match = re.search(r'\(', after_dot)
        if not match:                            # ЕСЛИ НЕТ ПЕРИОДА В ЧИСЛЕ
            rank_10 = adot_usual[len(after_dot)]                # ДЛИНА ЧИСЛА ПОСЛЕ ТОЧКИ, НЕЯВЛЯЮЩИМСЯ ПЕРИОДОМ
            for i in after_dot:
                if i == '0':                                    # УКОРАЧИВАНИЕ ЧИСЛА ПО ПОСЛЕДНИМ НУЛЯМ
                    after_dot = after_dot[1:]
                else:
                    break
            after_dot = num2words(int(after_dot), lang='ru')            # ПЕРЕВОД ЧИСЛА ПОСЛЕ ТОЧКИ В ТЕКСТ

            ans = before_dot + ' и ' + after_dot + ' ' + rank_10        # ФОРМИРОВАНИЕ ГОТОВОГО ОТВЕТА В СТРОКУ


    else:  # ЕСЛИ ОБЫЧНОЕ ЧИСЛО
        ans = num2words(ans, lang='ru')   # ПЕРЕВОД ЧИСЛА ОБРАТНО В ТЕКСТ

    return ans  # ВОЗВРАЩЕНИЕ ФУНКЦИЕЙ calc() ответа

"""
        Основная функция
    Считаем строку, пытаемся выполнить в ней описанною операцию. Если введено некорректно, выполняем заново,
    пока не сможем выполнить 
    
"""

if __name__ == "__main__":
    flag = True
    while flag:                                    # ЦИКЛ ДЛЯ ПРОВЕРКИ КОРРЕКТНОСТИ ВВЕДЕНЫХ ЗНАЧЕНИЙ
        line_main = input('Введите выражение: ')   # СЧИТЫВАНИЕ СТРОКИ В ВИДЕ: "ЧИСЛО ОПЕРАЦИЯ ЧИСЛО"
        line_main = line_main.lower()              # ЗАНИЖЕНИЕ СТРОКИ В НИЖНИЙ РЕГИСТР

        ans = calc(line_main)                      # ВЫЗОВ ФУНКЦИИ ОСНОВНОГО КАЛЬКУЛЯТОРА
        if ans != -1:                              # ПРОВЕРКА НА ОШИБКУ | ОШИБКА = -1, ИНАЧЕ - ОШИБОК НЕТ
            print('Ответ =', ans)
            flag = False                           # ВЫВОД СТРОКИ И ЗАВЕРШЕНИЕ ПРОГРАММЫ
        else:
            flag = True
            print('Вы ввели неверное выражение!')  # СООБЩЕНИЕ ОБ ОШИБКЕ