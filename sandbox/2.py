# code from stack overflow by user 'alias', in response to a question about encoding game rules using z3

from z3 import *

# The state. In your case, you seem to have 12 values. For
# simplicity, here I'll just use one integer value.
a = Int('a')

# Rules of the game. Instead of swapping things around,
# I'll simply use a few arithmetic operations to represent
# the next value the state can take
def rule1(v):
    # print(v)
    return v+1

def rule2(v):
    return v-3

def rule3(v):
    return v*2

# Allocate vars for moves. Allow for 100 moves at most.

moves = [Int('mv_' + str(cnt)) for cnt in range(100)]

# A move picks an arbitrary rule, and applies it
# to the state. We take a cnt argument, counting the moves.
def move(cnt):
    global a
    mv = moves[cnt]
    if s.check() == sat:
        # print(s.model())
        pass
    s.add(mv >= 1)
    s.add(mv <= 3)
    print(cnt, mv)
    a = If(mv == 1, rule1(a),
        If(mv == 2, rule2(a),
                    rule3(a)));

s = Solver()

# Record the beginning state
s.add(a == 0)

cnt = 0
# To solve, we simply iterate and see if we reach the final state.
def solvePuzzle():
    global cnt
    global a
    if cnt == 100:
       print("Count reached 100, no solution found.")
    else:
       move(cnt)
       cnt = cnt+1
       # Check if the state implies the end condition
       # that a is 73. (Arbitrarily chosen for example.)
       s.push()
       s.add(a == 73)
       if s.check() == sat:
           # solved, print the moves:
           print("Solution found in step: %d" % cnt)
           m = s.model()
        #    print(m)
           for i in range(cnt):
               d = m[moves[i]].as_long()
               print("%3d. %s" % (i+1, ("rule 1", "rule 2", "rule 3")[d - 1]))
       else:
           print("No solutions with %d moves" % cnt)
           s.pop()
           solvePuzzle()

solvePuzzle()