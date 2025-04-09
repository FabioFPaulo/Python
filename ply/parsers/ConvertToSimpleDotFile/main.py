import sys
import ply.yacc as yacc
import ply.lex as lex
tokens = (
    'NAME', 'LPAREN', 'COMA', 'RPAREN', 'SON'
)


def t_SON(t):
    r'SON'
    return t


def t_NAME(t):
    r'[a-z][A-Z]+'
    return t


literals = "(),"

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_COMA = r"\,"

t_ignore = " \t\n"


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()

parser = yacc.yacc()


if len(sys.argv) < 2:
    sys.exit("Usage: %s <filename>" % sys.argv[0])

fp = open(sys.argv[1])
contents = fp.read()
print("Digraph{")
result = parser.parse(contents)
print("}")
