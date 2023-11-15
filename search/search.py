# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class Node:
    def __init__(self, state, prev = None, action = None, score = None, sum_cost = 0):
        self.state = state
        self.prev = prev
        self.action = action
        self.score = score
        self.sum_cost = sum_cost

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    visited = set() 
    my_stack = util.Stack()
    my_path = util.Stack()

    my_stack.push(problem.getStartState())
    my_path.push([])

    while not my_stack.isEmpty():
        state = my_stack.pop()
        path = my_path.pop()
        visited.add(state)

        if problem.isGoalState(state):
            return path

        for (succ, action, cost) in problem.getSuccessors(state):
            if succ not in visited:
                path_up = path + [action]
                my_stack.push(succ)
                my_path.push(path_up)
    
    return None


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "* YOUR CODE HERE *"

    visited = set()
    queue = util.Queue()
    queue.push(Node(problem.getStartState()))

    while not queue.isEmpty():
        u = queue.pop()

        if problem.isGoalState(u.state):
            actions = []
            while u.action != None:
                actions.append(u.action)
                u = u.prev
            actions.reverse()
            return actions

        if u.state not in visited:
            visited.add(u.state)
            for v in problem.getSuccessors(u.state):
                queue.push(Node(v[0], u, v[1]))

    return []

def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    visited = []
    pq = util.PriorityQueue()
    pq_path = util.PriorityQueue()

    pq.push((problem.getStartState(), 0), 0)
    pq_path.push([], 0)

    while not pq.isEmpty():
        state, total_cost = pq.pop()
        path = pq_path.pop()
        if state not in visited:
            visited.append(state)
            if problem.isGoalState(state):
                return path
        
            for (succ, action, cost) in problem.getSuccessors(state):
            
                new_cost = cost + total_cost
                path_up = path + [action]
                pq.push((succ, new_cost), new_cost)
                pq_path.push(path_up, new_cost)
    
    return None

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

    
"""*** q4 ***"""
def getScore(node: Node):
    return node.score

"""*** q4 ***"""
def getActionSequence(node: Node):
    actions = []
    while node.prev is not None:
        actions.append(node.action)
        node = node.prev
    actions.reverse()
    return actions

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** q4 ***"
    pq = util.PriorityQueueWithFunction(getScore)
    visited = set()
    start = problem.getStartState()
    start_cost = heuristic(start, problem)
    pq.push(Node(start, prev=None, action=None, score=start_cost, sum_cost=0))
    while not pq.isEmpty():
        node = pq.pop()
        if problem.isGoalState(node.state):
            return getActionSequence(node)
        if node.state not in visited:
            visited.add(node.state)
            for successor, action, cost in problem.getSuccessors(node.state):
                cost = node.sum_cost + cost
                score = cost + heuristic(successor, problem)
                pq.push(Node(successor, prev=node, action=action, score=score, sum_cost=cost))
    return []


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch