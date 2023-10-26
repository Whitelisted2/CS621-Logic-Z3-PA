from z3 import *
from numpy.random import *
import sys

input_path = None
default_size = 5

A = [] # availability matrix

def schedule(m):
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
    if s.check() == sat:
        print("The interviews are schedulable for the given binary matrix! :)")
    else:
        print("Unfortunately, there is no scenario where every single candidate gets a timeslot. :(\n")

    while s.check() == sat:
        num_sol += 1
        print("Possible Solution "+str(num_sol)+":")
        mod = s.model()
        for i in range(n):
            for j in range(n):
                print(mod[x[(i,j)]],end=" ")
            print("")
        print("")
        s.add(Or([x[(i,j)] != mod[x[(i,j)]] for i in range(n) for j in range(n)]))
    
    print("Number of solutions:", num_sol)

if __name__ == "__main__":
    if(len(sys.argv) >= 2):
        input_path = sys.argv[1]
    else:
        input_path = None
    if input_path != None:
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
            schedule(A)
    else:
        A = choice([0, 1], size=(default_size, default_size))
        print("Randomly Generated Availability Matrix:")
        print(A)
        print()
        schedule(A)