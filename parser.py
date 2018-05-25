from uncertainty import *

# BNF grammars for mathematical expressions: 


# <expression> ::= <signed-term> | <expression> "+" <term> | <expression> "-" <term>
# <signed-term> ::= "-" <term> | <term>
# <term> ::= <factor> | <term> * <factor>  | <term> / <factor>
# <factor> ::= <element> | <element> ** <numeral>
# <element> ::= <func> | <variable> | <numeral> | "(" <expression> ")"
# <func> :: = <measure> | 'sin' '(' <measure> ')' | 'cos' '(' <measure> ')' | 'log' '(' <measure> ')'
# <measure> ::= <variable> | <decimal> "+/-" <decimal> | <variable> "+/-" <decimal>
# <variable> ::= [a-z]
# <decimal> ::= [0-9]+ "." [0-9]+ | <numeral> ::= <numeral> | <numeral> "." <numeral>
# <numeral> ::= [0-9]+


# recursive descent parser for mathematical expressions

# first define the internal representation of mathematical expressions
# using classes

# integer
class Number:
    def __init__(self, value):
        self.value = value

# two integers representing the integral part and fractional
class Decimal:
    def __init__(self, integ, frac):
        self.integ = integ
        self.frac = frac

# two floats representing measurement value and its uncertainty
class Measure:
    def __init__(self, val, uncert):
        self.val = val
        self.uncert = uncert

# symbolic variable represented by a single character
class Variable:
    def __init__(self, char):
        self.char = char


# expr is a mathematical expression
# could be Number, Variable, GroupME, NegME, etc. 
class GroupME:
    def __init__(self, expr):
        self.expr = expr
        
# negative expression
class NegME:
    def __init__(self, expr):
        self.expr = expr

# addition of two expressions
class AddME:
    def __init__(self, left, right):
        self.left = left
        self.right = right

# subtraction of two expressions
class SubME:
    def __init__(self, left, right):
        self.left = left
        self.right = right

# multiplication of two expressions
class MulME:
    def __init__(self, left, right):
        self.left = left
        self.right = right

class DivME:
    def __init__(self, left, right):
        self.left = left
        self.right = right

# an expression raised to an integer power
class PowerME:
    def __init__(self, base, exp):
        self.base = base
        self.exp = exp

class SinME:
    def __init__(self, arg):
        self.arg = arg

class CosME:
    def __init__(self, arg):
        self.arg = arg

class LogME:
    def __init__(self, arg):
        self.arg = arg


# returned when a parse fails
class ErrorME:
    def __init__(self, msg):
        self.msg = msg


# define how we print a mathematical expression
# the type is shown first, then the relevant values
def show_me(me):
    if type(me) == Number:
        return ('(' + 'Num ' + str(me.value) + ')')

    elif type(me) == Decimal:
        return ('(' + 'Dec ' + str(me.integ) + '.' + str(me.frac) + ')')

    elif type(me) == Measure:
        return ('(' + 'Meas ' + str(me.val) + "+/-" + str(me.uncert) + ')')
    
    elif type(me) == Variable:
        return ('(' + 'Var ' + str(me.char) + ')')

    elif type(me) == GroupME:
        return ('(' + 'Group ' + show_me(me.expr) + ')')

    elif type(me) == NegME:
        return ('(' + 'Neg ' + show_me(me.expr) + ')')

    elif type(me) == AddME:
        return ('(' + 'Add ' + show_me(me.left) + ' ' + show_me(me.right) + ')')

    elif type(me) == SubME:
        return ('(' + 'Sub ' + show_me(me.left) + ' ' + show_me(me.right) + ')')

    elif type(me) == MulME:
        return ('(' + 'Mul ' + show_me(me.left) + ' ' + show_me(me.right) + ')')

    elif type(me) == DivME:
        return ('(' + 'Div ' + show_me(me.left) + ' ' + show_me(me.right) + ')')

    elif type(me) == PowerME:
        return ('(' + 'Power ' + show_me(me.base) + ' ' + str(me.exp) + ')')

    elif type(me) == SinME:
        return ('(' + 'Sin ' + show_me(me.arg) + ')')

    elif type(me) == CosME:
        return ('(' + 'Cos ' + show_me(me.arg) + ')')

    elif type(me) == LogME:
        return ('(' + 'Log ' + show_me(me.arg) + ')')
    
    elif type(me) == ErrorME:
        return me.msg


# Parser
# Input: a string, output:a list containing a ME and more characters

