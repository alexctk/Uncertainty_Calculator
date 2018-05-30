# Uncertainty
Python tool for propagating experimental uncertainty

Applies basic rules of uncertainty propagation to streamline calculations. 

Run "calc.py" and enter a mathematical expression to be evaluated. 

Expressions are recursive, with the format "(" <expression> ")" <operator> "(" <expression> ")"
Values should be written as <float> "+/-" <float>, representing the value and its associated uncertainty. 

Supported operators: "+" "-" "*" "/" "\**"
Supported functions: "sin( <expression> )", "cos( <expression> )", "log( <expression> )"
  Note that log refers to the base e logarithm.
  
The tool is a work in progress, requiring debugging and addition of features.

