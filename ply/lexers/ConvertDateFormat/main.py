import ply.lex as lex
import sys

tokens = ("DATE", "SPACER")


def t_DATE(t):
    r'[0-9]{2}/[0-9]{2}/[0-9]{4}'
    l = t.value.split("/")
    print(f"{l[2]}-{l[1]}-{l[0]}", end="")


def t_SPACER(t):
    r'.|\n'
    print(t.value, end="")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
if len(sys.argv) < 2:
    sys.exit("Usage: %s <filename>" % sys.argv[0])

fp = open(sys.argv[1])
contents = fp.read()
lexer.input(contents)

for token in lexer:
    pass
print()
