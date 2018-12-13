from collections import deque

def auto_succ(v1, v2):
    return {
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
    }

def auto_eq(v1, v2):
    return {
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
    }

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
        "initial": d[aut["initial"]],
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

def disj(a, b):
    adjlist = {}

    q = deque([(a["initial"], b["initial"])])

    while len(q) > 0:
        asrc, bsrc = q.pop()
        edges_a = a["adjlist"][asrc]["edges"]
        edges_b = b["adjlist"][bsrc]["edges"]


        if (asrc, bsrc) not in adjlist:
            adjlist[(asrc, bsrc)] = {
                "final": a["adjlist"][asrc]["final"] or b["adjlist"][bsrc]["final"],
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
        "initial": (a["initial"], b["initial"]),
        "adjlist": adjlist
    })


def conj(a, b):
    adjlist = {}

    q = deque([(a["initial"], b["initial"])])

    while len(q) > 0:
        asrc, bsrc = q.pop()
        edges_a = a["adjlist"][asrc]["edges"]
        edges_b = b["adjlist"][bsrc]["edges"]


        if (asrc, bsrc) not in adjlist:
            adjlist[(asrc, bsrc)] = {
                "final": a["adjlist"][asrc]["final"] and b["adjlist"][bsrc]["final"],
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
        "initial": (a["initial"], b["initial"]),
        "adjlist": adjlist
    })

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


def determinize(a):
    adjlist = {}

    q = deque([frozenset([a["initial"]])])

    F = final_set(a)

    labels = all_labels(vars_set(a), a["alphabet"])

    while len(q) > 0:
        src = q.pop()
        ve = set()

        if src not in adjlist:
            adjlist[src] = {
                "final": len(src & F) > 0,
                "edges": []
            }
        for u in src:
            for l in labels:
                S = frozenset(map(lambda x: x[0], filter(lambda x: x[1] == l, a["adjlist"][u]["edges"])))
                adjlist[src]["edges"].append((S, l))
                if S not in adjlist:
                    q.appendleft(S)

    return cleanup({
        "initial": frozenset([a["initial"]]),
        "adjlist": adjlist
    })

def neg(a):
    det = determinize(a)
    for v in det["adjlist"]:
        det["adjlist"][v]["final"] = not det["adjlist"][v]["final"]
    return det

def exists(var, a):
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
        for e in a["adjlist"][v]["edges"]:
            d = dict(e[1])
            del d[var]
            ret["adjlist"][v]["edges"].append((e[0], d))

    return ret

def eval_truth(aut):
    if len(vars_set(aut)) > 0:
        raise Exception("Trying to evaluate truth of automaton with tracks")
    for v in aut["adjlist"]:
        if aut["adjlist"][v]["final"]:
            return True
    return False

xz = auto_succ("x", "z")
yz = auto_succ("y", "z")
xeqy = auto_eq("x", "y")
xzyz = conj(xz, yz)
xny = neg(xeqy)
mat = conj(xzyz, xeqy)
form = exists("x", exists("y", exists("z", mat)))
