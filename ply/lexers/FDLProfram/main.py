import sys
import ply.lex as lex

tokens = ("PROD", "OPT", "OF", 'MF', 'SPACE')


def t_PROD(t):
    r':'
    t.lexer.countProd += 1


def t_OPT(t):
    r'opt'
    t.lexer.countOpt += 1


def t_ALL(t):
    r'all'
    t.lexer.countA += 1
    print(t.value, end="")


def t_OF(t):
    r'one\-of'
    t.lexer.countOf += 1
    print(t.value, end="")


def t_MF(t):
    r'more\-of'
    t.lexer.countMf += 1
    print(t.value, end="")


def t_SPACE(t):
    r'.|\n'
    print(t.value, end="")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
lexer.countProd = 0
lexer.countOpt = 0
lexer.countA = 0
lexer.countOf = 0
lexer.countMf = 0

if len(sys.argv) < 2:
    sys.exit("Usage: %s <filename>" % sys.argv[0])

fp = open(sys.argv[1])
contents = fp.read()
lexer.input(contents)

while True:
    tok = lexer.token()
    if not tok:
        break  # No more input
    print(tok)

print("\nNumber of productions: ", lexer.countProd)
print("Number of optional comp: ", lexer.countOpt)
print("Number of all: ", lexer.countA)
print("Number of one_of: ", lexer.countOf)
print("Number of more_of: ", lexer.countMf)
