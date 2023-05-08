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
        A_copy = copy.deepcopy(A)
        B_copy = copy.deepcopy(B)
        
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

            
        C = Clause(A_copy.pos_lits.union(B_copy.pos_lits), A_copy.neg_lits.union(B_copy.neg_lits))
        
        if C.pos_lits.intersection(C.neg_lits):
            return False
        
        # Remove duplicates 
        C.pos_lits = set(filter(lambda l: l not in C.neg_lits, C.pos_lits))
        C.neg_lits = set(filter(lambda l: l not in C.pos_lits, C.neg_lits))
        
        return C
        
if __name__ == "__main__": 
    # Example 1: Resolving A = a ∨ b ∨ ¬c and B = c ∨ b
    A = Clause(['a', 'b'], ['c'])
    B = Clause(['b', 'c'])
    resolvent = A.resolvent(B)
    print(resolvent) # Output: a, b

    # Example 2: Resolving A = a ∨ b ∨ ¬c and B = d ∨ b ∨ ¬g
    A = Clause(['a', 'b'], ['c'])
    B = Clause(['b', 'd'], ['g'])
    resolvent = A.resolvent(B)
    print(resolvent) # Output: False

    # Example 3: Resolving A = ¬b ∨ c ∨ t and B = ¬c ∨ z ∨ b
    A = Clause(['c', 't'], ['b'])
    B = Clause(['b', 'z'], ['c'])
    resolvent = A.resolvent(B)
    print(resolvent) # Output: False
