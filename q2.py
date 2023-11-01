from z3 import *
import sys

input_path = sys.argv[1]

def color(V, E, k):
    # init solver
    s = Solver()
    
    # make vertex dictionary for z3 ints
    vmap = { vname: Int("v_" + str(vname)) for vname in V }

    # edge constraints: adjacent vertices never same color
    edge_constraints = [ Distinct(vmap[vi], vmap[vj]) for vi, vj in E ]
    s.add(edge_constraints)

    # vertex constraints: colour in (0, k-1)
    num_c = Int('k')
    vert_constraints = [ And(0 <= v, v < num_c) for v in vmap.values() ]    
    s.add(vert_constraints)
    
    def result(model):
        return {vname: model[vmap[vname]] for vname in V}

    # k=None: find min num of colors. k=(int): try coloring in (int) num of colors
    if k is not None:
        # add rule for num of colours, just check if SAT
        s.add(num_c == k)
        if s.check() == sat:
            return result(s.model())
        else:
            return False
    else:
        # min: 1 color, max: number of vertices
        k_min = 1
        k_max = len(V)
        
        # let's do binary search to find the minimum possible num of colors
        best_model = None
        best_k = 0
        while k_min <= k_max:
            s.push()                        # keep track
            k = int((k_min + k_max) / 2)      # midpt
            s.add(num_c == k)
            if s.check() == sat:            # if k is doable, then bring k_max to k-1 (and keep best_k = k)
                best_model = s.model()
                best_k = k
                k_max = k-1
            else:
                k_min = k+1                  # if k is not doable, bring k_min to k+1
            s.pop()

        return best_k, result(best_model)

def min_colors(V, E):
    k, _ = color(V, E, k=None)
    return k

if __name__ == '__main__':
    V = []
    E = []
    with open(input_path) as f:
        # if a line has 1 item, it is a vertex.
        # if a line has 2 items, it is an edge
        # all other cases, ignore.
        for line in f:
            record = line.split()
            if len(record) == 1:
                V.append(record[0])
            elif len(record) == 2:
                E.append((record[0], record[1]))
            else:
                print("Line of the file in unspecified format: ", line, " (Please use recommended format.)")
    m = min_colors(V, E)
    print("\nFor Graph G = (V, E) at location", input_path, ":")
    print("Minimum total number of colors required in a valid colouring of G =", m)
    print("Valid assignment of colors to vertex set V =", color(V, E, m),"\n")