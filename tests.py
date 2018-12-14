from formulae import *

# SAMPLE AUTOMATA **************************************************************

def auto_succ(v1, v2):
    d = {
        "alphabet": frozenset(["0", "1"]),
        "initial": frozenset([1]),
        "adjlist": {
            1: {
                "final": True,
                "edges": [
                    (0, {v1: "0", v2: "1"}),
                    (1, {v1: "1", v2: "0"})
                ]
            },
            0: {
                "final": True,
                "edges": [
                    (1, {v1: "1", v2: "1"}),
                    (0, {v1: "0", v2: "0"})
                ]
            }
        }
    }
    def susp(debug=0):
        if debug > 1:
            print("Auto_succ", d)
        return Automaton(d)
    return susp

def auto_eq(v1, v2):
    d = {
        "alphabet": frozenset(["0", "1"]),
        "initial": frozenset([0]),
        "adjlist": {
            0: {
                "final": True,
                "edges": [
                    (0, {v1: "0", v2: "0"}),
                    (0, {v1: "1", v2: "1"})
                ]
            }
        }
    }
    def susp(debug=0):
        if debug > 1:
            print("Auto_eq", d)
        return Automaton(d)
    return susp

def auto_eq_const(v1, s):
    alpha = set()
    for c in s:
        alpha.add(c)
    d = {
        "alphabet": frozenset(alpha),
        "initial": frozenset([0]),
        "adjlist": {
            0: {
                "final": len(s) == 0,
                "edges": []
            }
        }
    }

    for i, c in enumerate(s):
        d["adjlist"][i]["edges"].append((i + 1, {v1: c}))
        d["adjlist"][i + 1] = {
            "final": i + 1 == len(s),
            "edges": []
        }

    def susp(debug=0):
        if debug > 1:
            print("Auto_eq_const_" + s, d)
        return Automaton(d)

    return susp

def all_binstrings(l):
    if l == 0:
        return [""]
    L = all_binstrings(l - 1)
    return ["0" + s for s in L] + ["1" + s for s in L]

# the non-injectivity test for the successor function
F1 = Exists("x", Exists("y", Exists("z", And(auto_succ("y", "z"), And(Neg(auto_eq("x", "y")), auto_succ("x", "z"))))))
print(Eval(F1, debug=0))

# the injectivity test for the successor function
F2 = ForAll("x", ForAll("y", ForAll("z", Implies(And(auto_succ("x", "z"), auto_succ("y", "z")), auto_eq("x", "y")))))
print(Eval(F2, debug=0))

# successor of 1 is 2 and 2 only
F = ForAll("x", ForAll("y", Implies(And(auto_eq_const("x", "10"), auto_succ("x", "y")), auto_eq_const("y", "00"))))
print("10 + 10 =", "00", Eval(F, debug=0))
L = all_binstrings(3)
for s in L:
    F = ForAll("x", ForAll("y", Implies(And(auto_eq_const("x", "100"), auto_succ("x", "y")), auto_eq_const("y", s))))
    print("100 + 100 =", s, Eval(F, debug=0))

F = ForAll("y", Exists("x", Neg(auto_eq("x", "y"))))
