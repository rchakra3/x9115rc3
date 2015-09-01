def print_twice(str):
    do_twice(print_string, str)


def do_twice_orig(f):
    f()
    f()


def print_spam():
    print 'spam'


def do_twice(f, *args):
    f(*args)
    f(*args)


def print_string(str):
    print str


def print_no_break(str):
    print str,


def do_four(f, *args):
    do_twice(f, *args)
    do_twice(f, *args)


def print_seq_line(*args):
    symbols = args[0]
    repeat = 2
    if len(args) > 1:
        repeat = args[1]

    for i in range(0, repeat):
        print_no_break(symbols[0])
        do_four(print_no_break, symbols[1])

    print_string(symbols[0])


def print_one_seq(symbols1, symbols2, repeat):
    print_seq_line(symbols1, repeat)
    do_four(print_seq_line, symbols2, repeat)


def print_grid(rows, columns):
    for i in range(0, rows):
        print_one_seq(['+', '-'], ['/', ' '], columns)
    print_seq_line(['+', '-'], columns)


def right_justify(str):
    '''Function to right justify a string with a 70-col width'''
    print str.rjust(70)


def right_justify2(str):
    '''Another Function to right justify a string with a 70-col width'''
    print '{0:>{1}}'.format(str, 70)


print "\n\n*******************************************************************"
print "\t\t\tExercise 3.1"
print "*******************************************************************\n"

# repeat_lyrics()


def repeat_lyrics():
    print_lyrics()
    print_lyrics()


def print_lyrics():
    right_justify("I'm a lumberjack, and I'm okay.")
    right_justify2("I sleep all night and I work all day.")


print "\n\n*******************************************************************"
print "\t\t\tExercise 3.2 and 3.3"
print "*******************************************************************\n"

repeat_lyrics()


print "\n\n*******************************************************************"
print "\t\t\tExercise 3.4 Part 1"
print "*******************************************************************\n"

do_twice_orig(print_spam)


print "\n\n*******************************************************************"
print "\t\t\tExercise 3.4 Part 2"
print "*******************************************************************\n"

do_twice(print_string, 'spam')


print "\n\n*******************************************************************"
print "\t\t\tExercise 3.4 Part 3"
print "*******************************************************************\n"

print_twice('spam')


print "\n\n*******************************************************************"
print "\t\t\tExercise 3.4 Part 4"
print "*******************************************************************\n"

do_twice(print_twice, 'spam')


print "\n\n*******************************************************************"
print "\t\t\tExercise 3.4 Part 5"
print "*******************************************************************\n"

do_four(print_string, 'spam')


print "\n\n**********************************END******************************"
