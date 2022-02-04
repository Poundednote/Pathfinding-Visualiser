from math import sqrt
import heapq
import pygame
from collections import defaultdict
import sys


# creates 9x9 grid 2d array with each item in the list being a tuple of (x,y) coordinate
class aStar:
    '''
    An A* Pathing algorithm written in python where each node is a coordinate on the grid
    each node is connected to each 4 adjacent squares. the wight of the edges is just 1 and the
    heuristic function to estimate distance from node to goal is the magnitude of the distance between cooridinates
    '''
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal

        # set of newly discovered nodes 
        self.open_set = {start}
        
        # set of visited nodes 
        self.closed_set = set()

        self.current = start
        
        # created path after algorithm is completed
        self.path = None

        # list of previous nodes on the path where camefrom[n] is the node behind it
        self.came_from = {}

        # gscore[n] the cost of the cheapest path form start to n currently known 
        self.gscore = defaultdict(lambda: float('inf'))
        self.gscore[self.start] = 0

        # dictionary with defualt value starting at infity
        self.fscore = defaultdict(lambda: float('inf'))
        self.fscore[self.start] = self.heuristic(self.start)


    def heuristic(self, node):
        # the a star heuristic function used to estimate the cost to reach goal from node n
        # computes the distance from node to end sqrt(x**2 + y**2)
        return sqrt((self.goal[0] - node[0])**2 + (self.goal[1] - node[1])**2)

    def connected_nodes(self): 
        nodes = []
        if self.current[0] > 0:
           nodes.append(grid[self.current[1]][self.current[0]-1])  # 2D array indexed y, x instead of x, y 
        if self.current[1] > 0:
            nodes.append(grid[self.current[1]-1][self.current[0]])
        if self.current[0] < len(grid[0]) - 1 :
            nodes.append(grid[self.current[1]][self.current[0]+1])
        if self.current[1] < len(grid) - 1:
            nodes.append(grid[self.current[1]+1][self.current[0]])

        return nodes

    def reconstruct_path(self):
        # creates a list of nodes traversed in the best path possible 
        total_path = []
        total_path.append(self.current)
        while self.current in self.came_from.keys():
            self.current = self.came_from[self.current]
            total_path.insert(0, self.current)
        return total_path

    def algorithm(self):

        # loops through open set finds the smallest value and changes current node
        prev_fscore = float('inf')
        for node in self.open_set:
            if self.fscore[node] < prev_fscore:
                prev_fscore = self.fscore[node]
                self.current = node

        if self.current == self.goal:
            self.path = self.reconstruct_path()
            return True

        if self.open_set:
            self.open_set.remove(self.current) 
            self.closed_set.add(self.current)

            for neighbor in self.connected_nodes():
                # tentative score is the distance from start to the neighbor through current
                # gscore + wieght of edge
                # all edges in grid are weighted one as all equidistant
                tentative_gscore = self.gscore[self.current] + 1
                if tentative_gscore < self.gscore[neighbor] and neighbor is not None:
                    self.came_from[neighbor] = self.current
                    self.gscore[neighbor] = tentative_gscore
                    self.fscore[neighbor] = self.gscore[neighbor] + self.heuristic(neighbor)

                    if neighbor not in self.open_set:
                        self.open_set.add(neighbor)
            return None
            

        else:
            return False



def main():
    pygame.init()

    global SCREEN, CLOCK
    SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    CLOCK = pygame.time.Clock()
    pathing = None

    start = ()  # has to be empty tuple not None as None value is for walls
    goal = ()
    path = []

    while True:
        
        if pathing is not None:
            step = pathing.algorithm()
            print(step)
            if step is False:
                print('Path not found')
            if step is True:
                path = pathing.path
            
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.MOUSEBUTTONDOWN and pathing is not True:
                pos = pygame.mouse.get_pos()
                row = pos[1] // (HEIGHT + MARGIN)
                column = pos[0] // (WIDTH + MARGIN)

                if event.button == 3 and grid[row][column] is not None:
                    start = grid[row][column]
                
                if event.button == 2 and grid[row][column] is not None:
                    goal = grid[row][column]

            if pygame.mouse.get_pressed()[0]:
                try:
                    pos = event.pos
                except AttributeError:
                    pass

                row = pos[1] // (HEIGHT + MARGIN)
                column = pos[0] // (WIDTH + MARGIN)
                grid[row][column] = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and pathing is None:
                    pathing = aStar(start, goal)
                    print('PATH STARTED') 
                elif event.key == pygame.K_SPACE and pathing is not None:
                    # once pathing is complete pressing space will reset the screen
                    pathing = None
                    path = [] 

        for row in range(len(grid)):
            for column in range(len(grid[0])):
                colour = WHITE

                if pathing is not None:

                    if grid[row][column] in pathing.open_set:
                       colour = RED 

                    if grid[row][column] in pathing.closed_set:
                       colour = GREEN 

                    if grid[row][column] in path:
                        colour = YELLOW

                if grid[row][column] is None:
                    # sets grid obstacles to black
                    colour = BLACK

                if grid[row][column] == start:
                    colour = BLUE

                if grid[row][column] == goal:
                    colour = PINK

                pygame.draw.rect(SCREEN, colour, [(MARGIN + WIDTH) * column + MARGIN,
                                                    (MARGIN + HEIGHT) * row + MARGIN,
                                                    WIDTH,
                                                    HEIGHT])

        CLOCK.tick(60)
        pygame.display.flip()
                                

grid = ([[(x, y) for x in range(60)] for y in range(30)])

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 200)
PINK = (255, 20, 147)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)


WIDTH, HEIGHT = 20, 20
MARGIN = 2
WIN_WIDTH = len(grid[0]) * (WIDTH + MARGIN) + MARGIN
WIN_HEIGHT = len(grid) * (HEIGHT + MARGIN) + MARGIN  
main()
