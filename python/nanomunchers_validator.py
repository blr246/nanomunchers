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
        ##print programOutput
        nanomunchers = int(programOutput[0])
        ##print "number of nanomunchers dropped: %d" % nanomunchers
        ##print "number suggested by program output %d " % len(programOutput[1:])
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
        self.x = xloc
        self.y = yloc
        self.state = state

class States:
    init=0
    drop=1
    munch=2
    blackhole=3
    killed=4

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
        self.edges = [[int(idx) for idx in lis] for lis in refinedF if len(lis) ==2]
        self.time =0
        self.nodes = self.createNodes();
        self.munched = 0
        self.totalNodes = len(self.vertices)
        self.nanoMunchers = []
    
    def createNodes(self):
        nodes = {}
        for vertex in self.vertices:
            nodes[int(vertex[0])] = Node(int(vertex[0]),int(vertex[1]),
                                    int(vertex[2]),NodeState.notMunched)
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
            killed = []
            #print "Time Step: %d" % self.time
            for nanoMuncher in nanoMunchers:
                if(self.time == nanoMuncher.dropTime):
                    #print "dropped nanoMuncher: (%d,%d) at time %d" % (nanoMuncher.x,nanoMuncher.y,self.time)
                    if(self.isValidLocation(nanoMuncher)):
                        nanoMuncher.state = States.drop
                    else:
                        ##print "killed...dropped at (%d,%d)" %(nanoMuncher.x,nanoMuncher.y)
                        killed.append(nanoMuncher)
                        nanoMuncher.state = States.killed
            # remove all that were dropped on an already munched node or the one that didn't exist.
            self.removeAll(nanoMunchers, killed)
            #resolve conflicts, some nanomunchers will be killed.
            self.conflictDropTime(nanoMunchers) # Nanomunchers dropped at the same node.
            
            blackholes = []
            for nanoMuncher in nanoMunchers:
                if(self.time >= nanoMuncher.dropTime):
                    print "nanoMuncher at (%d,%d) is munching." %(nanoMuncher.x,nanoMuncher.y)
                    #munch
                    #print "program before moving: %s" % nanoMuncher.program
                    self.markNodeMunched(nanoMuncher)
                    self.munched +=1
                    
            
            for nanoMuncher in nanoMunchers:
                didMove = self.moveNanoMuncher(nanoMuncher)
                ##print "didMove: " + str(didMove)
                # if canot move, then make it a blackhole.
                if(didMove == False and nanoMuncher.dropTime < self.time):
                    blackholes.append(nanoMuncher)
                ##print "program: %s" % nanoMuncher.program
                   
            #print "blackholes: " + str(blackholes)
            self.time += 1
            
            #post processing:
            #resolve conflicts, some nanomunchers will be killed.
            self.conflictSameNode(nanoMunchers) # NanoMunchers moved to the same node.
            #remove rookies, rookies will be killed and removed.
            self.removeRookies(nanoMunchers) # NanoMunchers moved to the node that was already munched.
            #remove blackholes
            self.removeAll(nanoMunchers,blackholes) # remove all blackholes.
            
        print "Total nodes munched: %d out of: %d in time: %d" % (self.munched,self.totalNodes,self.time)
    
    
    def isValidLocation(self,nanoMuncher):
        for k,v in self.nodes.iteritems():
            if(v.x == nanoMuncher.x and 
                v.y == nanoMuncher.y and
                v.state != NodeState.munched):
                ##print "Valid location (%d,%d)" %(v.x,v.y)
                return True
        return False
                
    
    # This helps in identifying rookies, if the nanomuncher tries to munch an already
    # node then it is declared as rookie and is killed.
    def markNodeMunched(self,nanoMuncher):
        print "marking nodes as munched for nanoMuncher at (%d,%d)" % (nanoMuncher.x,nanoMuncher.y)
        for k,v in self.nodes.iteritems():
            if(v.x == nanoMuncher.x and 
                v.y == nanoMuncher.y):
                self.nodes[k].state = NodeState.munched
                print "...node at (%d,%d), marked as munched" % (v.x,v.y)

    #This function checks for rookies.
    def removeRookies(self,nanoMunchers):
        #print "removing rookies..."
        rookies=[]
        #print "nanoMunchers: "+str(nanoMunchers)
        for nanoMuncher in nanoMunchers:
            if(nanoMuncher.dropTime < self.time 
               and self.isRookie(nanoMuncher)):
                rookies.append(nanoMuncher)
        #print "number of rookies: %d" % len(rookies)
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
        if(self.time >= nanoMuncher.dropTime):
            #print "moving nanoMuncher..."
            if(self.isBlackHole(nanoMuncher) == False):
                #print "is not a blackhole..."
                move = self.mutateNanoMuncherProgram(nanoMuncher)
                print "nanomuncher at (%d,%d), actually moved in %s direction" % (nanoMuncher.x,
                                                                                  nanoMuncher.y,
                                                                                  nanoMuncher.program[-1])
                #print "move: " + str(move)
                nanoMuncher.x = move[1].x
                nanoMuncher.y = move[1].y
                return True
        return False
      
    # This function checks if the nanoMuncher has become a black hole or not.
    def isBlackHole(self,nanoMuncher):
        #print "checking if nanoMuncher at (%d,%d) is a blackhole." % (nanoMuncher.x,nanoMuncher.y)
        count = 1
        #print "len(nanoMuncher.program) %d" % len(nanoMuncher.program)
        while(count != len(nanoMuncher.program)):
            initProgram = nanoMuncher.program
            move = self.mutateNanoMuncherProgram(nanoMuncher)
            if(move != ()):
                self.restoreNanoMuncherProgram(nanoMuncher,initProgram)
                #print "Not a blackhole..."
                return False
            count += 1
            #print "count: %d" % count
        #print "a blackhole..."
        return True   
    
    # Instead of program counter, we are rotating the program.
    def mutateNanoMuncherProgram(self,nanoMuncher):
        ##print "mutating nanoMuncher at (%d,%d)" % (nanoMuncher.x,nanoMuncher.y)
        move = self.tryMove(nanoMuncher)
        nanoMuncher.program = nanoMuncher.program[1:] + nanoMuncher.program[0]
        #print "move after mutation: " + str(move)
        return move
    
    # Restore the program
    def restoreNanoMuncherProgram(self,nanoMuncher, initProgram):
        #print "restoring nanomuncher's move..."
        #print "nanomuncher at (%d,%d)" %(nanoMuncher.x,nanoMuncher.y)
        print "Undoing move in %s direction, so that nanoMuncher can actually move" % nanoMuncher.program[-1]
        nanoMuncher.program = initProgram
        #print "Restoring done..."
    
          
    # Try to move by finding a valid node.
    def tryMove(self,nanoMuncher):
        #print "Trying to move from (%d,%d)" % (nanoMuncher.x,nanoMuncher.y)
        direction = nanoMuncher.program[0]
        x = nanoMuncher.x
        y = nanoMuncher.y
        #print "direction: %s" % direction
        #check direction of movement and adjust coordinates
        if(direction == "L"):
            x = x-1
        elif(direction == "R"):
            x = x+1
        elif(direction == "D"):
            y = y-1
        elif(direction == "U"):
            y = y+1
        print "Trying to move towards: (%d,%d) in direction %s" % (x,y,direction)
        for edge in self.edges:
            node1 = self.nodes[edge[0]]
            node2 = self.nodes[edge[1]]
            if(self.isValidMove(x,y,node1)):
                #print "moved"
                return (edge,node1)
            elif(self.isValidMove(x,y,node2)):
                #print "moved"
                return (edge, node2)
        print "cannot move in %s direction" % direction       
        return ()       
  
            
    # Checks if the intent to move matches with the actual node
    def isValidMove(self,x,y,node):
        ##print "checking if node is valid..."
        if (x == node.x and y == node.y):
            ##print "Valid move"
            return True
        else:
            ##print "Invalid move"
            return False
    

    # This function resolves conflicts between nanoMunchers which reach the same
    # node while munching
    def conflictSameNode(self,nanoMunchers):
        #print "conflict Same Node..."
        up = left = down = right = []
        conflictedNanoMunchers=[]
        for i in range(0,len(nanoMunchers)):
            conflictArose = False
            for j in range(i+1,len(nanoMunchers)):
                if(self.isMunching(nanoMunchers[i],nanoMunchers[j])):
                    conflictedNanoMunchers.append(nanoMunchers[j])
                    conflictArose = True
            if(conflictArose == True):
                conflictedNanoMunchers.append(nanoMunchers[i])
       
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
        if(len(conflictedNanoMunchers) !=0):
            #print "conflicts same node arose"
            self.removeAll(nanoMunchers,conflictedNanoMunchers)
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
            conflictArose = False
            for j in range(i+1,len(nanoMunchers)):
                if(self.isSame(nanoMunchers[i],nanoMunchers[j])):
                    conflictedNanoMunchers.append(nanoMunchers[j])
                    conflictArose = True
            if(conflictArose):
                conflictedNanoMunchers.append(nanoMunchers[i])
       
        # randomly pick one and declare it as winner.          
        random.shuffle(conflictedNanoMunchers)
        
        if(len(conflictedNanoMunchers) != 0):
            ##print "conflict arose while dropping..."
            ##print "conflicted nanoMunchers: " + str(conflictedNanoMunchers)
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

