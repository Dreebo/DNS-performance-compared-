def print_title(text):
    print('\x1b[1;03;36;40m' + text + '\x1b[0m')

def print_with_background(text):
    print('\x1b[1;03;30;102m' + text + '\x1b[0m')

def print_odd_table_line(text):
    print('\x1b[1;03;30;47m' + text + '\x1b[0m')

def print_even_table_line(text):
    print('\x1b[1;03;97;100m' + text + '\x1b[0m')
