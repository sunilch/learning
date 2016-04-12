
class Explore(object):
    '''
    Base class for all explorations
    '''
    def __init__(self,searchName):
        self.searchName=searchName
        pass

    def generateNodes(self,inputNode):
        raise NotImplementedError

    def StageNodes(self,listofNodes):
        raise NotImplementedError

    def UnstageNode(self):
        raise NotImplementedError

    def GoalTest(self,inputNode):
        raise NotImplementedError

    def explore(self,startNode):
        raise NotImplementedError

class BFS(Explore):
    '''
    Outline for Breadth First Search
    '''
    def __init__(self,nodeDedup=True):
        super(BFS,self).__init__()
        self.nodeDedup=nodeDedup
        self.stageQ=[]

    def StageNodes(self,listofPaths):
        self.stageQ

if __name__=="__main__":
    exploreObj=Explore()
