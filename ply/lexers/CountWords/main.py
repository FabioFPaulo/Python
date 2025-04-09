import ply.lex as lex
tokens = ('PAL', 'SPACE')


def t_PAL(t):
    r'Maria'
    t.lexer.count += 1
    print(t.value, t.lexer.count, end="")


def t_SPACE(t):
    r'.|\n'
    print(t.value, end="")


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


lexer = lex.lex()
lexer.count = 0
lexer.input("Maria is the housekeeper of Maria but if Maria got Maria ")

for token in lexer:
    pass

print()
print(lexer.count)