# <element> ::= <func> | <variable> | <numeral> | "(" <expression> ")"
def parse_elem(string):
    first = string[0]
    rest = string[1:]

    # check if we can find a valid Measure
    #measure = parse_measure(string)
    #if type(measure) != ErrorME:
    #    return measure

    function = parse_func(string)
    if type(function) != ErrorME:
        return function
        
    # if we see a bracket, look for an expression
    if first == '(':
        # (ME, String)
        expr_and_str = parse_expr(rest)
        str_first = expr_and_str[1][0]
        if str_first == ')':
            return [ GroupME(expr_and_str[0]), expr_and_str[1][1:] ]
        else:
            return ErrorME('Elem parse failure at group')
    # if alpha, it is a variable
    elif first.isalpha:
        return [ Variable(first), rest]
    # otherwise it is a number
    else:
        numeral_and_str = parse_numeral(string)
        if type(numeral_and_str) == ErrorME:
            return ErrorME('Elem parse failure at numeral')
        else:
            return [ Number( numeral_and_str[0]), numeral_and_str[1]]

# Integer parsing
def parse_numeral(string):
    if string == "":
        return ErrorME('Empty string to parse numeral')
    else:
        first = string[0]
        rest = string[1:]
        if first.isdigit():
            return extend_num(int(first), rest)
        else:
            return ErrorME('Numeral parse failure')

def extend_num(accum, string):
    if string == "":
        return [ accum, ""]
    else:
        first = string[0]
        rest = string[1:]
        if first.isdigit():
            return extend_num( 10*accum + int(first), rest)
        else:
            return [accum, string]

def parse_factor(string):
    elem_and_more = parse_elem(string)
    if type(elem_and_more) == ErrorME:
        return ErrorME('Factor parse failure')
    elif (elem_and_more[1] == ""):
        return elem_and_more
    elif (elem_and_more[1][0] == '*' and elem_and_more[1][1] == '*'):
        numeral_and_more = parse_numeral(elem_and_more[1][2:])
        if type(numeral_and_more) == ErrorME:
            return ErrorME('Factor parse failure at power')
        else:
            return [PowerME( elem_and_more[0], numeral_and_more[0]), numeral_and_more[1]]
    else:
        return elem_and_more

def parse_term(string):
    factor_and_more = parse_factor(string)
    if type(factor_and_more) == ErrorME:
        return ErrorME('Term parse failure in parsing factor')
    else:
        return extend_term(factor_and_more[0], factor_and_more[1])

def extend_term(me, string):
    if string == "":
        return [me, ""]
    
    elif (string[0] == '*'):
        factor_and_more = parse_factor(string[1:])
        if type(factor_and_more) == ErrorME:
            return ErrorME('Extend failure factor after star')
        else:
            return extend_term(MulME(me, factor_and_more[0]), factor_and_more[1])
        
    elif (string[0] == '/'):
        factor_and_more = parse_factor(string[1:])
        if type(factor_and_more) == ErrorME:
            return ErrorME('Extend term failure factor after backslash')
        else:
            return extend_term(DivME(me, factor_and_more[0]), factor_and_more[1])
        
    else:
        return [me, string]

def parse_expr(string):
    if (string[0] == '-'):
        term_and_more = parse_term(string[1:])
        if type(term_and_more) == ErrorME:
            return ErrorME('Expr parse failure minus')
        else:
            return [NegME(term_and_more[0], term_and_more[1])]
    else:
        term_and_more = parse_term(string)
        if type(term_and_more) == ErrorME:
            return ErrorME('Expr parse failure')
        else:
            return extend_expr(term_and_more[0], term_and_more[1])

def extend_expr(me, string):
    if string == "":
        return [me, ""]
    elif (string[0] == '+'):
        term_and_more = parse_term(string[1:])
        if type(term_and_more) == ErrorME:
            return ErrorME('Expr extend fail at add')
        else:
            return extend_expr(AddME(me, term_and_more[0]), term_and_more[1])
    elif (string[0] == '-'):
        term_and_more = parse_term(string[1:])
        if type(term_and_more) == ErrorME:
            return ErrorME('Expr extend fail at add')
        else:
            return extend_expr(SubME(me, term_and_more[0]), term_and_more[1])
    else:
        return [me, string]

