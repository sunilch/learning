#------------------
# User Instructions
#
# Hopper, Kay, Liskov, Perlis, and Ritchie live on
# different floors of a five-floor apartment building.
#
# Hopper does not live on the top floor.
# Kay does not live on the bottom floor.
# Liskov does not live on either the top or the bottom floor.
# Perlis lives on a higher floor than does Kay.
# Ritchie does not live on a floor adjacent to Liskov's.
# Liskov does not live on a floor adjacent to Kay's.
#
# Where does everyone live?
#
# Write a function floor_puzzle() that returns a list of
# five floor numbers denoting the floor of Hopper, Kay,
# Liskov, Perlis, and Ritchie.

import itertools

def floor_puzzle():
    # Your code here
    top=1
    bottom=5
    for (Hopper, Kay, Liskov, Perlis, Ritchie) in itertools.permutations(range(1,6)):
        if Hopper is not top:
            if Kay is not bottom:
                if Liskov not in [top,bottom]:
                    if Perlis>Kay:
                        if abs(Ritchie-Liskov)>1:
                            if abs(Liskov-Kay)>1:
                                break
    return [Hopper, Kay, Liskov, Perlis, Ritchie]

def test():
    print floor_puzzle()

test()