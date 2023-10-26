from z3 import *

# state vars
a, b, c = Ints('a b c')

# Allocate variables for moves
moves = [Int('mv_' + str(cnt)) for cnt in range(100)]

# pick an arbitrary rule and apply it to the state
def move(cnt):
    global a, b, c
    mv = moves[cnt]
    if s.check() == sat:
        # print(s.model())
        pass
    s.add(mv >= 1)
    s.add(mv <= 6)
    # print(cnt, mv)
    a = If(mv == 1, a - If(b > 5 - a, 5 - a, b),
           If(mv == 2, a - If(c > 3 - a, 3 - a, c),
              If(mv == 3, a + b,
                 If(mv == 4, a + c, a))))
    b = If(mv == 1, If(a + b > 5, 5, a + b),
           If(mv == 2, b,
              If(mv == 3, 0,
                 If(mv == 4, b,
                    If(mv == 5, b - If(c > 5 - b, 5 - b, c),
                       If(c + b > 3, 3, c + b))))))
    c = If(mv == 1, c,
           If(mv == 2, If(a + c > 3, 3, a + c),
              If(mv == 3, c,
                 If(mv == 4, 0,
                    If(mv == 5, If(b + c > 5, 5, b + c),
                       c - If(b > 3 - c, 3 - c, b))))))

# Create a Z3 solver instance
s = Solver()

# Initialize the puzzle's initial state
s.add(a == 8, b == 0, c == 0)

# Solve the puzzle
cnt = 0

cap_a = 8
cap_b = 5
cap_c = 3
temp_a = 8
temp_b = 0
temp_c = 0
temp_step = 0
def printabc(a, b, c):
    print("A:"+str(a)+" B:"+str(b)+" C:"+str(c), end="")
def printRule(i):
    global temp_a, temp_b, temp_c, temp_step, cap_a, cap_b, cap_c
    if i == 1:
        print("transfer from A to B")
        pour_qty = min([temp_a, cap_b - temp_b])
        temp_a -= pour_qty
        temp_b += pour_qty
    elif i == 2:
        print("transfer from A to C")
        pour_qty = min([temp_a, cap_c - temp_c])
        temp_a -= pour_qty
        temp_c += pour_qty
    elif i == 3:
        print("transfer from B to A")
        temp_a += temp_b
        temp_b = 0
    elif i == 4:
        print("transfer from C to A")
        temp_a += temp_c
        temp_c = 0
    elif i == 5:
        print("transfer from B to C")
        pour_qty = min([cap_c - temp_c, temp_b])
        temp_b -= pour_qty
        temp_c += pour_qty
    elif i == 6:
        print("transfer from C to B")
        pour_qty = min([temp_c, cap_b - temp_b])
        temp_b += pour_qty
        temp_c -= pour_qty
    print("step " + str(i) + ": ", end="")
    printabc(temp_a, temp_b, temp_c)
    print()

        

def solvePuzzle():
    global cnt
    global a
    if cnt == 50:
        print("Count reached 100, no solution found.")
    else:
        move(cnt)
        cnt+=1
        s.push()
        s.add(a == 4, b == 4, c == 0)
        if s.check() == sat:
            # solved, print the moves:
            print("Solution found in step: %d" % cnt)
            m = s.model()
            print(m)
            print("step 0: A:8 B:0 C:0")
            for i in range(cnt):
                d = m[moves[i]].as_long()
                print(d)
                printRule(d)
                # print("%3d. %s" % (i+1, ("rule 1", "rule 2", "rule 3", "rule 4", "rule 5", "rule 6")[d - 1]))
        else:
            print("No solutions with "+ str(cnt) + " moves")
            s.pop()
            solvePuzzle()


solvePuzzle()
