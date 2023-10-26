from z3 import *

s = Solver()
a = Int('a')
s.add(a == 3)

a+=3

s.add(a == 5)

print(s.check(), s.assertions())
