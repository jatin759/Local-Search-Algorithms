# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including p_no link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      P_NO reflex agent chooses an action at each choice point by examining
      its alternatives via p_no state evaluation function.

      The code below is provided as p_no guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes p_no GameState and returns
        some Directions.SCARED for some SCARED in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        avial_moves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in avial_moves]
        bestScore = max(scores)
        ind = [index for index in range(len(scores)) if scores[index] == bestScore]
        final_Ind = random.choice(ind) # Pick randomly among the best

        "Add more of your code here if you want to"

        return avial_moves[final_Ind]

    def evaluationFunction(self, currentGameState, action):
        """
        Design p_no better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns p_no number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each n_ghosts will remain
        scared because of Pacman having eaten p_no power pellet.

        Print out these variables to see what you're getting, then combine them
        to create p_no masterful evaluation function.
        """
        # Useful information you can extract from p_no GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [g_staTe.scaredTimer for g_staTe in newGhostStates]

        "*** YOUR CODE HERE ***"
        #list of pos of food particles
        food = newFood.asList()
        #utility value
        total = 0

        #avoid pacman from staying at the same pos
        if manhattanDistance(currentGameState.getPacmanPosition(), newPos) == 0:
        	return -10000000

        #high -ve utility if ghost is near	
        for g_state in newGhostStates:
        	if manhattanDistance(g_state.getPosition(),newPos)<=1:
        		return -10000000

        for j in food:
        	total += manhattanDistance(j,newPos)

        if len(food)!=0:
        	uti =  26020/len(food) + 2501/total
        else:
        	return 10000000 #high utiltiy if food list's length is zero			

        return uti

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search n_agents
      (not reflex n_agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search n_agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns p_no list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of n_agents in the game
        """
        "*** YOUR CODE HERE ***"
        #getting agent info
        n_agents=gameState.getNumAgents()
        n_ghosts=n_agents-1 #no of enemies
        
        act=self.minimax(gameState,self.depth,n_ghosts)
        
        return act
    
    def minimax(self,state,depth,p_no):	
        #legal moves available
        avial_moves=state.getLegalActions(0)
        #get min values from all successor state 
        val_arr=[self.mini(state.generateSuccessor(0, action),depth,p_no,1) for action in avial_moves]
        max_val=max(val_arr)
        # break the tie randomly among the max actions
        ind = [index for index in range(len(val_arr)) if val_arr[index] == max_val]
        final_Ind = random.choice(ind) 
       
        return avial_moves[final_Ind] #final move taken to reahc goal state
    
	#Gives max utility among all successor states
    def maxi(self,state,depth,p_no):

    	#if required depth is reached then return utility value of state
        if(depth==0):  
            return self.evaluationFunction(state)
        avial_moves=state.getLegalActions(0)
        #select max out of min values picked by successors
        val_arr=[self.mini(state.generateSuccessor(0, action),depth,p_no,1) for action in avial_moves]
        if(val_arr==[]):
            return self.evaluationFunction(state)
       
        return max(val_arr)
    	
    #Gives min utility among all successor states
    #used by ghosts to minimize the utitity value of pacman
    def mini(self,state,depth,p_no,tranf):
        #if all enemies have taken their turn then pick max among succ
        if(p_no==1):
            avial_moves=state.getLegalActions(tranf)
            val_arr=[self.maxi(state.generateSuccessor(tranf, action),depth-1,tranf) for action in avial_moves]
        #if no more successors    
            if(val_arr==[]):
                return self.evaluationFunction(state)
            
            return min(val_arr)
        #allow all enemies to take their turn by calling mini recursively
        else:
        
            avial_moves=state.getLegalActions(tranf)
            val_arr=[self.mini(state.generateSuccessor(tranf, action),depth,p_no-1,tranf+1) for action in avial_moves]
        #if no more successors
            if(val_arr==[]):
                return self.evaluationFunction(state)
        
            return min(val_arr)
			




class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        n_agents=gameState.getNumAgents()
        n_ghosts=n_agents-1
        act=self.alphabeta(gameState,self.depth,n_ghosts,-10000000,+99999999)
        return act

    # minimax function that uses aplha beta pruning
    def alphabeta(self,state,depth,p_no,alpha,beta):
        avial_moves=state.getLegalActions(0)
        temp=-9999999999
        for action in avial_moves:
            scared=self.mini(state.generateSuccessor(0, action),depth,p_no,1,alpha,beta)
            
            if scared>=temp:
                temp=scared
                act=action
            if temp<beta:
                alpha=max(alpha,temp)
        return act
    
    def maxi(self,state,depth,p_no,alpha,beta):
        avial_moves=state.getLegalActions(0)
        if(avial_moves==[]):
            return self.evaluationFunction(state)
        if(depth==0):
            return self.evaluationFunction(state)
        temp=-9999999999
        #pruning action. Returns maximum value among succ if it is in range (alpha,beta)
        for action in avial_moves:
            temp=max(temp,self.mini(state.generateSuccessor(0, action),depth,p_no,1,alpha,beta))
            if temp<=beta:
                alpha=max(alpha,temp)
            else: 
            	return temp
      
        return temp

    def mini(self,state,depth,p_no,tranf,alpha,beta):
        #if all enemies have taken their turn then pick max among succ
        if(p_no==1):
            avial_moves=state.getLegalActions(tranf)
            if(avial_moves==[]):
                return self.evaluationFunction(state)
            temp=9999999999
            for action in avial_moves:
                temp=min(temp,self.maxi(state.generateSuccessor(tranf, action),depth-1,tranf,alpha,beta))
                if temp>=alpha:
                    beta=min(beta,temp)
                else: 
                	return temp
            return temp
        #allow all enemies to take their turn by calling mini recursively
        else:
            avial_moves=state.getLegalActions(tranf)
            if(avial_moves==[]):
                return self.evaluationFunction(state)
            temp=9999999999
            #pruning action. Returns min value among succ if it is in range (alpha,beta)
            for action in avial_moves:
                temp=min(temp,self.mini(state.generateSuccessor(tranf, action),depth,p_no-1,tranf+1,alpha,beta))
                if temp>=alpha:
                    beta=min(beta,temp)
                else: 
                	return temp
            return temp

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        n_agents=gameState.getNumAgents()
        n_ghosts=n_agents-1
        act=self.expecti(gameState,self.depth,n_ghosts)
        return act
    
    def expecti(self,state,depth,p_no):
        avial_moves=state.getLegalActions(0)
        arr=[self.mini(state.generateSuccessor(0, action),depth,p_no,1) for action in avial_moves]
        m=max(arr)
        bestIndices = [index for index in range(len(arr)) if arr[index] == m]
        chosenIndex = random.choice(bestIndices) 
        return avial_moves[chosenIndex]
    
    def maxi(self,state,depth,p_no):
        if(depth==0):
            return self.evaluationFunction(state)
        avial_moves=state.getLegalActions(0)
        arr=[self.mini(state.generateSuccessor(0, action),depth,p_no,1) for action in avial_moves]
        if(arr==[]):
            return self.evaluationFunction(state)
        total=0.0
        return max(arr)
    
    def mini(self,state,depth,p_no,tranf):
        if(p_no==1):
            avial_moves=state.getLegalActions(tranf)
            arr=[self.maxi(state.generateSuccessor(tranf, action),depth-1,tranf) for action in avial_moves]
            if(arr==[]):
                return self.evaluationFunction(state)

            total=0.0

            #expected values of all successoors as all moves of enemy are likely..
            for x in arr:
                total+=x
            return float(float(total)/float(len(arr)))

        else:
            avial_moves=state.getLegalActions(tranf)
            arr=[self.mini(state.generateSuccessor(tranf, action),depth,p_no-1,tranf+1) for action in avial_moves]
            if(arr==[]):
                return self.evaluationFunction(state)
            total=0.0
            for x in arr:
                total+=x
            return float(float(total)/float(len(arr)))

def betterEvaluationFunction(currentGameState):
    """
      Your extreme n_ghosts-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    #Get the required detils

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [g_staTe.scaredTimer for g_staTe in newGhostStates]
    capsule_pos = currentGameState.getCapsules()
    
    "*** YOUR CODE HERE ***"
    
    #list of the positions of food particles
    food=newFood.asList()
    total=0
    #flag represents if the ghost is far enough or not
    flag=0
    
    for g_state in newGhostStates:
    	#return very low utility if ghost is very near
        if manhattanDistance(g_state.getPosition(),newPos)<=2:
            return -10000000
        elif manhattanDistance(g_state.getPosition(),newPos)>=4:
            flag=1

    scared=0
    f1 = 0 
    f2 = 0
    #distance of ghost from scared times
    if newScaredTimes>0:
        scared=manhattanDistance(g_state.getPosition(),newPos)

    #total sum of food particles    
    for i in food:
        total+=manhattanDistance(i,newPos)

    if len(food)==0:
        return 100000000

    f1 =3501/scared
    f2 = 26020/len(food)
        
    if flag==1:
        final= f2 + f1
    else:
        final=3500/total + f1 + f2

    return final





# Abbreviation
better = betterEvaluationFunction

