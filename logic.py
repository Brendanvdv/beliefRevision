from sympy import *


def resolution(beliefs, alpha):
    formula = to_cnf(beliefs & ~alpha)
    clauses = get_clauses(formula)
    new = set()
    while True:
        pairs = [(clauses[i], clauses[j]) for i in range(len(clauses))
                 for j in range(i + 1, len(clauses))]
        for (ci, cj) in pairs:
            resolvents = pl_resolve(ci, cj)
            if False in resolvents:
                return True
            new = new.union(set(resolvents))


def pl_resolve(ci, cj):
    resolvents = set()
    for di in get_literals(ci):
        for dj in get_literals(cj):
            if di == -dj or -di == dj:
                resolvents.add(associate(Or, unique(remove_all(di, get_literals(ci)) +
                                                    remove_all(dj, get_literals(cj)))))
    return resolvents


def remove_all(element, iterable):
    return [item for item in iterable if item != element]


def unique(iterable):
    return list(set(iterable))


def associate(op, args):
    if len(args) == 0:
        if op == And:
            return True
        elif op == Or:
            return False
    elif len(args) == 1:
        return args[0]
    else:
        return op(*args)


def get_literals(formula):
    if isinstance(formula, Symbol):
        return {formula}
    elif isinstance(formula, Not):
        return {-formula.args[0]}
    else:
        literals = set()
        for arg in formula.args:
            literals |= get_literals(arg)
        return literals


def get_clauses(formula):
    if isinstance(formula, And):
        clauses = set()
        for arg in formula.args:
            clauses |= get_clauses(arg)
        return clauses
    else:
        return {formula}


p = Symbol('p')
q = Symbol('q')
r = Symbol('r')
s = Symbol('s')

print(pl_resolve(p | ~q, p | q))
