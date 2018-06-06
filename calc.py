import parser as p
import evaluate as e

# get one line of input, parse, and evaluate
def get_input_and_eval():
    user_in = input()
    internal_rep = p.parse_me(user_in)
    eval_exp = e.unc_eval(internal_rep)
    eval_exp.printMeasure()
    return

def get_file_and_eval():
    filename = input()
    me_file = open(filename, 'r')
    file_read = me_file.read()
    file_lines = file_read.splitlines()
    print(file_lines)
    output_list = []
    for i in range(len(file_lines)):
        internal_rep = p.parse_me(file_lines[i])
        # if parse fails, can get an ErrorME or None, in which case print the text which caused the error
        if type(internal_rep) == p.ErrorME or type(internal_rep) == None:
            print(file_lines[i])
        else:
            eval_exp = e.unc_eval(internal_rep)
            eval_exp.printMeasure()
    return

def print_directions():
    print("Example input: (3.14+/-0.02)+(1.12+/-0.01)")

### TOP LEVEL ###

while(True):
    print_directions()
    get_file_and_eval()
