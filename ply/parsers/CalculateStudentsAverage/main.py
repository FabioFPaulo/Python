import ply.yacc as yacc
import sys
import ply.lex as lex

tokens = ('NAME', 'N', 'OPAR', 'CPAR', 'COM')
literals = ",()"


def t_NAME(t):
    r'[a-zA-Z]+'
    return t


def t_N(t):
    r'[0-9]{1,2}'
    return t


t_OPAR = r'\('
t_CPAR = r'\)'
t_COM = r'\,'

t_ignore = " \t\n"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()


def p_def_def(t):
    'prog : students'
    print(t[1])


def p_def_students(t):
    '''students : student
                | students student'''
    if (len(t) == 2):
        t[0] = t[1]
    elif (len(t) == 3):
        t[0] = max(t[1], t[2])


def p_def_student(t):
    'student : NAME N OPAR N COM N COM N COM N CPAR'
    t[0] = (int(t[4])+int(t[6])+int(t[8])+int(t[10]))/4
    print(t[0])


def p_error(t):
    print("Syntax error at '%s'" % t.value)


parser = yacc.yacc()
if len(sys.argv) < 2:
    sys.exit("Usage: %s <filename>" % sys.argv[0])

fp = open(sys.argv[1])
contents = fp.read()
result = parser.parse(contents)
