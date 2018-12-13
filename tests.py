from formulae import *

# SAMPLE AUTOMATA **************************************************************

def auto_succ(v1, v2):
    return Automaton({
        "alphabet": frozenset(["0", "1"]),
        "initial": 1,
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
    })

def auto_eq(v1, v2):
    return Automaton({
        "alphabet": frozenset(["0", "1"]),
        "initial": 0,
        "adjlist": {
            0: {
                "final": True,
                "edges": [
                    (0, {v1: "0", v2: "0"}),
                    (0, {v1: "1", v2: "1"})
                ]
            }
        }
    })

# the non-injectivity test for the successor function
F = Exists("x", Exists("y", Exists("z", And(auto_succ("y", "z"), And(Neg(auto_eq("x", "y")), auto_succ("x", "z"))))))
t = Eval(F)
print(t)