# <func> :: = <measure> | 'sin' '(' <measure> ')' | 'cos' '(' <measure> ')' | 'log' '(' <measure> ')'
def parse_func(string):
    # make sure the string is indexable
    if len(string) > 4:
        if string[0:4] == "sin(":
            measure_and_more = parse_measure(string[4:])
            if type(measure_and_more[0]) == ErrorME:
                return ErrorME('Func parse failure detecting sin')
            elif measure_and_more[1] != "" and measure_and_more[1][0] == ')':
                return [SinME(measure_and_more[0]), measure_and_more[1][1:]]
            else:
                return ErrorME('Func parse failure detecting sin closing bracket')
            
        if string[0:4] == "cos(":
            measure_and_more = parse_measure (string[4:])
            if type(measure_and_more[0]) == ErrorME:
                return ErrorME('Func parse failure detecting cos')
            elif measure_and_more[1] != "" and measure_and_more[1][0] == ')':
                return [CosME(measure_and_more[0]), measure_and_more[1][1:]]
            else:
                return ErrorME('Func parse failure detecting cos closing bracket')
            
        if string[0:4] == "log(":
            measure_and_more = parse_measure (string[4:])
            if type(measure_and_more[0]) == ErrorME:
                return ErrorME('Func parse failure detecting log')
            elif measure_and_more[1] != "" and measure_and_more[1][0] == ')':
                return [LogME(measure_and_more[0]), measure_and_more[1][1:]]
            else:
                return ErrorME('Func parse failure detecting log closing bracket')
        else:
            measure_and_more = parse_measure(string)
            if type(measure_and_more) == ErrorME:
                return ErrorME('Func parse failure base case')
            else:
                return [measure_and_more[0], measure_and_more[1]]
    else:
        measure_and_more = parse_measure(string)
        if type(measure_and_more) == ErrorME:
            return ErrorME('Func parse failure short string')
        else:
            return [measure_and_more[0], measure_and_more[1]]
        

def parse_measure(string):
    # find the decimal on the left of "+/-"
    decimal_and_more = parse_decimal(string)
    if type(decimal_and_more) == ErrorME:
        return ErrorME('Measure parse failure at first decimal parse')
    elif decimal_and_more[1] == "":
        return [decimal_and_more[0], ""]
    elif decimal_and_more[1][0:3] == "+/-":
        after_symbol = parse_decimal( decimal_and_more[1][3:])
        if type(after_symbol) == ErrorME:
            return ErrorME("Measure parse failure at second decimal parse")
        else:
            # measure holds two floats, so we want to convert from our decimal representation
            # to a float

            value_float = make_float( decimal_and_more[0].integ, decimal_and_more[0].frac)
            uncert_float = make_float( after_symbol[0].integ, after_symbol[0].frac)
            return [Measure( value_float, uncert_float), after_symbol[1]]
    else:
        return [decimal_and_more[0], decimal_and_more[1]]

# helper function to obtain a float from our internal representation of a decimal
# input: int, int
def make_float( integ, frac):
    # obtain the fractional part by taking the frac numeral and dividing by 10^(number of digits)
    return integ + frac/(10**(len(str(frac))))
    

def parse_decimal(string):
    # find the first numeral
    numeral_and_more = parse_numeral(string)
    if type(numeral_and_more) == ErrorME:
        return ErrorME('Decimal parse failure at numeral parse')
    # not a decimal
    elif (numeral_and_more[1] == ""):
        return numeral_and_more
    # find the point in the decimal
    elif (numeral_and_more[1][0] == '.'):
        # look for the numeral after the point
        after_dot = parse_numeral(numeral_and_more[1][1:])
        if type(after_dot) == ErrorME:
            return ErrorME('Decimal parse failure after dot')
        else:
            return [Decimal(numeral_and_more[0], after_dot[0]), after_dot[1]]
    else:
        return numeral_and_more

    
def parse_me(string):
    if string == "":
        return ErrorME('Empty string')
    expr_and_more = parse_expr(string)
    if type(expr_and_more) == ErrorME:
        return expr_and_more
    elif expr_and_more[1] == "":
        return expr_and_more[0]
    else:
        return ErrorME('me parse failure')
        

# function which preprocesses a string to remove whitespace
def remove_whitespace(string):
    for i in range(len(string)):
        if (string[i] == " ") and ( (i+1) < len(string)):
            return remove_whitespace(new_string)
        elif (string[i] == " "):
            new_string = string[0:i]
            return remove_whitespace(new_string)
    return string
       

add_meas = "sin(1.23+/-0.04)"
parse = parse_func(add_meas)
print(show_me(parse))


