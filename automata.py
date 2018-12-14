from collections import deque

class Automaton:
    def __init__(self, d={"alphabet": frozenset(), "adjlist": {}}, bval=None):
        self.aut = d
        if isinstance(bval, bool):
            self.bval = bval
            self._isb = True
        else:
            self._isb = False

    def num_states(self):
        return len(self.aut["adjlist"]) if not self._isb else 0

    def is_boolean(self):
        return self._isb

    def __repr__(self):
        if self._isb:
            return "Automaton: " + str(self.bval)
        else:
            return "Automaton: " + str(self.aut)

def final_set(a):
    F = set()

    for k in a["adjlist"]:
        if a["adjlist"][k]["final"]:
            F.add(k)

    return frozenset(F)

def vars_set(a):
    V = set()
    for k in a["adjlist"]:
        for e in a["adjlist"][k]["edges"]:
            V = V.union(set(e[1].keys()))

    return frozenset(V)

def edge_merge(label1, label2):
    ret = {}
    for k in label1:
        if k in label2 and label1[k] != label2[k]:
            return None
        ret[k] = label1[k]
    for k in label2:
        ret[k] = label2[k]
    return ret

def cleanup(aut):
    num = 0
    d = {}
    alpha = set()
    for k in aut["adjlist"]:
        d[k] = num
        num += 1

    ret = {
        "initial": frozenset(map(lambda x: d[x], aut["initial"])),
        "adjlist": {}
    }

    for k in aut["adjlist"]:
        ret["adjlist"][d[k]] = {
            "final": aut["adjlist"][k]["final"],
            "edges": list(map(lambda x: (d[x[0]], x[1]), aut["adjlist"][k]["edges"]))
        }

        for x in aut["adjlist"][k]["edges"]:
            for u in x[1]:
                alpha.add(x[1][u])

    ret["alphabet"] = frozenset(alpha)
    return ret

def product_bfs(a, b, disj=False):
    adjlist = {}

    q = deque()
    init = set()
    for ai in a["initial"]:
        for bi in b["initial"]:
            init.add((ai, bi))
            q.append((ai, bi))

    while len(q) > 0:
        asrc, bsrc = q.pop()
        edges_a = a["adjlist"][asrc]["edges"]
        edges_b = b["adjlist"][bsrc]["edges"]


        if (asrc, bsrc) not in adjlist:
            bol = False
            if disj:
                bol = a["adjlist"][asrc]["final"] or b["adjlist"][bsrc]["final"]
            else:
                bol = a["adjlist"][asrc]["final"] and b["adjlist"][bsrc]["final"]
            adjlist[(asrc, bsrc)] = {
                "final": bol,
                "edges": []
            }

        for a_to, a_label in edges_a:
            for b_to, b_label in edges_b:
                e = edge_merge(a_label, b_label)
                if e:
                    adjlist[(asrc, bsrc)]["edges"].append(((a_to, b_to), e))
                    if (a_to, b_to) not in adjlist:
                        q.appendleft((a_to, b_to))

    return cleanup({
        "initial": frozenset(init),
        "adjlist": adjlist
    })

def disj(A, B, debug=0):
    if debug > 0:
        print("Orring machines of size %d and %d" % (A.num_states(), B.num_states()))

    if A.is_boolean():
        if A.bval:
            ret = Automaton(bval=True)
            if debug > 1:
                print(ret)
            return ret
        if B.is_boolean():
            if B.bval:
                ret = Automaton(bval=True)
                if debug > 1:
                    print(ret)
                return ret
            else:
                ret = Automaton(bval=False)
                if debug > 1:
                    print(ret)
                return ret
    if B.is_boolean():
        if B.bval:
            ret = Automaton(bval=True)
            if debug > 1:
                print(ret)
            return ret
        ret = Automaton(d=A.aut)
        if debug > 1:
            print(ret)
        return ret

    a = determinize(A.aut)
    b = determinize(B.aut)

    aut = product_bfs(a, b, disj=True)
    aut = determinize(aut)
    is_deterministic(aut)
    ret = Automaton(aut)
    if debug > 1:
        print(ret)
    return ret

