from collections import deque

class Automaton:
    def __init__(self, d, verify=False):
        if verify:
            # do verification of d
            pass
        self.aut = d

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

def product_bfs(a, b, disj=False):
    adjlist = {}

    q = deque([(a["initial"], b["initial"])])

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
        "initial": (a["initial"], b["initial"]),
        "adjlist": adjlist
    })

def disj(A, B):
    return Automaton(product_bfs(A.aut, B.aut, disj=True))

def conj(A, B):
    return Automaton(product_bfs(A.aut, B.aut, disj=False))

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

def neg(A):
    det = determinize(A.aut)
    for v in det["adjlist"]:
        det["adjlist"][v]["final"] = not det["adjlist"][v]["final"]
    return Automaton(det)

def exists(var, A):
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
        for e in a["adjlist"][v]["edges"]:
            d = dict(e[1])
            del d[var]
            ret["adjlist"][v]["edges"].append((e[0], d))

    return Automaton(ret)

def eval_truth(A):
    aut = A.aut
    if len(vars_set(aut)) > 0:
        raise Exception("Trying to evaluate truth of automaton with tracks")
    for v in aut["adjlist"]:
        if aut["adjlist"][v]["final"]:
            return True
    return False
