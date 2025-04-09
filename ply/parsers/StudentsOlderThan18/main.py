import sys
import ply.yacc as yacc
import ply.lex as lex
tokens = (
    'NAME', 'AGE'
)


def t_NAME(t):
    r'[a-zA-Z]+'
    return t


def t_AGE(t):
    r'[0-9]+'
    return t


# Ignored characters
t_ignore = " \t\n"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()
# Parsing rules


def p_def_def(t):
    'def : students'


def p_def_students(t):
    '''students : student
        | students student'''


def p_def_student(t):
    'student : NAME AGE'
    num = int(t[2])

    if (num > 18):
        print(t[1])


def p_error(t):
    print("Syntax error at '%s'" % t.value)


parser = yacc.yacc()
if len(sys.argv) < 2:
    sys.exit("Usage: %s <filename>" % sys.argv[0])

fp = open(sys.argv[1])
contents = fp.read()
result = parser.parse(contents)
