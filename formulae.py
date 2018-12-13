from automata import *

# these are just some wrappers so that the syntax used when specifying
# formulae is readable and normal

def Exists(variable, formula):
    return exists(variable, formula)

def Neg(formula):
    return neg(formula)

def And(formula_1, formula_2):
    return conj(formula_1, formula_2)

def Or(formula_1, formula_2):
    return disj(formula_1, formula_2)

def Eval(formula):
    return eval_truth(formula)
