import ply.lex as lex

tokens = (
	'AND',
	'OR',
	'NOT',
	'LPAREN',
	'RPAREN',
	'ASSIGN',
	'ID',
)

literals = '=*'

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_ASSIGN  = r'\*='

reserved = {
	'and': 'AND',
	'AND': 'AND',
	'or': 'OR',
	'OR': 'OR',
	'not': 'NOT',
	'NOT': 'NOT',
}

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_ID(t):
	r'[a-zA-Z_][a-zA-Z_0-9/-]*'
	t.type = reserved.get(t.value,'ID')    # Check for reserved words
	return t

t_ignore  = ' \t'

def t_error(t):
	print("Non-tokenizable character '%s'" % t.value[0])
	t.lexer.skip(1)

lexer = lex.lex()