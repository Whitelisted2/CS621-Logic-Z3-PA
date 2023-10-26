from z3 import *
import sys

input_path = sys.argv[1]

A = [] # availability matrix

def appointment_scheduling(m):
    s = Solver()
    n = len(m)

    # constraints to establish domain of matrix
    x = {}
    for i in range(n):
        for j in range(n):
            x[(i, j)] = Int("x_" + str(i) + "_" + str(j))
            s.add(x[(i, j)] >= 0, x[(i, j)] <= 1) 
            
    # more constraints
    for i in range(n):
        # ensure agreement with availability matrix
        s.add(Sum([m[i][j] * x[(i,j)] for j in range(n)]) == 1)
        # ensure one assignment per timeslot, and per person
        s.add(Sum([x[(i,j)] for j in range(n)]) == 1)
        s.add(Sum([x[(j,i)] for j in range(n)]) == 1)

    num_sol = 0
    while s.check() == sat:
        num_sol += 1
        mod = s.model()
        for i in range(n):
            for j in range(n):
                print(mod[x[(i,j)]],end=" ")
            print("")
        print("")
        s.add(Or([x[(i,j)] != mod[x[(i,j)]] for i in range(n) for j in range(n)]))

    print("num_solutions:", num_sol)

if __name__ == "__main__":
    with open(input_path) as f:
        N = 0
        for line in f:
            N = len(line.split())
            A.append(line.split())
        i = 0
        for row in A:
            j = 0
            for entry in row:
                A[i][j] = int(A[i][j])
                j+=1
            i+=1
        appointment_scheduling(A)