# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
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
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # 가능한 행동들(getLegalActions)을 가져옴옴
        # 각 행동을 실행했을 때의 상태를 만듬
        # 그 상태를 evaluationFunction에 넣어 점수를 매김
        # 점수가 가장 높은 행동을 고름

        #가까운 음식이 있을수록 점수 높이기
        total_score = successorGameState.getScore()
        f_position = newFood.asList()

        if f_position:
            min_dis = min(manhattanDistance(newPos,food) for food in f_position)
            total_score += 10 / (min_dis+1)

        #유령이 가까우면 점수 낮추지만 scared상태면 괜찮
        for ghostState, scaredTime in zip(newGhostStates, newScaredTimes):
            ghostPos = ghostState.getPosition()
            dist = manhattanDistance(newPos, ghostPos)

            if scaredTime > 0:
                total_score += 200 / (dist + 1)

            elif dist < 2:
                total_score -= 1000  

        return total_score

        # return successorGameState.getScore()
        

def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
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

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        # pacman이 먼저 움직이고 그 다음에 모든 유령들이 차례대로 움직임
        # pacman의 턴: 가능한 행동 중에서 점수가 가장 높은 행동 선택 max
        # 유령턴에는 가능한 행동 중에서 점수가 가장 낮은 행동 선택 min
        # 모든 턴을 재귀적으로 돌면서 depth가 다 차거나 게임이 끝나면 반환
        def minimax(agentIndex, depth, state):
            # 종료조건
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            # agent, depth 설정 pacman돌아오면 depth 1 추가
            numAgents = state.getNumAgents()
            nextAgent = (agentIndex + 1) % numAgents
            nextDepth = depth + 1 if nextAgent == 0 else depth

            # agent의 행동이 아예 없을 때때
            actions = state.getLegalActions(agentIndex)
            if not actions:
                return self.evaluationFunction(state)

            # pacman 최대값 선택
            if agentIndex == 0:  
                return max(minimax(nextAgent, nextDepth, state.generateSuccessor(agentIndex, action)) for action in actions)

            # 유령이면 최소값
            else:  
                return min(minimax(nextAgent, nextDepth, state.generateSuccessor(agentIndex, action)) for action in actions)

        good_score = float('-inf')
        good_action = None
        for action in gameState.getLegalActions(0):
            score = minimax(1, 0, gameState.generateSuccessor(0, action))
            if score > good_score:
                good_score = score
                good_action = action
        return good_action 
        

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # max는 점수를 최대화 + alpha 갱신 + beta cut-off
        # min은 점수를 최소화 + beta 갱신 + alpha cut-off
        # 각 재귀 호출마다 agent 인덱스와 depth 업데이트
        # cut-off는 alpha/beta 범위를 벗어날 때만
        def abSearch(state, agentIndex, depth, alpha, beta):
            if depth == self.depth or state.isWin() or state.isLose():
                return self.evaluationFunction(state), None
            #  agent와 depth 계산
            num_agent = state.getNumAgents()
            next_agent = (agentIndex + 1) % num_agent
            next_depth = depth + 1 if next_agent == 0 else depth

            # 행동 없으면 현재 점수 반환
            legal_actions = state.getLegalActions(agentIndex)
            if not legal_actions:
                return self.evaluationFunction(state), None

            good_action = None
            # pacman max처리
            if agentIndex == 0:
                value = float('-inf')
                for action in legal_actions:
                    next_state = state.generateSuccessor(agentIndex, action)
                    score, _ = abSearch(next_state, next_agent, next_depth, alpha, beta)

                    # 더 좋은 점수 발견하면 업데이트
                    if score > value:
                        value = score
                        good_action = action

                    # beta보다 커지면 컷컷
                    if value > beta:
                        break
                    alpha = max(alpha, value)
                return value, good_action
            
            # 유령 min처리
            else:
                value = float('inf')
                for action in legal_actions:
                    next_state = state.generateSuccessor(agentIndex, action)
                    score, _ = abSearch(next_state, next_agent, next_depth, alpha, beta)
                    # 더 작은 점수 발견하면 업데이트
                    if score < value:
                        value = score
                        good_action = action
                    # alpha보다 작아지면 컷컷
                    if value < alpha:
                        break
                    beta = min(beta, value)
                return value, good_action

        _, action = abSearch(gameState, 0, 0, float('-inf'), float('inf'))
        return action

        # util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        
        def expectimax(state, agentIndex, depth):
            if state.isWin() or state.isLose() or depth == self.depth:
                return self.evaluationFunction(state)
            # agent와 depth 계산
            num_agents = state.getNumAgents()
            next_agent = (agentIndex + 1) % num_agents
            next_depth = depth + 1 if next_agent == 0 else depth

            # 행동 없으면 현재 점수 반환
            legal_actions = state.getLegalActions(agentIndex)
            if not legal_actions:
                return self.evaluationFunction(state)

            # pacman max 처리
            if agentIndex == 0:  
                value = float('-inf')
                for action in legal_actions:
                    successor = state.generateSuccessor(agentIndex, action)
                    value = max(value, expectimax(successor, next_agent, next_depth))
                return value
            
            # 유령 min 처리
            else:  
                value = 0
                for action in legal_actions:
                    successor = state.generateSuccessor(agentIndex, action)
                    prob = 1.0 / len(legal_actions)
                    value += prob * expectimax(successor, next_agent, next_depth)
                return value


        # 루트 노드에서 가능한 행동들 중 가장 기대값이 높은 행동 선택
        good_score = float('-inf')
        good_action = None
        for action in gameState.getLegalActions(0):
            score = expectimax(gameState.generateSuccessor(0, action), 1, 0)
            if score > good_score:
                good_score = score
                good_action = action
        return good_action

        # util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

# 점수만 보는 것이 아니라:
# 남은 음식 개수
# 캡슐 위치
# 유령과의 거리 (scared/비scared)
# 음식까지의 거리
def betterEvaluationFunction(currentGameState):
    pacman_pos = currentGameState.getPacmanPosition()
    food_list = currentGameState.getFood().asList()
    capsule_list = currentGameState.getCapsules()
    ghost_states = currentGameState.getGhostStates()
    scared_times = [ghost.scaredTimer for ghost in ghost_states]

    score = currentGameState.getScore() 

    # 음식 개수 적을수록 이득득
    food_count = len(food_list)
    if food_count > 0:
        # pacman과 가장 가까운 음식까지의 거리 계산
        closest_food_dist = min(util.manhattanDistance(pacman_pos, food) for food in food_list)
        score += 10.0 / closest_food_dist  # 가까울수록 점수 가산
    score -= 4 * food_count  # 음식이 많을수록 패널티

    # 캡슐 개수 적을수록 이득
    score -= 20 * len(capsule_list)

    # 유령과의의 거리 
    for ghost, scared_time in zip(ghost_states, scared_times):
        ghost_pos = ghost.getPosition()
        dist = util.manhattanDistance(pacman_pos, ghost_pos)

        if scared_time > 0:
            # 유령이 scared 상태면 가까이 갈수록 이득득
            score += 200 / (dist + 1)
        else:
            # 일반 유령이면 가까울수록 위험
            if dist < 2:
                score -= 1000
    return score
    # util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
