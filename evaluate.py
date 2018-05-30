import uncertainty as u
import parser as p

## Evaluate parses using functions in uncertainty.py

# a fully parsed me is sent to the evaluator
# must unwrap values and apply appropriate operations

# strategy: recursive unwrapper which detects the objects and handles appropriately


        

# unc_eval: a function which applies the given operation, and returns the resulting measure
# should be recursive: ie evaluate inner part before outer
# input: a parser.(Mathematical expression) object
# output: an uncertainty.measure object
# evaluation of negative expressions: evaluate then make the result negative
def unc_eval(me):
    if type(me) == p.Measure:
        return u.measure(me.val, me.uncert)
    
    if type(me) == p.GroupME:
        return unc_eval(me.expr)
    if type(me) == p.NegME:
        non_neg_result = unc_eval(me.expr)
        return u.measure(-(non_neg_result.val), non_neg_result.uncert)

    if type(me) == p.AddME:
        left_res = unc_eval(me.left)
        right_res = unc_eval(me.right)
        return u.qsum(left_res, right_res)
    if type(me) == p.SubME:
        left_res = unc_eval(me.left)
        right_res = unc_eval(me.right)
        return u.qsub(left_res, right_res)

    if type(me) == p.MulME:
        left_res = unc_eval(me.left)
        right_res = unc_eval(me.right)
        return u.multiply(left_res, right_res)
    if type(me) == p.DivME:
        left_res = unc_eval(me.left)
        right_res = unc_eval(me.right)
        return u.divide(left_res, right_res)

    if type(me) == p.PowerME:
        base_res = unc_eval(me.base)
        # exponent is an integer
        return u.power(base_res, me.exp)

    if type(me) == p.SinME:
        arg_res = unc_eval(me.arg)
        return u.sine(arg_res)
    if type(me) == p.CosME:
        arg_res = unc_eval(me.arg)
        return u.cosine(arg_res)
    if type(me) == p.LogME:
        arg_res = unc_eval(me.arg)
        return u.loge(me.arg)



