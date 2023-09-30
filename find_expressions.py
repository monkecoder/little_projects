from itertools import permutations


def check_expression(num_list):
    if len(num_list) != 10:
        return None
    
    result = True
    for cnt in range(2):
        if (num_list[0 + cnt * 5] * 10 + num_list[1 + cnt * 5]) * num_list[2 + cnt * 5] != num_list[3 + cnt * 5] * 10 + num_list[4 + cnt * 5]:
            result = False
            break
    return result

def print_expression(num_list):
    for cnt in range(2):
        print('{0}{1} x {2} = {3}{4}'.format(num_list[0 + cnt * 5], num_list[1 + cnt * 5], num_list[2 + cnt * 5], num_list[3 + cnt * 5], num_list[4 + cnt * 5]))
    print()


if __name__ == '__main__':
    int_list = list(range(10))
    permutations = permutations(int_list)
    for permutation in permutations:
        if check_expression(permutation):
            print_expression(permutation)
