from sympy import *
import itertools


class Belief(object):
    def __init__(self, belief, order) -> None:
        self.belief = to_cnf(sympify(belief))
        self.order = order

    def __str__(self) -> str:
        return f'{self.belief}: {self.order}'

    def __repr__(self) -> str:
        return f'{self.belief}: {self.order}'


class BeliefBase(object):

    def __init__(self, initial_beliefs=None, orders=None) -> None:
        if initial_beliefs is not None:
            self.beliefs = initial_beliefs
            self.orders = orders
        else:
            self.beliefs = set()
            self.orders = {}

    # Add new belief to the belief base
    def add(self, belief):
        self.beliefs.add(belief.belief)
        self.orders[str(belief.belief)] = belief.order

    # Remove belief from the belief base
    def remove(self, belief):
        self.beliefs.remove(belief)
        del self.orders[str(belief)]

    # Check if the belief base entails a given formula, pseudo code from the book
    def entails(self, alpha, base=None):
        if base is not None:
            beliefs = list(base)
        else:
            beliefs = [belief.belief for belief in list(self.beliefs)]
        # Convert to CN F and negate the formula
        if len(beliefs) == 0:
            formula = ~alpha
        elif len(beliefs) == 1:
            formula = to_cnf(beliefs[0] & ~alpha)
        else:
            formula = to_cnf(And(*beliefs) & ~alpha)
        clauses = self.get_clauses(formula)  # Get all clauses from the formula

        new = set()
        while True:
            pairs = [pair for pair in itertools.combinations(
                clauses, 2)]  # Get all pairs of clauses
            for (ci, cj) in pairs:
                # Get all resolvents from the pair
                resolvents = self.pl_resolve(ci, cj)
                if False in resolvents:  # If there is a resolvent that is False, then the formula is entailed
                    return True
                new = new.union(set(resolvents))
            # If there are no new resolvents, then the formula is not entailed
            if new.issubset(set(clauses)):
                return False

            clauses = clauses.union(new)

    # Get all resolvents from a pair of clauses
    def pl_resolve(self, ci, cj):
        resolvents = set()
        for di in self.get_literals(ci):
            for dj in self.get_literals(cj):
                if di == ~dj or ~di == dj:  # If the literals are negations of each other, then they can be resolved
                    resolvents.add(
                        Or(*self.unique(self.delete_all(di, self.get_literals(ci)) + self.delete_all(dj, self.get_literals(cj)))))  # Add the resolvent to the set of resolvents
        return resolvents

    def implies(self, alpha, beta):
        return self.entails(Or(~alpha, beta))

    def delete_all(self, element, iterable):
        # Delete all occurences of a literal from a set of literals
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

    def contract(self, belief):
        # Delete the belief from the belief base

        formula = to_cnf(belief)

        r = []
        for _belief in self.beliefs:
            # check if removing the belief from the belief base entails the formula
            if self.beliefs - {_belief} and not self.entails(formula, self.beliefs - {_belief}):
                # _belief can be removed
                r.append((self.beliefs - {_belief}))

        if not r:
            # if no belief can be removed, then simply remove the selected belief
            self.beliefs = self.beliefs - {belief}
            if str(belief) in self.orders:
                del self.orders[str(belief)]
            return

        # select a belief set to remove based on the order of the beliefs
        selected = self.select(r)

        self.beliefs = set()
        temp = self.orders
        self.orders = {}

        # update the belief base and the order of the beliefs
        for s in selected:
            self.beliefs |= s
            for belief in s:
                self.orders[str(belief)] = temp[str(belief)]
        return self.beliefs

    def select(self, remainders):
        if not remainders:
            return []

        selected = []
        # sum the orders in a set
        orders = [sum([self.orders[str(belief)]
                       for belief in remainder]) for remainder in remainders]

        # select the set with the highest order
        for i in range(len(remainders)):
            if orders[i] == max(orders):
                selected.append(remainders[i])

        return selected

    def clean(self):
        self.beliefs = set()
        self.orders = {}

    def get_clauses(self, formula):
        if isinstance(formula, And):
            clauses = set()
            for arg in formula.args:
                clauses |= self.get_clauses(arg)
            return clauses
        else:
            return {formula}

    def revise(self, belief):
        self.contract(~belief.belief)
        self.add(belief)
        return self.beliefs

    def expand(self, belief):
        self.add(belief)

    def __str__(self) -> str:
        return f'{self.beliefs}'

    def __repr__(self) -> Set:
        return self.beliefs