def conj(A, B, debug=0):
    if debug > 0:
        print("Anding machines of size %d and %d" % (A.num_states(), B.num_states()))

    # decay to propositional logic
    if A.is_boolean():
        if not A.bval:
            ret = Automaton(bval=False)
            if debug > 1:
                print(ret)
            return ret
        if B.is_boolean():
            if not B.bval:
                ret = Automaton(bval=False)
                if debug > 1:
                    print(ret)
                return ret
            else:
                ret = Automaton(bval=True)
                if debug > 1:
                    print(ret)
                return ret
    if B.is_boolean():
        if not B.bval:
            ret = Automaton(bval=False)
            if debug > 1:
                print(ret)
            return ret
        ret = Automaton(d=A.aut)
        if debug > 1:
            print(ret)
        return ret

    a = determinize(A.aut)
    b = determinize(B.aut)

    aut = product_bfs(a, b, disj=False)
    aut = determinize(aut)
    is_deterministic(aut)
    ret = Automaton(aut)
    if debug > 1:
        print(ret)
    return ret

def all_alpha_tups(alpha, len):
    if len == 0:
        return [()]
    else:
        S = all_alpha_tups(alpha, len - 1)
        L = []
        for u in S:
            for a in alpha:
                L.append((a,) + u)
        return L

def all_labels(vars, alpha):
    L = all_alpha_tups(alpha, len(vars))
    S = []
    for t in L:
        d = {}
        cnt = 0
        for v in vars:
            d[v] = t[cnt]
            cnt += 1
        S.append(d)
    return S

def is_deterministic(a):
    if(len(a["initial"]) != 1):
        print("ERROR: too many initial states")
        raise Exception()
    labels = all_labels(vars_set(a), a["alphabet"])
    for v in a["adjlist"]:
        for l in labels:
            k = len(list(filter(lambda x: x[1] == l, a["adjlist"][v]["edges"])))
            if k != 1:
                print("ERROR:", k, "edges labeled", l, "out of", v, "detected")
                raise Exception()
                # print(a)
                return False
    return True

def determinize(a):
    adjlist = {}

    q = deque([a["initial"]])
    to_be_visited = set([a["initial"]])

    F = final_set(a)

    labels = all_labels(vars_set(a), a["alphabet"])

    while len(q) > 0:
        src = q.pop()
        to_be_visited.remove(src)

        if src not in adjlist:
            adjlist[src] = {
                "final": len(src & F) > 0,
                "edges": []
            }

        for l in labels:
            S = frozenset()
            for u in src:
                S = S | frozenset(map(lambda x: x[0], filter(lambda x: x[1] == l, a["adjlist"][u]["edges"])))
            adjlist[src]["edges"].append((S, l))
            if S not in adjlist and S not in to_be_visited:
                to_be_visited.add(S)
                q.appendleft(S)

    return cleanup({
        "initial": frozenset([a["initial"]]),
        "adjlist": adjlist
    })

def neg(A, debug=0):
    if debug > 0:
        print("Negating. Machine currently has %d states" % A.num_states())

    if A.is_boolean():
        ret = Automaton(bval=(not A.bval))
        if debug > 1:
            print(ret)
        return ret

    det = determinize(A.aut)
    for v in det["adjlist"]:
        det["adjlist"][v]["final"] = not det["adjlist"][v]["final"]

    ret = Automaton(det)
    if debug > 1:
        print(ret)
    return ret

def exists(var, A, debug=0):
    if debug > 0:
        print("Projecting. Machine currently has %d states" % A.num_states())
    if A.is_boolean():
        ret = Automaton(bval=A.bval)
        if debug > 1:
            print(ret)
        return ret
    a = A.aut

    ret = {
        "alphabet": a["alphabet"],
        "initial": a["initial"],
        "adjlist": {}
    }

    for v in a["adjlist"]:
        ret["adjlist"][v] = {
            "final": a["adjlist"][v]["final"],
            "edges": []
        }
        tmp = set()
        for e in a["adjlist"][v]["edges"]:
            d = dict(e[1])
            del d[var]
            tmp.add((e[0], tuple(d.items())))
        for u in tmp:
            ret["adjlist"][v]["edges"].append((u[0], dict(u[1])))

    V = vars_set(ret)
    if len(V) == 0:
        # we have projected everything out. time to reduce to a boolean
        F = final_set(ret)
        if len(F) > 0:
            # true!
            n = Automaton(bval=True)
            if debug > 1:
                print(n)
            return n
        else:
            n = Automaton(bval=False)
            if debug > 1:
                print(n)
            return n
    ret = Automaton(d=ret)
    if debug > 1:
        print(ret)
    return ret

def eval_truth(A, debug=0):
    if debug > 0:
        print("Evaluating. Machine currently has %d states" % A.num_states())
    # if A.is_boolean():
    #     return Automaton(bval=A.bval)
    # else:
    #     raise Exception("You did not enter a sentence. You probably have free variables.")
    return A
