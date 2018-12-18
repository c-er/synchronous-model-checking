#!/usr/bin/python3
from formulae import *
from automata import *

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

# the generic ECA automaton for bi-infinite words
def auto_biinfinite(rho):
    def f(v1, v2):
        d = {
            "alphabet": frozenset(["0", "1"]),
            "initial": frozenset([0]),
            "adjlist": {
                0: {
                    "final": True,
                    "edges": [
                        (0, {v1: "0", v2: rho("000")}),
                        (1, {v1: "1", v2: rho("001")})
                    ]
                },
                1: {
                    "final": True,
                    "edges": [
                        (3, {v1: "0", v2: rho("010")}),
                        (2, {v1: "1", v2: rho("011")})
                    ]
                },
                2: {
                    "final": True,
                    "edges": [
                        (2, {v1: "1", v2: rho("111")}),
                        (3, {v1: "0", v2: rho("110")})
                    ]
                },
                3: {
                    "final": True,
                    "edges": [
                        (1, {v1: "1", v2: rho("101")}),
                        (0, {v1: "0", v2: rho("100")})
                    ]
                }
            }
        }

        def susp(debug=0):
            if debug > 1:
                print("Auto_infinite", d)
            return Automaton(d)

        return susp
    return f

# the rule 90 automaton
def rho90(s):
    d = {
        "000": "0",
        "001": "1",
        "010": "0",
        "011": "1",
        "100": "1",
        "101": "0",
        "110": "1",
        "111": "0"
    }
    return d[s]

# the ECA automaton for fixed boundary condition (0s on both sides)
# note the higher order nature - takes in a rho and returns the
# corresponding suspension
def auto_fix(rho):
    def f(v1, v2):
        d = {
            "alphabet": frozenset([0, 1]),
            "initial": frozenset(["bot"]),
            "adjlist": {
                "bot": {
                    "final": False,
                    "edges": [
                        ("000", {v1: "0", v2: rho("000")}),
                        ("010", {v1: "1", v2: rho("010")}),
                        ("001", {v1: "0", v2: rho("001")}),
                        ("011", {v1: "1", v2: rho("011")}),
                    ]
                },
                "000": {
                    "final": False,
                    "edges": [
                        ("000", {v1: "0", v2: rho("000")}),
                        ("001", {v1: "0", v2: rho("001")}),
                        ("top", {v1: "0", v2: rho("000")}),
                    ]
                },
                "001": {
                    "final": False,
                    "edges": [
                        ("010", {v1: "1", v2: rho("010")}),
                        ("011", {v1: "1", v2: rho("011")}),
                        ("top", {v1: "1", v2: rho("010")}),
                    ]
                },
                "010": {
                    "final": False,
                    "edges": [
                        ("100", {v1: "0", v2: rho("100")}),
                        ("101", {v1: "0", v2: rho("101")}),
                        ("top", {v1: "0", v2: rho("100")}),
                    ]
                },
                "011": {
                    "final": False,
                    "edges": [
                        ("110", {v1: "1", v2: rho("110")}),
                        ("111", {v1: "1", v2: rho("111")}),
                        ("top", {v1: "1", v2: rho("110")}),
                    ]
                },
                "100": {
                    "final": False,
                    "edges": [
                        ("000", {v1: "0", v2: rho("000")}),
                        ("001", {v1: "0", v2: rho("001")}),
                        ("top", {v1: "0", v2: rho("000")}),
                    ]
                },
                "101": {
                    "final": False,
                    "edges": [
                        ("010", {v1: "1", v2: rho("010")}),
                        ("011", {v1: "1", v2: rho("011")}),
                        ("top", {v1: "1", v2: rho("010")}),
                    ]
                },
                "110": {
                    "final": False,
                    "edges": [
                        ("100", {v1: "0", v2: rho("100")}),
                        ("101", {v1: "0", v2: rho("101")}),
                        ("top", {v1: "0", v2: rho("100")}),
                    ]
                },
                "111": {
                    "final": False,
                    "edges": [
                        ("110", {v1: "1", v2: rho("110")}),
                        ("111", {v1: "1", v2: rho("111")}),
                        ("top", {v1: "1", v2: rho("110")}),
                    ]
                },
                "top": {
                    "final": True,
                    "edges": []
                }
            }
        }
        def susp(debug=0):
            if debug > 1:
                print("Auto-fixed", d)
            return Automaton(cleanup(d))
        return susp

    return f

