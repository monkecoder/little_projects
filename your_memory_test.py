import random
import time

is_mixing = False  # нужно ли перемешивать слова при выдаче
words_num = 32  # количество слов

max_dec_len = len(str(words_num - 1))
max_hex_len = len(hex(words_num - 1)) - 2

words_full = [
    'книга',     'концерт',   'гора',      'ладонь',        # 0
    'доктор',    'дождь',     'колесо',    'провод',        # 1
    'труба',     'поле',      'кожа',      'дорога',        # 2
    'цветок',    'река',      'магазин',   'стол',          # 3
    'рыба',      'солнце',    'нос',       'президент',     # 4
    'костёр',    'фильм',     'дача',      'снег',          # 5
    'дуб',       'шишка',     'осьминог',  'метель',        # 6
    'сосна',     'нога',      'расчёска',  'собака',        # 7

    'кошелёк',   'кошка',     'болото',    'рубашка',       # 8
    'зеркало',   'окно',      'рюкзак',    'клавиатура',    # 9
    'ель',       'кактус',    'бобёр',     'кукуруза',      # 10
    'мухомор',   'страус',    'гитара',    'полотенце',     # 11
    'гирлянда',  'ножницы',   'стакан',    'велосипед',     # 12
    'луна',      'шкаф',      'кит',       'ледник',        # 13
    'муравей',   'кочерга',   'кастрюля',  'бумеранг',      # 14
    'повар',     'весло',     'подкова',   'монета',        # 15

    'волк',      'швабра',    'заноза',    'бумага',        # 16
    'чайник',    'стрекоза',  'колокол',   'лампа',         # 17
    'лупа',      'трактор',   'тигр',      'чашка',         # 18
    'сундук',    'арматура',  'вешалка',   'зонт',          # 19
    'свеча',     'весло',     'степь',     'лошадь',        # 20
    'чучело',    'манул',     'печенье',   'библиотека',    # 21
    'озеро',     'коробка',   'валенок',   'квас',          # 22
    'шкатулка',  'лестница',  'ковёр',     'метро',         # 23

    'термометр', 'блин',      'вишня',     'мешок',         # 24
    'баклажан',  'наушники',  'цапля',     'верёвка',       # 25
    'мост',      'бутерброд', 'медуза',    'пугало',        # 26
    'клён',      'слон',      'жаба',      'капкан',        # 27
    'слизень',   'блокнот',   'фартук',    'утюг',          # 28
    'скатерть',  'тесто',     'кладбище',  'загар',         # 29
    'клетка',    'клон',      'дракон',    'печь',          # 30
    'пепел',     'шоколад',   'гном',      'пружина'        # 31
]

# перевод перемешанных значений в словарь
def wdict_add(list_default, list_mixed, dict_mixed):
    for element in list_mixed:
        dict_mixed[list_default.index(element)] = element

# выравнивание вывода пробелами
def spaces(some_str, form=''):
    if form == 'd':
        n = max_dec_len - len(some_str) + 1
    elif form == 'h':
        n = max_hex_len - len(some_str) + 1
    else:
        n = 1
    return n * ' '

# основная программа
def test():
    # выбор слов из общего списка
    words = random.sample([el for el in words_full if words_full.count(el) == 1], words_num)

    words_mixed_dict1 = dict()  # словарь для выдачи слов
    words_mixed_dict2 = dict()  # словарь для проверки слов

    # выбор последовательности слов на выдачу
    if is_mixing:
        words_mixed = random.sample(words, words_num)
    else:
        words_mixed = words.copy()
    wdict_add(words, words_mixed, words_mixed_dict1)

    # выдача слов
    print('Запоминайте:', end='\n\n')
    i = 0
    inp = '-'
    start_time = time.time()
    for key in words_mixed_dict1:
        print(f'[#{i}] {key} (hex: {hex(key)[2:]}): {words_mixed_dict1[key]}')
        inp = input()
        if inp == '0':
            return
        elif inp == '1':
            break
        print('\n' * 10)
        i += 1
    all_time = time.time() - start_time

    # выбор последовательности слов на проверку
    words_mixed = random.sample(words_mixed, words_num)
    wdict_add(words, words_mixed, words_mixed_dict2)

    # проверка слов
    print(8 * '\n')
    print('Вспоминайте:', end='\n\n')
    ok_sum = 0
    i = 0
    conf_tuple = ('', '0', '1')
    notfound_words = dict()
    found_words = dict()
    for key in words_mixed_dict2:
        word = words_mixed_dict2[key]
        inp = '-'
        is_start = False
        while(inp != word and inp not in conf_tuple):
            if is_start:
                print('Неправильное слово\n')
            is_start = True
            print(f'[#{i}] {key} (hex: {hex(key)[2:]}): ', end='')
            inp = input()
            print()
        if inp == word:
            found_words[key] = words_mixed_dict2[key]
            ok_sum += 1
        elif inp == '':
            notfound_words[key] = words_mixed_dict2[key]
        elif inp == '0':
            return
        elif inp == '1':
            for key in words_mixed_dict2:
                if key not in found_words and key not in notfound_words:
                    notfound_words[key] = words_mixed_dict2[key]
            break
        i += 1
    
    # вывод результатов
    print('\n\n')
    print(f'Воспроизведённые слова: {ok_sum}/{words_num}\n')
    notfound_words = dict(sorted(notfound_words.items()))
    if len(notfound_words) > 0:
        i = 0
        print('Список невоспроизведённых слов:')
        for key in notfound_words:
            print(f"[#{i}]{spaces(str(i), 'd')}{key}{spaces(str(key), 'd')}(hex: {hex(key)[2:]}):{spaces(hex(key)[2:], 'h')}{words_mixed_dict2[key]}")
            i += 1
    print()
    print('На запоминание списка было потрачено', round(all_time / 60, 2), 'мин.')
    print('В среднем', round(all_time / words_num, 2), 'cек. на слово', end='\n\n')


if __name__ == "__main__":
    test()
