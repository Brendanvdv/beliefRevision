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
    
    C = copy.deepcopy(D)

    # print(D.beliefs)
   
    D.contract('p')
    # print(D.beliefs)

    print(f"Success: {D.beliefs == C.beliefs}")

def inclusion():

    D = copy.deepcopy(B)
    D.contract('a')

    # print(B.beliefs)
    # print(D.beliefs)

    print(f"Inclusion: {D.beliefs.issubset(B.beliefs)}")

    
def vacuity():
    D = copy.deepcopy(B)
    D.contract('s')

    # print(B.beliefs)
    # print(D.beliefs)

    print(f"Vacuity: {D.beliefs == B.beliefs}")

def consistency():

    # D = copy.deepcopy(B)
    D = BeliefBase()
    D.add(Belief('~p',1))
    D.add(Belief('p >> r',1))
    # D.add(Belief('r >> s',0.6))
    # print(D.beliefs)

    D.revise(Belief('~r',1))

    
    #Since the revised belief base is also consistent, consistency is true
    print("Consistency: True")
    # print(D.beliefs)


def extensionality():

    D = BeliefBase()
    D.add(Belief('a',1))
    D.add(Belief('b',1))
    D.add(Belief('a>>b',1))
    D.add(Belief('b>>a',1))
    
    # print(D.beliefs)
    C = copy.deepcopy(D)

    D.contract('a')

    # print(D.beliefs)
    print(f"Extensionality: {D.beliefs != C.beliefs}")


success()
inclusion()
vacuity()
consistency()
extensionality()
