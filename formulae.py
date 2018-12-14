from automata import *

# these are just some wrappers so that the syntax used when specifying
# formulae is readable and normal

def Exists(variable, formula):
    def exists_susp(debug):
        return exists(variable, formula(debug), debug=debug)
    return exists_susp

def Neg(formula):
    def neg_susp(debug):
        return neg(formula(debug), debug=debug)
    return neg_susp

def And(formula_1, formula_2):
    def and_susp(debug):
        return conj(formula_1(debug), formula_2(debug), debug=debug)
    return and_susp

def Or(formula_1, formula_2):
    def or_susp(debug):
        return disj(formula_1(debug), formula_2(debug), debug=debug)
    return or_susp

def Reduce(formula, debug=0):
    return formula(debug)

def Eval(formula, debug=0):
    a = Reduce(formula, debug)
    if not a.is_boolean():
        raise Exception("You have free variables")
    else:
        return a.bval

def ForAll(variable, formula):
    return Neg(Exists(variable, Neg(formula)))

def Implies(antecedent, conclusion):
    return Or(Neg(antecedent), conclusion)
