from belief_base import *
# from sympy import *
import itertools
import copy

B = BeliefBase()
B.add(Belief('a', 1))
B.add(Belief('b', 1))
B.add(Belief('a|b', 1))

def success():

    D = BeliefBase()
    D.add(Belief('p|q',1))
    # D.add(Belief('p',1))
    
    print(D.beliefs)
    
    D.revise(Belief('~p',1))
    # D.contract('p')

    print(D.beliefs)

def inclusion():

    D = copy.deepcopy(B)
    D.contract('a')

    print(B.beliefs)
    print(D.beliefs)

    print(f"Inclusion: {D.beliefs.issubset(B.beliefs)}")

    
def vacuity():

    

    D = copy.deepcopy(B)
    D.contract('s')



    print(B.beliefs)
    print(D.beliefs)

    print(f"Vacuity: {D.beliefs == B.beliefs}")

def consistency():

    # D = copy.deepcopy(B)
    D = BeliefBase()
    D.add(Belief('~p',1))
    D.add(Belief('p >> r',1))
    # D.add(Belief('r >> s',0.6))
    print(D.beliefs)

    D.revise(Belief('~r',1))

    # print(B.beliefs)
    print(D.beliefs)


def extensionality():

    # D = copy.deepcopy(B)
    D = BeliefBase()
    D.add(Belief('a',1))
    D.add(Belief('b',1))
    D.add(Belief('a>>b',1))
    D.add(Belief('b>>a',1))
    
    # print(D.beliefs)

    D.contract('a')

    print(D.beliefs)


# success()
inclusion()
vacuity()
consistency()
# extensionality()
