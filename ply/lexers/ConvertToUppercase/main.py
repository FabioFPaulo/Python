import ply.lex as lex

tokens = ("WORD", "SPACE")


def t_WORD(t):
    r'[a-z]'
    print(t.value.upper(), end="")


def t_SPACE(t):
    r'.|\n'
    print(t.value, end="")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
lexer.input("Maria is the housekeeper of Maria but if Maria got Maria")

for token in lexer:
    pass

print()