# the prefix automaton - accepts iff string on tape v1 is a prefix of the
# string on tape v2
def auto_prefix(v1, v2):
    d = {
        "alphabet": frozenset(["0", "1", "#"]),
        "initial": frozenset([0]),
        "adjlist": {
            0: {
                "final": True,
                "edges": [
                    (0, {v1: "0", v2: "0"}),
                    (0, {v1: "1", v2: "1"}),
                    (1, {v1: "#", v2: "0"}),
                    (1, {v1: "#", v2: "1"}),
                ]
            },
            1: {
                "final": True,
                "edges": [
                    (1, {v1: "#", v2: "0"}),
                    (1, {v1: "#", v2: "1"}),
                    (1, {v1: "#", v2: "#"}),
                ]
            }
        }
    }
    def susp(debug=0):
        if debug > 1:
            print("Auto_prefix", d)
        return Automaton(d)
    return susp

# ENTER YOUR TEST CASES HERE ***************************************************

dbg_level = 0

print("\nMISCELLANEOUS TESTS")
print("=======================================================================")

F = ForAll("x", ForAll("y", Implies(auto_eq("x", "y"), auto_eq("y", "x"))))
print("Equality is symmetric:", Eval(F, debug=dbg_level))
# true

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(auto_eq("x", "y"), auto_eq("y", "z")), auto_eq("x", "z")))))
print("Equality is transitive:", Eval(F, debug=dbg_level))
# true

F = ForAll("x", ForAll("y", Implies(Neg(auto_eq("x", "y")), Neg(auto_eq("y", "x")))))
print("Inequality is symmetric:", Eval(F, debug=dbg_level))
# true

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(Neg(auto_eq("x", "y")), Neg(auto_eq("y", "z"))), Neg(auto_eq("x", "z"))))))
print("Inequality is transitive:", Eval(F, debug=dbg_level))
# false: 00 neq 11, 11 neq 00 but 00 = 00

F = ForAll("x", ForAll("y", Implies(auto_prefix("x", "y"), auto_prefix("y", "x"))))
print("Prefix is symmetric:", Eval(F, debug=dbg_level))
# false: 0# prefix 00, but not 00 prefix 0#

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(auto_prefix("x", "y"), auto_prefix("y", "z")), auto_prefix("x", "z")))))
print("Prefix is transitive:", Eval(F, debug=dbg_level))
# true

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(auto_prefix("x", "y"), auto_prefix("x", "z")), auto_prefix("y", "z")))))
print("Prefix relation is a function:", Eval(F, debug=dbg_level))
# nope, 0# is a prefix of 00 and 01

print("\nSUCCESSOR TESTS")
print("=======================================================================")

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(auto_succ("x", "y"), auto_succ("x", "z")), auto_eq("y", "z")))))
print("Successor relation is a function:", Eval(F, debug=dbg_level))
# true

F = Exists("x", Exists("y", Exists("z", And(auto_succ("y", "z"), And(Neg(auto_eq("x", "y")), auto_succ("x", "z"))))))
print("Successor is non-injective:", Eval(F, debug=dbg_level))
# false

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(auto_succ("x", "z"), auto_succ("y", "z")), auto_eq("x", "y")))))
print("Successor is injective:", Eval(F, debug=dbg_level))
# true, time difference between this one and the previous one is significant

F = ForAll("y", Exists("x", auto_succ("x", "y")))
print("Successor is surjective:", Eval(F, debug=dbg_level))
# true

F = Exists("x", auto_succ("x", "x"))
print("Successor contains a 1-cycle:", Eval(F, debug=dbg_level))
# empty string is a fixed point

F = Exists("x", Exists("y", And(auto_succ("x", "y"), And(auto_succ("y", "x"), Neg(auto_eq("x", "y"))))))
print("Successor contains a 2-cycle:", Eval(F, debug=dbg_level))
# succ(0) = 1, succ(1) = 0

F = Exists("x", Exists("y", Exists("z", And(auto_succ("x", "y"), And(auto_succ("y", "z"), And(auto_succ("z", "x"), Neg(auto_eq("x", "y"))))))))
print("Successor contains a 3-cycle:", Eval(F, debug=dbg_level))
# false because 3 is not a power of 2

