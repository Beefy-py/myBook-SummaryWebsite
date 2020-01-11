numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']


def get_id(string):
    num = ''
    for i in string:
        if i in numbers:
            num += i
    return num


