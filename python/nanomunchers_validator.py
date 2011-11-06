import sys,os
from nanomunchers_serialize import MuncherPresenter

class FormatValidator:
    def validate(self,programOutput):
        return self.parseAndValidate(programOutput)
    
    def parseAndValidate(self,programOutput):
        nanomunchers = int(programOutput[0])
        if(nanomunchers != len(programOutput[1:])):
            raise Exception('NanoMunchers dropped do not match the given count');
        
        munchPresenters = []
        for line in programOutput[1:]:
            presenter = line.split(' ')
            munchP = MuncherPresenter(int(presenter[0]),
                                      int(presenter[1]),
                                      int(presenter[2]),
                                      presenter[3])
            munchPresenters.append(munchP)
        return sorted(munchPresenters,key=lambda mp:mp.dropTime)

class Node:
    def __init__(self,nodeid,xloc,yloc,state):
        self.nodeid = nodeid
        self.xloc = xloc
        self.yloc = yloc
        self.state = state
        
class Simulation:

    def __init__(self,filename="inputsample"):
        refinedF = [line.replace('\n','').split(",") 
                    for line in open(filename,'r').readlines() 
                    if line!="\n" and
                    line.replace('\n','')!="nodeid,xloc,yloc" and
                    line.replace('\n','')!="nodeid1,nodeid2"]

        self.vertices = [lis for lis in refinedF if len(lis) == 3]
        self.edges = [lis for lis in refinedF if len(lis) ==2]

        self.remainingEdges = self.edges
        self.nodes = self.createNodes();
        self.munched = []
        self.StateConst = ["notmunched","munched"]
    
    def createNodes(self):
        nodes = {}
        for vertex in self.vertices:
            nodes[vertex[0]] = Node(vertex[0],vertex[1],
                                    vertex[2],self.StateConst[0])
        return nodes
    
    # time = 0
    # while nodesRemaining && munchersRemaining
    #   for each muncher in munchers
    #      if time == muncher.dropTime
    #        drop muncher on graph
    #   resolve conflicts (kill rookies and pick random rookies)
    #   for each muncher on the graph
    #      munch
    #      move
    #   resolve conflicts (up left down right precedence)
    #   time++
    #   
    def simulate(self,munchPresenters):
       for munchP in munchPresenters:
           if(not isRookie(munchP)):
               self.munchGraph(munchP)
           else:
               print "Muncher at (%d,%d) acted like a rookie, it's been killed." %
               (munchP.x,munchP.y)
       print "Nodes munched: %d out of %d" % (len(self.munched),len(self.vertices))
     
    def isRookie(self,munchP):
        for k,v in self.nodes:
            if(v.x == munchP.x and v.y == munchP.y and v.state != self.StateConst[0]):
                return True
        return False

    def munchGraph(self,munchP):
       while(not self.isBlackHole(munchP)):
           move = self.mutateMuncherPresenter(munchP)
           self.munched.append(self.nodes[move[1]])
           
           self.nodes[move[1]].state = self.StateConst[1]

           indexEdge = self.getEdgeIndex(move[0])
           if(indexEdge == -1):
               raise Exception("Attempt to erase an unexisting Edge.")
           del self.remainingEdges[indexEdge]
           
    def isBlackHole(self,munchP):
      initProgram = munchP.program
      count = 1
      while(count != 4):
          move = self.mutateMuncherPresenter(munchP)
          if(move != ()):
              self.restoreMuncherPresenter(munchP,initProgram)
              return True
          count += 1
      return False   


    def getEdgeIndex(self,edge):
        for i in range(0,self.remainingEdges):
            if(edges[0] == self.remainingEdges[i][0] and 
               edges[1] == self.remainingEdges[i][1]):
                return i
        return -1

    def mutateMuncherPresenter(self,munchP):
      move = self.tryMove(munchP)
      munchP.program = munchP.program[1:] + munchP.program[0]
      return move

    def restoreMuncherPresenter(self,munchP, initProgram):
      munchP.program = initProgram
          

    def tryMove(self,munchPresenter):
        direction = munchPresenter.program[0]
        x = munchPresenter.x
        y = munchPresenter.y

        if(direction == "L"):
            x = x-1
        elif(direction == "R"):
            x = x+1
        elif(direction == "D"):
            y = y-1
        elif(direction == "U"):
            y = y+1

        for edge in self.remainingEdges:
            node1 = self.nodes[edge[0]]
            node2 = self.nodes[edge[1]]
            if(self.isValidMove(x,y,node1)):
                return (edge,node1)
            elif(self.isValidMove(x,y,node2)):
                return (edge, node2)
                
        return ()
   
    # This function expects a tuple representing 
    # a nanomuncher id and direction the it was moving in
    def conflictSameNode(conflictedMunchPresenters):
       left = down = right = []
       
       for munchP in conflictedMunchPresneters:
           lastMove = munchP.program[-1]
           if(lastMove == "U"):
               return munchP
           elif(lastMove == "L"):
               left.append(munchP)
           elif(lastMove == "D"):
               down.append(munchP)
           elif(lastMove =="R"):
               right.append(munchP)
       
       if(len(left) != 0):
           return left[0]
       elif(len(down)!=0):
           return dowb[0]
       elif(len(right)):
           return right[0]
       return None        
       

    # This function resolves the conflicts between the nanomunchers 
    # dropped at the same time
    def conflictSameNodeDropTime(conflictedMunchPresenters):
       random.shuffle(conflictedMunchPresenters)
       return conflictedMunchPresenters[0]
  
            
     # Checks if the intent to move matches with the actual node
    def isValidMove(self,x,y,node):
        return (x == node.x and y == node.y and node.state==self.StateConst[0])
    

def runValidator(programOutput):
    munchPresenters = FormatValidator().validate(programOutput)
    Simulation().simulate(munchPresenters)
    

def main():
        programOutput = sys.stdin.read()
        if('' in programOutput):
            programOutput = programOutput.split('\n')[:-1]
        runValidator(programOutput)

if __name__ == "__main__":
    main();
