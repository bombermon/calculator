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


word = input()

word = translate_to_letter(word)

print(word)