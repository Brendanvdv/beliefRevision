from sympy import *
import itertools


class Belief(object):
    def __init__(self, belief, entrenchment) -> None:
        self.belief = belief
        self.entrenchment = entrenchment

    def __str__(self) -> str:
        return f'{self.belief}: {self.entrenchment}'

    def __repr__(self) -> str:
        return f'{self.belief}: {self.entrenchment}'


class BeliefBase(object):

    def __init__(self, initial_beliefs=None) -> None:
        if initial_beliefs is not None:
            self.beliefs = initial_beliefs
        else:
            self.beliefs = set()

    # Add new belief to the belief base
    def add(self, belief):
        self.beliefs.add(belief)

    # Remove belief from the belief base
    def remove(self, belief):
        self.beliefs.remove(belief)

    # Check if the belief base entails a given formula, pseudo code from the book
    def entails(self, alpha, base=None):
        if base is not None:
            beliefs = base
        else:
            beliefs = self.beliefs

        # Convert to CNF and negate the formula
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

    # Delete all occurences of a literal from a set of literals
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

    def revision(self, belief):
        pass

    def contraction(self, belief, order):
        p = belief

        belief_update = []

        for q in self.beliefs:
            if q.entrenchment > order:
                if self.degree(p) == self.degree(Or(sympify(p), sympify(q.belief))):
                    belief_update.append((q, order))
        for belief, order in belief_update:
            self.remove(belief)
            if order > 0:
                belief.entrenchment = order
                self.add(belief)
        return self

    def degree(self, belief):
        # Degree of acceptance of belief according to BRA_AWilliams

        # tautology
        if self.entails(sympify(belief), []):
            return 1

        ordered_beliefs = {}

        # Sort beliefs by entrenchment and group them by entrenchment
        for _belief in sorted(self.beliefs, key=lambda x: x.entrenchment, reverse=True):
            if _belief.entrenchment not in ordered_beliefs:
                ordered_beliefs[_belief.entrenchment] = [_belief.belief]
            else:
                ordered_beliefs[_belief.entrenchment].append(_belief.belief)
        base = []
        # Check if the belief is entailed by the base
        for entrenchment, beliefs in ordered_beliefs.items():
            base += [sympify(_belief) for _belief in beliefs]
            if self.entails(sympify(belief), base=base):
                return entrenchment

        return 0

    def expansion(self, belief, order):

        p = belief

        #list of all same literals as the expansion
        list = [q for q in self.beliefs if p == q.belief]
        
        #removes duplicate literals and combines their order
        for q in list:
            self.remove(q)
            order += q.entrenchment

        self.add(Belief(belief, order))
        return self


    def expansion2(self, belief, order=None):
        if order is None:
            # set the order of the new belief to be higher than the highest order in the belief base
            if len(self.beliefs) == 0:
                order = 1
            else:
                order = max(belief.entrenchment for belief in self.beliefs) + 1
        self.add(Belief(belief, order))
        return self

    def __str__(self) -> str:
        return f'{self.beliefs}'

    def __repr__(self) -> Set:
        return self.beliefs


bb = BeliefBase(set([Belief('p', 0.2), Belief('q', 0.3),
                Belief('a|c', 0.5), Belief('a&d', 0.9)]))

# bb = BeliefBase(set([Belief('p', 0.2), Belief('q', 0.3)]))

print(bb)
# print(bb.contraction('q', 0.1))
# print(bb.contraction('q', 0.1))
print(bb.expansion('s', 0.1))

