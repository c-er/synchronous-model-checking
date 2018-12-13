from collections import deque

def auto_succ(v1, v2):
    return {
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

def edge_merge(label1, label2):
    ret = {}
    for k in label1:
        if k in label2 and label1[k] != label2[k]:
            return None
        ret[k] = label1[k]
    for k in label2:
        ret[k] = label2[k]
    return ret

def cleanup_names(aut):
    num = 0
    d = {}
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

    return cleanup_names({
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

    return cleanup_names({
        "initial": (a["initial"], b["initial"]),
        "adjlist": adjlist
    })


xz = auto_succ("x", "z")
yz = auto_succ("y", "z")
xzyz = conj(xz, yz)
