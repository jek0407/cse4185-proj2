from util import manhattanDistance
from game import Directions
import random, util
from game import Agent

MIN_ = float("-inf")
MAX_ = float("inf")

## Example Agent
class ReflexAgent(Agent):

  def Action(self, gameState):

    move_candidate = gameState.getLegalActions()

    scores = [self.reflex_agent_evaluationFunc(gameState, action) for action in move_candidate]
    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]
    get_index = random.choice(Index)

    return move_candidate[get_index]

  def reflex_agent_evaluationFunc(self, currentGameState, action):

    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()

def scoreEvalFunc(currentGameState):
  return currentGameState.getScore()

class AdversialSearchAgent(Agent):

  def __init__(self, getFunc ='scoreEvalFunc', depth ='2'):
    self.index = 0
    self.evaluationFunction = util.lookup(getFunc, globals())

    self.depth = int(depth)

######################################################################################

class MinimaxAgent(AdversialSearchAgent):
  """
    [문제 01] MiniMax의 Action을 구현하시오. (20점)
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):
    ####################### Write Your Code Here ################################
  
    move_candidate = gameState.getLegalActions()
    
    list_nextstates = [gameState.generateSuccessor(0,action) for action in move_candidate]
    n_agents = gameState.getNumAgents()
    scores = [self.MinimaxValue(n_agents,1,nextstate,(n_agents * self.depth)-1) for nextstate in list_nextstates]  

    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]

    get_index = random.choice(Index) 
    
    return move_candidate[get_index]

  def MinimaxValue(self, n_agents, i_agent, gameState, depth):
    
    if (depth == 0 or gameState.isLose() or gameState.isWin()): # terminal tet
      return self.evaluationFunction(gameState)
      
    depth -= 1
    move_candidate = gameState.getLegalActions(i_agent)
    list_nextstates = [gameState.generateSuccessor(i_agent,action) for action in move_candidate]

    if (i_agent != 0): # Ghost
      val = min([self.MinimaxValue(n_agents, (i_agent+1)%n_agents, nextstate, depth) for nextstate in list_nextstates])
      
    else: # Pacman
      val = max([self.MinimaxValue(n_agents, 1%n_agents, nextstate, depth) for nextstate in list_nextstates])
    
    return val
    ############################################################################

class AlphaBetaAgent(AdversialSearchAgent):
  """
    [문제 02] AlphaBeta의 Action을 구현하시오. (25점)
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):
    ####################### Write Your Code Here ################################

    move_candidate = gameState.getLegalActions()
    
    list_nextstates = [gameState.generateSuccessor(0,action) for action in move_candidate]     
    n_agents = gameState.getNumAgents()
    scores = [self.AlphaBetaValue(n_agents,1,nextstate, (n_agents * self.depth)-1, MIN_, MAX_) for nextstate in list_nextstates]
      
    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore] 
    
    get_index = random.choice(Index)

    return move_candidate[get_index]

  def AlphaBetaValue(self, n_agents, i_agent, gameState, depth, alpha, beta):

    if (depth==0 or gameState.isLose() or gameState.isWin()):  # terminal tet
      return self.evaluationFunction(gameState)

    depth -= 1
    move_candidate=gameState.getLegalActions(i_agent)
    list_nextstates=[gameState.generateSuccessor(i_agent,action) for action in move_candidate]
    if (i_agent != 0): # Ghost
      val = MAX_
      for nextstate in list_nextstates:
        val = min(self.AlphaBetaValue(n_agents, (i_agent+1)%n_agents, nextstate, depth, alpha, beta), val)
        if (val < alpha):
          return val
        beta = min(beta, val)
      
    else: # Pacman
      val = MIN_
      for nextstate in list_nextstates:
        val = max(self.AlphaBetaValue(n_agents, 1%n_agents, nextstate, depth, alpha, beta), val)
        if (val > beta):
          return val
        alpha = max(alpha, val)
    
    return val
    ############################################################################

class ExpectimaxAgent(AdversialSearchAgent):
  """
    [문제 03] Expectimax의 Action을 구현하시오. (25점)
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  def Action(self, gameState):
    ####################### Write Your Code Here ################################
    
    move_candidate = gameState.getLegalActions()
    
    list_nextstates = [gameState.generateSuccessor(0,action) for action in move_candidate]
    n_agents = gameState.getNumAgents()
    scores = [self.ExpectimaxValue(n_agents,1,nextstate,(n_agents * self.depth)-1) for nextstate in list_nextstates]  

    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]

    get_index = random.choice(Index) 
    
    return move_candidate[get_index]

  def ExpectimaxValue(self, n_agents, i_agent, gameState, depth):
    if (depth==0 or gameState.isLose() or gameState.isWin()):  # terminal tet
      return self.evaluationFunction(gameState)

    depth -= 1
    move_candidate=gameState.getLegalActions(i_agent)
    list_nextstates=[gameState.generateSuccessor(i_agent,action) for action in move_candidate]
    if (i_agent != 0): # Ghost
      val = sum([self.ExpectimaxValue(n_agents, (i_agent+1)%n_agents, nextstate, depth) for nextstate in list_nextstates])  / len(list_nextstates)
      
    else: #pacman
      val =  max([self.ExpectimaxValue(n_agents, 1%n_agents, nextstate, depth) for nextstate in list_nextstates])
    
    return val
    ############################################################################
