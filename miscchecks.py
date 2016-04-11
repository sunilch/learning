import random


def deal(numhands, n=5, deck=mydeck):
    # Your code here.
    handlist=[[] for elem in xrange(5)]
    random.shuffle(deck)
    smalldeck=deck[:25]
    for cnt,elem in enumerate(smalldeck):
        handlist[cnt%5].append(elem)
    return handlist

if __name__=='__main__':
    mydeck = [r+s for r in '23456789TJQKA' for s in 'SHDC']
    deal(5,deck=mydeck)