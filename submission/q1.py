from z3 import *

def main():
    sol = Solver()

    # sort of brute force DFA construction method
    n = 15
    start = 0  # start node
    end = 14  # end node
    M = 7920   # a large number

    nodes = ['8,0,0', '5,0,3', '5,3,0', '2,3,3', '2,5,1',
            '7,0,1', '7,1,0', '4,1,3', '3,5,0', '3,2,3',
            '6,2,0', '6,0,2', '1,5,2', '1,4,3', '4,4,0']

    # this is like the initial matrix in algorithms like floyd warshall
    d = [[M, 1, M, M, M, M, M, M, 1, M, M, M, M, M, M],
        [M, M, 1, M, M, M, M, M, M, M, M, M, M, M, M],
        [M, M, M, 1, M, M, M, M, 1, M, M, M, M, M, M],
        [M, M, M, M, 1, M, M, M, M, M, M, M, M, M, M],
        [M, M, M, M, M, 1, M, M, 1, M, M, M, M, M, M],
        [M, M, M, M, M, M, 1, M, M, M, M, M, M, M, M],
        [M, M, M, M, M, M, M, 1, 1, M, M, M, M, M, M],
        [M, M, M, M, M, M, M, M, M, M, M, M, M, M, 1],
        [M, M, M, M, M, M, M, M, M, 1, M, M, M, M, M],
        [M, 1, M, M, M, M, M, M, M, M, 1, M, M, M, M],
        [M, M, M, M, M, M, M, M, M, M, M, 1, M, M, M],
        [M, 1, M, M, M, M, M, M, M, M, M, M, 1, M, M],
        [M, M, M, M, M, M, M, M, M, M, M, M, M, 1, M],
        [M, 1, M, M, M, M, M, M, M, M, M, M, M, M, 1],
        [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M]]


    # requirements (right hand statement)
    rhs = [Int("rhs["+str(i)+"]") for i in range(n)]
    for i in range(n):
        sol.add(rhs[i]>=(-1), rhs[i]<=1)

    x = {}
    for i in range(n):
        for j in range(n):
            x[i,j] = Int("x["+str(i)+","+str(j)+"]")
            sol.add(x[i,j]>=0, x[i,j]<=1)

    out_flow = [Int("out_flow["+str(i)+"]") for i in range(n)]
    in_flow = [Int("in_flow["+str(i)+"]") for i in range(n)]
    for i in range(n):
        sol.add(out_flow[i] >= 0, out_flow[i] <= 1, in_flow[i] >= 0, in_flow[i] <= 1)
    
    z = Int("z") # path length to be minimized 

    # constraints
    sol.add(z == Sum([d[i][j] * x[i, j] for i in range(n) for j in range(n) if d[i][j] < M]))

    # calculate rhs for each
    for i in range(n):
        if i == start:
            sol.add(rhs[i] == 1)
        elif i == end:
            sol.add(rhs[i] == -1)
        else:
            sol.add(rhs[i] == 0)

    # flow constraints
    for i in range(n):
        sol.add(out_flow[i] == Sum([x[i, j] for j in range(n) if d[i][j] < M]))
        sol.add(in_flow[i] == Sum([x[j, i] for j in range(n) if d[j][i] < M]))
        sol.add(out_flow[i] - in_flow[i] == rhs[i])

    # solution and search
    num_solutions = 0
    while sol.check() == sat:
        num_solutions += 1
        mod = sol.model()
        sol.add(z < mod.eval(z))

    def check(node1, node2):
        a1, b1, c1 = int(node1[0]), int(node1[2]), int(node1[4])
        a2, b2, c2 = int(node2[0]), int(node2[2]), int(node2[4])
        inc = '_'
        dec = '_'
        grad1, grad2, _ = a1-a2, b1-b2, c1-c2
        if grad1 > 0:
            inc = 'A'
            if grad2 < 0:
                dec = 'B'
            else:
                dec = 'C'
        elif grad1 < 0:
            dec = 'A'
            if grad2 > 0:
                inc = 'B'
            else:
                inc = 'C'
        else:
            if grad2 > 0:
                inc = 'B'
                dec = 'C'
            else:
                inc = 'C'
                dec = 'B'
        return inc, dec

    t = start
    i = 0
    while t != end:
        print("step "+str(i)+": A:"+str(nodes[t][0])+" B:"+str(nodes[t][2])+" C:"+str(nodes[t][4]))
        for j in range(n):
            if mod.eval(x[t, j]).as_long() == 1:
                f, t = check(nodes[j-1], nodes[j])
                print("transfer from",f,"to",t)
                if j == n-1:
                    # f, t = check(nodes[j-1], nodes[j])
                    # print("transfer from",f,"to",t)
                    print("step "+str(i+1)+": A:"+str(nodes[j][0])+" B:"+str(nodes[j][2])+" C:"+str(nodes[j][4]))
                # print(nodes[j])
                t = j
                break
        i+=1
    print("-------------------------\nMinimum total number of transfers:", i)
    print()

if __name__ == '__main__':
    main()