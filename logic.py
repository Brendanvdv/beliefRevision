from sympy import *
import itertools


class BeliefBase(object):

    def __init__(self, initial_beliefs=None):
        if initial_beliefs is not None:
            self.beliefs = initial_beliefs
        else:
            self.beliefs = set()

    def add(self, belief):
        self.beliefs.add(belief)

    def remove(self, belief):
        self.beliefs.remove(belief)

    def entails(self, alpha):
        formula = to_cnf(And(*self.beliefs) & ~alpha)
        clauses = self.get_clauses(formula)
        new = set()
        while True:
            pairs = [pair for pair in itertools.combinations(clauses, 2)]
            for (ci, cj) in pairs:
                resolvents = self.pl_resolve(ci, cj)
                if False in resolvents:
                    return True
                new = new.union(set(resolvents))
            if new.issubset(set(clauses)):
                return False

            clauses = clauses.union(new)

    def pl_resolve(self, ci, cj):
        resolvents = set()
        for di in self.get_literals(ci):
            for dj in self.get_literals(cj):
                if di == ~dj or ~di == dj:
                    resolvents.add(
                        Or(*self.unique(self.delete_all(di, self.get_literals(ci)) + self.delete_all(dj, self.get_literals(cj)))))
        return resolvents

    def delete_all(self, element, iterable):
        return [item for item in iterable if item != element]

    def unique(self, iterable):
        return list(set(iterable))

    def get_literals(self, formula):
        if isinstance(formula, Symbol) or isinstance(formula, Not):
            return {formula}
        else:
            literals = set()
            for arg in formula.args:
                literals |= self.get_literals(arg)
            return literals

    def get_clauses(self, formula):
        if isinstance(formula, And):
            clauses = set()
            for arg in formula.args:
                clauses |= self.get_clauses(arg)
            return clauses
        else:
            return {formula}


p = Symbol('p')
q = Symbol('q')
r = Symbol('r')
s = Symbol('s')


bb = BeliefBase({~p | q, p})

print(bb.entails(p))
