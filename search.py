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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    start = problem.getStartState()
    if problem.isGoalState(start):
    	return []
    visited = set()
    visited.add(start)
    for neighbor in problem.getSuccessors(start):
        path = depthFirstSearch_helper(problem,neighbor,visited,[])
        if path:
            return path
    return []

def depthFirstSearch_helper(problem,start,visited,path):
    visited.add(start[0])
    path.append(start[1])
    if problem.isGoalState(start[0]):
        return path
    for neighbor in problem.getSuccessors(start[0]):
        if neighbor[0] not in visited:
            result = depthFirstSearch_helper(problem,neighbor,visited,path)
            if result:
                return result
            path.pop()
    return []
    
def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    #Need to implement path
    start = problem.getStartState()
    frontier = util.Queue()
    frontier.push((start,[]))
    visited = []
    while not frontier.isEmpty():
    	node,direction = frontier.pop()
    	if problem.isGoalState(node):
    		return direction
    	for successor, action, stepcost in problem.getSuccessors(node):
    		if not successor in visited:
    			frontier.push((successor, direction + [action]))
    			visited.append(successor)
    	visited.append(node)
    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    start = problem.getStartState()
    if problem.isGoalState(start):
    	return []
    cost = {start:0}
    frontier = util.PriorityQueue()
    frontier.update(start,cost[start])
    path = dict()
    path[start] = []
    visited = set()
    visited.add(start)
    while not frontier.isEmpty():
    	current = frontier.pop()
    	if problem.isGoalState(current):
    		return path[current]
    	for child in problem.getSuccessors(current):
    		if child[0] not in visited:
    			cost[child[0]] = cost[current] + child[2]
    			frontier.update(child[0],cost[child[0]])
    			visited.add(child[0])
    			path[child[0]] = path[current] + [child[1]]
    		elif cost[current] + child[2] < cost[child[0]]:
    			cost[child[0]] = cost[current] + child[2]
    			frontier.update(child[0],cost[child[0]])
    			path[child[0]] = path[current] + [child[1]]
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    start = problem.getStartState()
    frontier = util.PriorityQueue()
    frontier.push((start, [], 0), (heuristic(start, problem)))
    visited = dict()
    while not frontier.isEmpty():
    	current = frontier.pop()
    	node, direction, cost = current
    	visited[node] = cost
    	if problem.isGoalState(node):
    		return direction
    	for successor, action, stepcost in problem.getSuccessors(node):
    		if (successor not in visited) or (successor in visited and visited[successor] > cost + stepcost):
    			visited[successor] = cost + stepcost
    			frontier.push((successor, direction + [action], cost + stepcost), cost + stepcost + (heuristic(successor, problem)))
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
