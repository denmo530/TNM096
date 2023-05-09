import copy
import random


class Clause:
    def __init__(self, pos_lits=None, neg_lits=None):
        self.pos_lits = set(pos_lits) if pos_lits else set()
        self.neg_lits = set(neg_lits) if neg_lits else set()

    def __repr__(self):
        return f"Clause({self.pos_lits} {self.neg_lits})"

    def __eq__(self, other):
        return self.pos_lits == other.pos_lits and self.neg_lits == other.neg_lits

    def __hash__(self):
        return hash((frozenset(self.pos_lits), frozenset(self.neg_lits)))

    def subsumes(self, other):
        return self.pos_lits.issubset(other.pos_lits) and self.neg_lits.issubset(other.neg_lits)

    def proper_subsumes(self, other):
        return self.subsumes(other) and (self.pos_lits != other.pos_lits or self.neg_lits != other.neg_lits)

    def resolvent(self, other):
        A_copy = copy.deepcopy(self)
        B_copy = copy.deepcopy(other)

        common_pos = A_copy.pos_lits.intersection(B_copy.neg_lits)
        common_neg = A_copy.neg_lits.intersection(B_copy.pos_lits)

        if not common_pos and not common_neg:
            return False

        a = None
        if common_pos:
            a = random.choice(list(common_pos))
            A_copy.pos_lits.remove(a)
            B_copy.neg_lits.remove(a)
        else:
            a = random.choice(list(common_neg))
            A_copy.neg_lits.remove(a)
            B_copy.pos_lits.remove(a)

        C = Clause(A_copy.pos_lits.union(B_copy.pos_lits),
                   A_copy.neg_lits.union(B_copy.neg_lits))

        if C.pos_lits.intersection(C.neg_lits):
            return False

        # Remove duplicates
        C.pos_lits = set(filter(lambda l: l not in C.neg_lits, C.pos_lits))
        C.neg_lits = set(filter(lambda l: l not in C.pos_lits, C.neg_lits))

        return C


def solver(KB):
    while True:
        S = set()
        KB_copy = copy.deepcopy(KB)
        for A in KB:
            for B in KB:
                C = A.resolvent(B)
                if C is not False:
                    S = S.union({C})

        if not S:
            return KB

        KB = incorporate(S, KB)
        if KB_copy == KB:
            break

    return KB


def incorporate(S, KB):
    for A in S:
        KB = incorporate_clause(A, KB)
    return KB


def incorporate_clause(A, KB):
    for B in KB:
        if B.subsumes(A):
            return KB
    for B in KB.copy():
        if A.subsumes(B):
            KB.remove(B)

    KB = KB.union({A})
    return KB


if __name__ == "__main__":
    # Example 1: Resolving A = a ∨ b ∨ ¬c and B = c ∨ b
    A = Clause(['a', 'b'], ['c'])
    B = Clause(['b', 'c'])
    resolvent = A.resolvent(B)
    print(resolvent)  # Output: a, b

    # Example 2: Resolving A = a ∨ b ∨ ¬c and B = d ∨ b ∨ ¬g
    A = Clause(['a', 'b'], ['c'])
    B = Clause(['b', 'd'], ['g'])
    resolvent = A.resolvent(B)
    print(resolvent)  # Output: False

    # Example 3: Resolving A = ¬b ∨ c ∨ t and B = ¬c ∨ z ∨ b
    A = Clause(['c', 't'], ['b'])
    B = Clause(['b', 'z'], ['c'])
    resolvent = A.resolvent(B)
    print(resolvent)  # Output: False

    print("\n-----------------------------------------------\n")
    print("Subsumption Examples\n\n")
    # Subsumption
    # 1.
    A = Clause(['c', 'a'])
    B = Clause(['a', 'b', 'c'])
    result = A.proper_subsumes(B)
    print('Strict subset 1: ', result)

    # 2.
    A = Clause(['b'], ["c"])
    B = Clause(['a', 'b'], ["c"])
    result = A.proper_subsumes(B)
    print('Strict subset 2: ', result)

    # 3.
    A = Clause(['b'], ["f", "c"])
    B = Clause(['a', 'b'], ["c"])
    result = A.proper_subsumes(B)
    print('Strict subset 3: ', result)

    # 4.
    A = Clause(['b'])
    B = Clause(['a', 'b'], ["c"])
    result = A.proper_subsumes(B)
    print('Strict subset 4: ', result)

    # 5.
    A = Clause(['b', 'a'], ['c'])
    B = Clause(['a', 'b'], ["c"])
    result = A.proper_subsumes(B)
    result2 = A.subsumes(B)
    print('Strict subset 5: ', result)
    print('Subset 5: ', result2)

    print("\n-----------------------------------------------\n")
    print("Bob Examples\n\n")
    # Drawing conclusions
    # 1.
    C1 = Clause(["ice"], ["sun", "money"])
    C2 = Clause(["ice", "movie"], ["money"])
    C3 = Clause(["money"], ["movie"])
    C4 = Clause(neg_lits=["movie", "ice"])
    C5 = Clause(["sun", "money", "cry"])
    C6 = Clause(["movie"])
    # 2.
    KB = set({C1, C2, C3, C4, C5, C6})
    # 3.

    print("\nBob print\n")
    new_KB = solver(KB)
    for A in new_KB:
        print(A)

    print("\nSo, is A innocent or guilty?\n")
    # Task B - Robbery puzzle
    C1 = Clause(['A', 'B', 'C'], ["A", "B", "C"])
    C2 = Clause(['A'], ['C'])
    C3 = Clause(neg_lits=['B'])

    KB = set({C1, C2, C3})
    result = solver(KB)
    print('\nFinal Clauses: ')
    for C in result:
        print(C)
