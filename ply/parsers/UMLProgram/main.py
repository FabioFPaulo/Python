import ply.lex as lex
import ply.yacc as yacc
import sys
from PlantUMLConverter import PlantUMLConverter

# define tokens used by the lexer
tokens = ["MODE", "ALIAS", "LABEL"]

# characters to ignore (whitespace and newline)
t_ignore = ' \t\n'

# Token rule for label literals, enclosed in double quotes


def t_LABEL(t):
    r'"[^"]*"'
    t.value = t.value.strip('"')
    return t

# Token rule for MODE keywords (specific UML concepts)


def t_MODE(t):
    r'Actor|Node|Association|Include|Extend|Inh'
    return t

# Token rule for ALIAS, which is a valid identifier


def t_ALIAS(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    return t

# Error handler for illegal characters


def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)


# Build the lexer
lexer = lex.lex()

# =========================================
# ==============Parsing Rules==============
# =========================================


# Grammar rule to allow multiple statements
def p_statements(p):
    '''statements : statements statement
                  | statement'''
    if len(p) == 2:
        p[0] = [p[1]]  # Single statement case
    else:
        p[0] = p[1] + [p[2]]  # Recursive concatenation of statements


# Grammar rule to define what a valid statement is
def p_statement(p):
    '''statement : mode_stmt
                 | link_stmt'''
    p[0] = p[1]


# Grammar rule for mode statements like: Actor Alice "A user"
def p_mode_stmt(p):
    'mode_stmt : MODE ALIAS LABEL'
    p[0] = (p[1], p[2], p[3])  # Return a tuple representing the statement


# Grammar rule for link statements like: Include Alice Bob
def p_link_stmt(p):
    'link_stmt : MODE ALIAS ALIAS'
    p[0] = (p[1], p[2], p[3])  # Return a tuple representing the link


# Syntax error handler
def p_error(p):
    print(f"Syntax error at '{p.value}'" if p else "Syntax error at EOF")


# Build the parser
parser = yacc.yacc()

# Entry point: check if filename argument is provided
if len(sys.argv) < 2:
    sys.exit("Usage: %s <filename>" % sys.argv[0])


# Open and read the input file
fp = open(sys.argv[1])
contents = fp.read()

# Parse the input file contents
result = parser.parse(contents)

# Convert parsed result into PlantUML format
plt = PlantUMLConverter(result)
print(plt)  # Print info about converter object

# Build and print the UML representation
uml = plt.build_uml()
print()
print(uml)
