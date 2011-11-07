import sys,random
from nanomunchers_serialize import MuncherPresenter

class NanoMunchers(MuncherPresenter):
    def __init__(self,dropTime,x,y,state):
        MuncherPresenter.__init__(dropTime,x,y)
        self.state = state

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

class States:
    init=0
    drop=1
    munch=2
    blackhole=3

class NodeState:
    notMunched=0
    munched=1        

class Simulation:

    def __init__(self,filename):
        refinedF = [line.replace('\n','').split(",") 
                    for line in open(filename,'r').readlines() 
                    if line!="\n" and
                    line.replace('\n','')!="nodeid,xloc,yloc" and
                    line.replace('\n','')!="nodeid1,nodeid2"]

        self.vertices = [lis for lis in refinedF if len(lis) == 3]
        self.edges = [lis for lis in refinedF if len(lis) ==2]
        self.time =0
        self.nodes = self.createNodes();
        self.munched = 0
        self.totalNodes = len(self.vertices)
        self.nanoMunchers = []
    
    def createNodes(self):
        nodes = {}
        for vertex in self.vertices:
            nodes[vertex[0]] = Node(vertex[0],vertex[1],
                                    vertex[2],NodeState.notMunched)
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
    def simulate(self,nanoMunchers):
       
        # 1) we begin with dropping nanomunchers, resolving the conflicts
        # 2) munch, move and increment time step.
        # if there's no nanomunchers that are dropped then:
        # conflict resolution after move, killing of rookies and removal of blackholes become 1
        # for the subsequent time steps.
       
        while len(self.nodes) != 0 and len(nanoMunchers) != 0:
            #drop
            for nanoMuncher in nanoMunchers:
                if(self.time == nanoMuncher.dropTime):
                    nanoMuncher.state = States.drop
            #resolve conflicts, some nanomunchers will be killed.
            self.conflictDropTime(nanoMunchers) # Nanomunchers dropped at the same node.
            
            blackholes = []
            for nanoMuncher in nanoMunchers:
                if(self.time > nanoMuncher.dropTime):
                    #munch
                    self.markNodeMunched(nanoMuncher)
                    self.munched +=1
                    #move
                    didMove = self.moveNanoMuncher(nanoMuncher)
                    # if canot move, then make it a blackhole.
                    if(not didMove):
                        blackholes.append(nanoMuncher)
            
            self.time += 1
            
            #post processing:
            #resolve conflicts, some nanomunchers will be killed.
            self.conflictSameNode(nanoMunchers) # NanoMunchers moved to the same node.
            #remove rookies, rookies will be killed and removed.
            self.removeRookies(nanoMunchers) # NanoMunchers moved to the node that was already munched.
            #remove blackholes
            self.removeAll(nanoMunchers,blackholes) # remove all blackholes.
            
        print "Total nodes munched: %d out of: %d in time: %d" % (self.munched,self.totalNodes,self.time)
    
    # This helps in identifying rookies, if the nanomuncher tries to munch an already
    # node then it is declared as rookie and is killed.
    def markNodeMunched(self,nanoMuncher):
        for k,v in self.nodes.iteritems():
            if(v.x == nanoMuncher.x and 
                v.y == nanoMuncher.y):
                self.nodes[k].state = NodeState.munched

    #This function checks for rookies.
    def removeRookies(self,nanoMunchers):
        rookies=[]
        for nanoMuncher in nanoMunchers:
            if(nanoMuncher.dropTime < self.time 
               and self.isRookie(nanoMuncher)):
                rookies.append(nanoMuncher)
        self.removeAll(nanoMunchers,rookies)

    # Rookie condition: the destination (node after move) has already been munched before.
    def isRookie(self,nanoMuncher):
        for k,v in self.nodes.iteritems():
            if(nanoMuncher.x == v.x and nanoMuncher.y == v.y and v.state==NodeState.munched):
                return True
        return False

    # munch the graph and move forward.
    # check if the nanoMuncher has become a blackhole or not.
    def moveNanoMuncher(self,nanoMuncher):
        if(not self.isBlackHole(nanoMuncher)):
            move = self.mutateNanoMuncherProgram(nanoMuncher)
            return True
        return False
      
    # This function checks if the nanoMuncher has become a black hole or not.
    def isBlackHole(self,nanoMuncher):
        initProgram = nanoMuncher.program
        count = 1
        while(count != len(nanoMuncher.program)):
            move = self.mutateNanoMuncherProgram(nanoMuncher)
            if(move != ()):
                self.restoreNanoMuncherProgram(nanoMuncher,initProgram)
                return True
            count += 1
        return False   
    
    # Instead of program counter, we are rotating the program.
    def mutateNanoMuncherProgram(self,nanoMuncher):
        move = self.tryMove(nanoMuncher)
        nanoMuncher.program = nanoMuncher.program[1:] + nanoMuncher.program[0]
        return move
    
    # Restore the program
    def restoreNanoMuncherProgram(self,nanoMuncher, initProgram):
        nanoMuncher.program = initProgram
    
          
    # Try to move by finding a valid node.
    def tryMove(self,nanoMuncher):
        direction = nanoMuncher.program[0]
        x = nanoMuncher.x
        y = nanoMuncher.y
        
        #check direction of movement and adjust coordinates
        if(direction == "L"):
            x = x-1
        elif(direction == "R"):
            x = x+1
        elif(direction == "D"):
            y = y-1
        elif(direction == "U"):
            y = y+1

        for edge in self.edges:
            node1 = self.nodes[edge[0]]
            node2 = self.nodes[edge[1]]
            if(self.isValidMove(x,y,node1)):
                return (edge,node1)
            elif(self.isValidMove(x,y,node2)):
                return (edge, node2)
                
        return ()       
  
            
    # Checks if the intent to move matches with the actual node
    def isValidMove(self,x,y,node):
        return (x == node.x and y == node.y)
    

    # This function resolves conflicts between nanoMunchers which reach the same
    # node while munching
    def conflictSameNode(self,nanoMunchers):
        up = left = down = right = []
        conflictedNanoMunchers=[]
        for i in range(0,len(nanoMunchers)):
            for j in range(i,len(nanoMunchers)):
                if(self.isMunching(nanoMunchers[i],nanoMunchers[j])):
                    conflictedNanoMunchers.append(nanoMunchers[j])
       
        retNanoMuncher = None
        for nanoMuncher in conflictedNanoMunchers:
            lastMove = nanoMuncher.program[-1]
            if(lastMove == "U"):
                up.append(nanoMuncher)
            elif(lastMove == "L"):
                left.append(nanoMuncher)
            elif(lastMove == "D"):
                down.append(nanoMuncher)
            elif(lastMove =="R"):
                right.append(nanoMuncher)
       
        random.shuffle(up)
        random.shuffle(left)
        random.shuffle(down)
        random.shuffle(right)
        if(len(up)!=0):
            retNanoMuncher = up[0]
        elif(len(left) != 0):
            retNanoMuncher = left[0]
        elif(len(down)!=0):
            retNanoMuncher = down[0]
        elif(len(right) !=0 ):
            retNanoMuncher =  right[0]
       
        conflictedNanoMunchers = up + left + down + right
        self.removeAllConflicted(nanoMunchers,conflictedNanoMunchers)
        nanoMunchers.append(retNanoMuncher)

    # Improve efficiency by augmenting the DS.
    # self.time > nm1.dropTime basically means that the nanomuncher has already started munching
    # and is moving around the graph.
    def isMunching(self,nm1,nm2):
        if (self.time > nm1.dropTime
           and nm1.x ==nm2.x and nm1.y == nm2.y):
            return True      
        else:
            return False
    
    # This function resolves the conflicts between the nanomunchers 
    # dropped at the same time
    def conflictDropTime(self,nanoMunchers):
        # container for keeping conflicted nanomunchers
        conflictedNanoMunchers=[]
        #find all conflicted nanomunchers
        for i in range(0,len(nanoMunchers)):
            for j in range(i,len(nanoMunchers)):
                if(self.isSame(nanoMunchers[i],nanoMunchers[j])):
                    conflictedNanoMunchers.append(nanoMunchers[j])
        
        # randomly pick one and declare it as winner.          
        random.shuffle(conflictedNanoMunchers)
        winner = conflictedNanoMunchers[0]
        
        #remove all conflicted.
        self.removeAll(nanoMunchers,conflictedNanoMunchers)
        #append the winner, it got deleted during the call to removeAll.
        nanoMunchers.append(winner)

    # removes all the munchers which are in list 2 from list 1
    def removeAll(self,nanoMunchers,conflictedNanoMunchers):
        for conflictedNm in conflictedNanoMunchers:
            self.findAndRemove(nanoMunchers,conflictedNm)
  
    # find conflictedNm in nanoMunchers list and remove it.
    def findAndRemove(self,nanoMunchers,conflictedNm):
        for i in range(0,len(nanoMunchers)):
            if(nanoMunchers[i].x == conflictedNm.x and 
              nanoMunchers[i].y == conflictedNm.y):
                del nanoMunchers[i]
                break

    # This function checks if nm1 is similar to nm2 and checks if their drop time is equal
    # to current time.
    def isSame(self,nm1,nm2):
        if (nm1.dropTime == nm2.dropTime
            and self.time == nm1.dropTime
            and nm1.x == nm2.x and nm1.y == nm2.y):
                return True      
        else:
            return False

def runValidator(filename,programOutput):
    munchPresenters = FormatValidator().validate(programOutput)
    Simulation(filename).simulate(munchPresenters)
    

def main():
        if(len(sys.argv) == 2):
            filename = sys.argv[1]
            programOutput = sys.stdin.read()
            if('' in programOutput):
                programOutput = programOutput.split('\n')[:-1]
            runValidator(filename,programOutput)
        else:
            print "Usage: python nanomunchers_validator.py <graph-input-file>"

if __name__ == "__main__":
    main();