F = Exists("w", Exists("x", Exists("y", Exists("z", And(auto_succ("w", "x"), And(auto_succ("x", "y"), And(auto_succ("y", "z"), And(auto_succ("z", "w"), And(Neg(auto_eq("w", "x")), And(Neg(auto_eq("w", "y")), Neg(auto_eq("w", "z"))))))))))))
print("Successor contains a 4-cycle:", Eval(F, debug=dbg_level))
# succ(00) = 10, succ(10) = 01, succ(01) = 11, succ(11) = 00

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
    # true iff s is 010, the successor of 100 in reverse binary

print("\nECA RULE 90 TESTS")
print("=======================================================================")

print("\nUsing the automaton for biinfinite strings:\n")
inf = auto_biinfinite(rho90)


F = ForAll("x", ForAll("y", ForAll("z", Implies(And(inf("x", "y"), inf("x", "z")), auto_eq("y", "z")))))
print("ECA 90 relation is a function:", Eval(F, debug=dbg_level))
# true

F = Exists("x", Exists("y", Exists("z", And(inf("y", "z"), And(Neg(auto_eq("x", "y")), inf("x", "z"))))))
print("ECA 90 is non-injective:", Eval(F, debug=dbg_level))
# false

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(inf("x", "z"), inf("y", "z")), auto_eq("x", "y")))))
print("ECA 90 is injective:", Eval(F, debug=dbg_level))
# true

F = ForAll("y", Exists("x", inf("x", "y")))
print("ECA 90 is surjective:", Eval(F, debug=dbg_level))
# true

F = Exists("x", inf("x", "x"))
print("ECA 90 contains a 1-cycle:", Eval(F, debug=dbg_level))

F = Exists("x", Exists("y", And(inf("x", "y"), And(inf("y", "x"), Neg(auto_eq("x", "y"))))))
print("ECA 90 contains a 2-cycle:", Eval(F, debug=dbg_level))

F = Exists("x", Exists("y", Exists("z", And(inf("x", "y"), And(inf("y", "z"), And(inf("z", "x"), Neg(auto_eq("x", "y"))))))))
print("ECA 90 contains a 3-cycle:", Eval(F, debug=dbg_level))

F = Exists("w", Exists("x", Exists("y", Exists("z", And(inf("w", "x"), And(inf("x", "y"), And(inf("y", "z"), And(inf("z", "w"), And(Neg(auto_eq("w", "x")), And(Neg(auto_eq("w", "y")), Neg(auto_eq("w", "z"))))))))))))
print("ECA 90 contains a 4-cycle:", Eval(F, debug=dbg_level))

print("\nUsing the automaton for fixed boundary (0s on both ends):\n")
fix = auto_fix(rho90)

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(fix("x", "y"), fix("x", "z")), auto_eq("y", "z")))))
print("ECA 90 relation is a function:", Eval(F, debug=dbg_level))

F = Exists("x", Exists("y", Exists("z", And(fix("y", "z"), And(Neg(fix("x", "y")), fix("x", "z"))))))
print("ECA 90 is non-injective:", Eval(F, debug=dbg_level))

F = ForAll("x", ForAll("y", ForAll("z", Implies(And(fix("x", "z"), fix("y", "z")), auto_eq("x", "y")))))
print("ECA 90 is injective:", Eval(F, debug=dbg_level))

F = ForAll("y", Exists("x", fix("x", "y")))
print("ECA 90 is surjective:", Eval(F, debug=dbg_level))
# false because, for instance, nothing evolves to "1"
# both "0" and "1" evolve to "0" under these fixed boundary conditions

F = Exists("x", fix("x", "x"))
print("ECA 90 contains a 1-cycle:", Eval(F, debug=dbg_level))

F = Exists("x", Exists("y", And(fix("x", "y"), And(fix("y", "x"), Neg(auto_eq("x", "y"))))))
print("ECA 90 contains a 2-cycle:", Eval(F, debug=dbg_level))

F = Exists("x", Exists("y", Exists("z", And(fix("x", "y"), And(fix("y", "z"), And(fix("z", "x"), Neg(auto_eq("x", "y"))))))))
print("ECA 90 contains a 3-cycle:", Eval(F, debug=dbg_level))

F = Exists("w", Exists("x", Exists("y", Exists("z", And(fix("w", "x"), And(fix("x", "y"), And(fix("y", "z"), And(fix("z", "w"), And(Neg(auto_eq("w", "x")), And(Neg(auto_eq("w", "y")), Neg(auto_eq("w", "z"))))))))))))
print("ECA 90 contains a 4-cycle:", Eval(F, debug=dbg_level))
