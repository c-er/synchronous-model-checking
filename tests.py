from formulae import *

# SAMPLE AUTOMATA **************************************************************

# the successor automaton we designed in homework 7
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

# returns an automaton that checks if the strings on tapes v1 and v2 are the same
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

# returns an automaton that accepts if and only if the string on tape
# v1 is s
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

# the rule 90 automaton from the lecture notes
def auto_rule90(v1, v2):
    d = {
        "alphabet": frozenset(["0", "1"]),
        "initial": frozenset([0]),
        "adjlist": {
            0: {
                "final": True,
                "edges": [
                    (0, {v1: "0", v2: "0"}),
                    (1, {v1: "1", v2: "1"})
                ]
            },
            1: {
                "final": True,
                "edges": [
                    (3, {v1: "0", v2: "0"}),
                    (2, {v1: "1", v2: "1"})
                ]
            },
            2: {
                "final": True,
                "edges": [
                    (2, {v1: "1", v2: "0"}),
                    (3, {v1: "0", v2: "1"})
                ]
            },
            3: {
                "final": True,
                "edges": [
                    (1, {v1: "1", v2: "0"}),
                    (0, {v1: "0", v2: "1"})
                ]
            }
        }
    }

    def susp(debug=0):
        if debug > 1:
            print("Auto_rule90", d)
        return Automaton(d)

    return susp

# ENTER YOUR TEST CASES HERE ***************************************************

dbg_level = 2

F = ForAll("x", auto_eq("x", "x"))
print("Equality is reflexive:", Eval(F, debug=dbg_level))

F = ForAll("x", ForAll("y", Implies(auto_eq("x", "y"), auto_eq("y", "x"))))
print("Equality is symmetric:", Eval(F, debug=dbg_level))

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(auto_eq("x", "y"), auto_eq("y", "z")), auto_eq("x", "z")))))
print("Equality is transitive:", Eval(F, debug=dbg_level))

F = ForAll("x", Neg(auto_eq("x", "x")))
print("Inequality is reflexive:", Eval(F, debug=dbg_level))

F = ForAll("x", ForAll("y", Implies(Neg(auto_eq("x", "y")), Neg(auto_eq("y", "x")))))
print("Inequality is symmetric:", Eval(F, debug=dbg_level))

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(Neg(auto_eq("x", "y")), Neg(auto_eq("y", "z"))), Neg(auto_eq("x", "z"))))))
print("Inequality is transitive:", Eval(F, debug=dbg_level))

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(auto_succ("x", "y"), auto_succ("x", "z")), auto_eq("y", "z")))))
print("Successor relation is a function:", Eval(F, debug=dbg_level))

F = Exists("x", Exists("y", Exists("z", And(auto_succ("y", "z"), And(Neg(auto_eq("x", "y")), auto_succ("x", "z"))))))
print("Successor is non-injective:", Eval(F, debug=dbg_level))

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(auto_succ("x", "z"), auto_succ("y", "z")), auto_eq("x", "y")))))
print("Successor is injective:", Eval(F, debug=dbg_level))

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(auto_rule90("x", "y"), auto_rule90("x", "z")), auto_eq("y", "z")))))
print("Rule 90 relation is a function:", Eval(F, debug=dbg_level))

F = Exists("x", Exists("y", Exists("z", And(auto_rule90("y", "z"), And(Neg(auto_eq("x", "y")), auto_rule90("x", "z"))))))
print("Rule 90 is non-injective:", Eval(F, debug=dbg_level))

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(auto_rule90("x", "z"), auto_rule90("y", "z")), auto_eq("x", "y")))))
print("Rule 90 is injective:", Eval(F, debug=dbg_level))

# successor of 1 (as a length-3 string in reverse binary) is 2, and not anything else
def all_binstrings(l):
    if l == 0:
        return [""]
    L = all_binstrings(l - 1)
    return ["0" + s for s in L] + ["1" + s for s in L]
L = all_binstrings(3)
for s in L:
    F = ForAll("x", ForAll("y", Implies(And(auto_eq_const("x", "100"), auto_succ("x", "y")), auto_eq_const("y", s))))
    print("Successor of 100 is", s, ":", Eval(F, debug=dbg_level))
