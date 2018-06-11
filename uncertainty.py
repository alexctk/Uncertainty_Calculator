import math
import rounding as r

class measure:
    val = 0.0
    uncert = 0.0
    def __init__(self, val, uncert):
        self.val = val
        self.uncert = uncert
    def writeMeasure( self ):
        print(self.uncert)
        chopped_uncert = r.chop_uncert(self.uncert)
        print(chopped_uncert)
        return (str(self.val)) + '+/-' + chopped_uncert
    def printMeasure( self ):
        print( self.val, '+/-', self.uncert )

## OPERATORS ##

# + - * /
# sin(), cos()
# e^, log_e()
# a^x

## OPERATORS ##        

def qsum( m1, m2 ):
    m = measure(0,0)
    m.val = m1.val + m2.val
    m.uncert = math.sqrt(math.pow(m1.uncert,2) + math.pow(m2.uncert,2))
    return m

def qsub( m1, m2 ):
    m = measure(0,0)
    m.val = m1.val - m2.val
    m.uncert = math.sqrt(math.pow(m1.uncert,2) + math.pow(m2.uncert,2))
    return m

def multiply( m1, m2 ):
    m = measure(0,0)
    m.val = m1.val*m2.val
    m.uncert = m.val*math.sqrt( math.pow( (m1.uncert/m1.val), 2 ) + math.pow( (m2.uncert/m2.val), 2 ) )
    return m

def divide( m1, m2 ):
    m = measure(0,0)
    m.val = m1.val/m2.val
    m.uncert = m.val*math.sqrt( math.pow( (m1.uncert/m1.val), 2 ) + math.pow( (m2.uncert/m2.val), 2 ) )
    return m

def expe( m1 ):
    m = measure(0,0)
    m.val = math.exp( m1.val )
    m.uncert =  m.val * m1.uncert
    return m

# base e logarithm

def loge( m1 ):
    m = measure(0,0)
    m.val = math.log( m1.val )
    m.uncert = (1/m.val)*m1.uncert
    return m


# m1 ^ exponent

def power( m1, exponent ):
    m = measure(0,0)
    m.val = math.pow( m1.val, exponent )
    m.uncert = m.val * exponent * (m1.uncert/m1.val)
    return m

def sine( m1 ):
    m = measure(0,0)
    m.val = math.sin( m1.val )
    m.uncert = abs(math.cos( m1.val ))*m1.uncert
    return m

def cosine( m1 ):
    m = measure(0,0)
    m.val = math.cos( m1.val )
    m.uncert = abs(math.sin( m1.val ))*m1.uncert
    return m


## MISC ##
def round_to_1( number ):
    return round( number, -int(math.floor(math.log10(abs(number)))))

def round_to_n( number, n ):
#http://code.activestate.com/recipes/578114-round-number-to-specified-number-of-significant-di/
    if number!= 0:
        return round( number, -int(math.floor(math.log10(abs(number)))) + (n - 1))
    else:
        return 0


def main():
    while True: 
        print()
        print('Menu')
        print()
        print('1) Addition')
        print('2) Subtraction')
        print('3) Multiplication')
        print('4) Division')
        print('5) exp')
        print('6) Base e log')
        print('7) Exponentiate')
        print('8) Sine')
        print('9) Cosine')

        user_in = int(input('Enter: '))

        if user_in == 1:
            print('(x+dx) + (y+dy)')
            x = float(input('x = '))
            dx = float(input('dx = '))
            y = float(input('y = '))
            dy = float(input('dy = '))
            m1 = measure(x, dx)
            m2 = measure(y, dy)
            result = qsum( m1, m2) 
            result.printMeasure()

        if user_in == 2:
            print('(x+dx) - (y+dy)')
            x = float(input('x = '))
            dx = float(input('dx = '))
            y = float(input('y = '))
            dy = float(input('dy = '))
            m1 = measure(x, dx)
            m2 = measure(y, dy)
            result = qsub( m1, m2) 
            result.printMeasure()

        if user_in == 3:
            print('(x+dx) * (y+dy)')
            x = float(input('x = '))
            dx = float(input('dx = '))
            y = float(input('y = '))
            dy = float(input('dy = '))
            m1 = measure(x, dx)
            m2 = measure(y, dy)
            result = multiply( m1, m2) 
            result.printMeasure()

        if user_in == 4:
            print('(x+dx) / (y+dy)')
            x = float(input('x = '))
            dx = float(input('dx = '))
            y = float(input('y = '))
            dy = float(input('dy = '))
            m1 = measure(x, dx)
            m2 = measure(y, dy)
            result = divide( m1, m2) 
            result.printMeasure()

        if user_in == 5:
            print('e^(x+dx)')
            x = float(input('x = '))
            dx = float(input('dx = '))
            m1 = measure(x, dx)
            result = expe( m1 )
            result.printMeasure()

        if user_in == 6:
            print('ln(x+dx)')
            x = float(input('x = '))
            dx = float(input('dx = '))
            m1 = measure(x, dx)
            result = loge( m1 ) 
            result.printMeasure()

        if user_in == 7:
            print('(x+dx)^a')
            x = float(input('x = '))
            dx = float(input('dx = '))
            y = float(input('a = '))
            m1 = measure(x, dx)
            result = power( m1, y)
            result.printMeasure()

        if user_in == 8:
            print('sin(x+dx)')
            x = float(input('x = '))
            dx = float(input('dx = '))
            m1 = measure(x, dx)
            result = sine( m1 ) 
            result.printMeasure()

        if user_in == 9:
            print('cos(x+dx)')
            x = float(input('x = '))
            dx = float(input('dx = '))
            m1 = measure(x, dx)
            result = cosine( m1 )
            result.printMeasure()




def test():
   result = chop_uncert(0.00913)
   print(result)

if __name__ == "__main__":
    test()
