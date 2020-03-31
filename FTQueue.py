
class FTQueue:

    def __init__(self,qId):
        self.qId=qId
        self.q = list()
    
    def qPush(self,element):
        self.q.append((element))
    
    def qTop(self):
        return self.q[len(self.q)-1]

    def qPop(self):
        top_element = self.qTop()
        self.q.pop()
        return top_element

    def qSize(self):
        return len(self.q)
    
    def qId():
        return self.qId
    def qPrint(self):
        print("elements in QueueID %d" % self.qId)
        for l in self.q:
            print(l)

