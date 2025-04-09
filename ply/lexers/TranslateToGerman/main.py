import sys
import ply.lex as lex
tokens = ('SPACE', 'LETTER_A', 'LETTER_E', 'LETTER_I', 'LETTER_O',
          'LETTER_U', 'LETTER')


def t_LETTER_A(t):
    r'[aA]'
    print("aitz", end="")


def t_LETTER_E(t):
    r'[eE]'
    print("ender", end="")


def t_LETTER_I(t):
    r'[iI]'
    print("inix", end="")


def t_LETTER_O(t):
    r'[oO]'
    print("over", end="")


def t_LETTER_U(t):
    r'[uU]'
    print("ufux", end="")


def t_LETTER(t):
    r'(.|\n)'
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
