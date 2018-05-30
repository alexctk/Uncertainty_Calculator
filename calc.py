import parser as p
import evaluate as e

def get_input_and_eval():
    user_in = input()
    internal_rep = p.parse_me(user_in)
    eval_exp = e.unc_eval(internal_rep)
    eval_exp.printMeasure()
    return


### TOP LEVEL ###

while(True):
    get_input_and_eval()
