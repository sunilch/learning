import functools

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return functools.update_wrapper(d(fn), fn)
    return _d
decorator = decorator(decorator)

@decorator
def memo(f):
    """Decorator that caches the return value for each call to f(args).
    Then when called again with same args, we can just look it up."""
    cache = {}
    def _f(*args):
        try:
            return cache[args]
        except KeyError:
            result = f(*args)
            cache[args] = result
            return result
        except TypeError:
            # some element of args can't be a dict key
            return f(*args)
    _f.cache = cache
    return _f

def fillGlass(holdings,capacities,whichone):
    '''
    Fills one of the glass to the full from the tap
    :param holdings: tuple of current holding of glasses
    :param holdings: tuple of capacity of glasses
    :param holdings: Which glass needs to be filled
    :return: tuple with one glass filled and the second untouched
    '''
    holdingsnew=holdings[:]
    filledAmount=capacities[whichone]-holdings[whichone]
    if filledAmount==0:
        print 'raising in fill '+str(whichone)
        raise OverflowError
    holdingsnew[whichone]=capacities[whichone]
    doc='Filled glass '+str(whichone+1)+' by adding '+str(filledAmount)
    return holdingsnew,doc

def emptyGlass(holdings,capacities,whichone):
    '''
    Empties one of the glass in to the sink
    :param holdings: tuple of current holding of glasses
    :param capacities: tuple of capacity of glasses
    :param whichone: Which glass needs to be emptied
    :return: tuple with one glass emptied and the second untouched
    '''
    holdingsnew=holdings[:]
    emptiedAmount=holdings[whichone]
    if emptiedAmount==0:
        print 'raising in empty '+str(whichone)
        raise OverflowError
    holdingsnew[whichone]=0
    doc='Emptied glass '+str(whichone+1)+' by removing '+str(emptiedAmount)
    return holdingsnew,doc

def transfer(holdings,capacities,source):
    '''
    Transfers the water from the source glass to the other as much as possible
    :param holdings: tuple of current holding of glasses
    :param capacities: tuple of capacity of glasses
    :param source: Which glass needs to be acting as the source
    :return: tuple of holdings after source transfers its water to the other
    '''
    holdingsnew=holdings[:]
    sink=1-source
    transferAmount=min(holdings[source],capacities[sink]-holdings[sink])
    if transferAmount==0:
        print 'raising in transfer ',str(source)
        raise OverflowError
    holdingsnew[source]=holdings[source]-transferAmount
    holdingsnew[sink]=holdings[sink]+transferAmount
    doc='Transfered '+str(transferAmount)+' from glass '+str(source+1)+' to glass '+str(sink+1)
    return holdingsnew,doc

def makeTransfer(holdings,capacities):
    '''

    :param holdings:
    :param capacities:
    :return:
    '''
    holdingList=[]
    actionList=[]
    for i in range(2):
        try:
            newholdings,newaction=fillGlass(holdings,capacities,i)
            holdingList.append(newholdings)
            actionList.append(newaction)
        except OverflowError:
            pass
        try:
            newholdings,newaction=emptyGlass(holdings,capacities,i)
            holdingList.append(newholdings)
            actionList.append(newaction)
        except OverflowError:
            pass
        try:
            newholdings,newaction=transfer(holdings,capacities,i)
            holdingList.append(newholdings)
            actionList.append(newaction)
        except OverflowError:
            pass
    return holdingList,actionList

def solve(holdings,capacities,targetHolding):
    '''
    Solves the water pouring problem with starting at the state as indicated by holdings
    :param holdings: tuple of current holding of glasses
    :param capacities: tuple of capacity of glasses
    :param targetHolding: target we want to achieve for holding
    :return: list of string of actions
    '''
    #print targetHolding,holdings
    if targetHolding > sum(capacities) or targetHolding < 0:
        return ['Not Possible']
    elif targetHolding in holdings:
        return ['Done']
    else:
        holdingSet,actionSet=makeTransfer(holdings,capacities)
        print holdingSet
        print actionSet
        return ['1']
        for counter,possibleHoldings in enumerate(holdingSet):
            possibleAction=actionSet[counter]
            nowList=solve(possibleHoldings,capacities,targetHolding)
            if counter==0:
                bestAction=possibleAction
                bestList=nowList
            else:
                if len(bestList)>len(nowList):
                    bestList=nowList
                    bestAction=possibleAction
        return [bestAction]+bestList

if __name__=='__main__':
    print '-'.join(solve([0,0],[9,4],4))

