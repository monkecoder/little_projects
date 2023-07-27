grades_dict = {
    1: ('плохо', 'кол', 'единица', 'мегаплох'),
    2: ('неудовлетворительно', 'неуд', 'неудовл', 'два', 'двойка', 'параша'),
    3: ('удовлетворительно', 'удовл', 'три', 'тройка', 'тройбан'),
    4: ('хорошо', 'хор', 'четыре', 'четвёрка', 'четверка'),
    5: ('отлично', 'отл', 'пять', 'пятёрка', 'пятерка', 'чудесно')
}


def check_input(inp):
    try:
        inp_int = int(inp)
    except ValueError:
        grades = [grade for grade in grades_dict if inp.lower() in grades_dict[grade]]
        if len(grades) != 0:
            inp_int = grades[0]
        else:
            print('not a correct number')
            return -1

    if inp_int < 1 or inp_int > 5:
        print('not a grade')
        return -1
    
    return inp_int


if __name__ == "__main__":
    inp = input()
    inp_list = list()
    inp_num, inp_sum = 0, 0
    inp_div = {grade: 0 for grade in grades_dict}

    while inp != '':
        inp_int = check_input(inp)
        if inp_int != -1:
            inp_num += 1
            inp_sum += inp_int
            inp_div[inp_int] += 1
            inp_list.append(inp_int)
        inp = input()


    if inp_num != 0:
        print('grades (numbers):', inp_list)
        print('grades (words):', [grades_dict[grade][0] for grade in inp_list])
        print('grades number:', inp_num)
        print('grades summary:', inp_sum)
        print('medium grade:', inp_sum * 1.0 / inp_num)
        print('grades divided:')
        [print('-', grades_dict[grade][0], ':', inp_div[grade]) for grade in inp_div.keys()]
        if inp_sum / inp_num < 3:
            print('\nNADO TRENIROVATSYA')
    else:
        print('no grades?')
    print()
