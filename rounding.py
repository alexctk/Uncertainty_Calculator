# Rounding logic
# A val should be rounded such that it is as precise as it's uncertainty indicates
# uncert should be rounded to one significant digit if it's first digit is greater than 2
# uncert is rounded to two significant digits if it's first digit is less than 2

# to handle the rounding we can work with string forms of val and uncert
# find the first nonzero digit in uncert (scanning from left)

# input: floating point number representing measure uncertainty
# output: string with unecessary digits removed
def chop_uncert( fl ):
    string_form = str(fl)
    string_length = len(string_form)
    i = 0
    while(string_form[i] == '0' or string_form[i] == '.'):
        i = i+1
    #print(string_form[i])
    if int(string_form[i]) > 1 and i+1 < string_length:
        chopped = string_form[:i+1]
    elif i+2 < string_length:
        chopped = string_form[:i+2]
    else:
        chopped = string_form

    return chopped
