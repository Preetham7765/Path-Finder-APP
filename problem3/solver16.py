#State Space: The state space for the 15 puzzle is 16!.
#Successor function: The successor function will create states that have not been added to the heap(successor list) or in the closed list(already visited) and duplicate states.
    #The successor function will create 6 successor states(if none of the states are in the heap) by moving tile horizontally and vertically.
#Edge Weights: The cost for moving one, two or three tiles is considered 1.
#Goal State: Goal state is the following state:[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]
#Heuristic Function: The heuristic funcion used is Manhattan Distance divided by 3. I formulated this heuristic as in this variant of 15 puzzle we are allowed to move 1,2 or 3 tiles in move.
    #Thus, if the original version of 15 puzzle problem accounts moving 1 tile as a move thus in this moving 3 tiles or 2 tiles is considered 1 move.Thus divided by 3.
#Admissibility: The admissibility can be explained as for the original version of 15 puzzle manhattan distance was considered to be admissible as it would never overestimate the number of moves to reach the goal.
    #Thus, here as we consider moving 2 or 3 tiles as 1 move we are dividing the heuristic by 3. SO here we are considering movinf 3 tiles as 1 move.
#Working of the search algorithm:
   # 1. The input to the code is the intiail unsolved puzzle.
   # 2. After reading the input the code starts from the initial board and creates its successors.
   # 3. The successors are created in two steps: First all the successors with horizontal moves are created and then all the successors with vertical moves are created.
   # 4. As the successors are being created their moves are also calculated and appended with them for calculating their paths.
   # 5. After successors are created each successor is checked for duplication and visited states.
    #   If the sucessor has already been visited or already been created then it will not be added to the successor list.
   # 6. Each successor is then checked if it is a goal state or not.
    #    If it is a goal state then we return the path to the goal state
    #    If it is not a goal state then the manhattan distance of the successor plus the cost to reach it is calculated and added to the heap of successors.
    #   Then successor with minimum cost or heuristic value is popped out and its successors are created and same process continues.

#Problems/Assumptions/Decisions/Simplifications:
    #One of the problems I faced during the assignment was th use of list comprehension. I found difficulty in understanding how to use list comprehensions in many cases like assigning variables while traversing nested loops.
    #One simplification I did was the use of dictionary to search for a particular state instead of looping over again and again on a heap.
    #One of the other difficulties I faced was to update an entry in a heap which was then implemented using a dictionary.





# put your 15 puzzle solver here!
#!/usr/bin/env python

import sys
import heapq
import math

def goal_state_index(element):
    for i in range(4):
        if element in goal_state[i]:
            g_col = goal_state[i].index(element)
            g_row = i
    return g_row,g_col


def in_visited_list(board):
    str1 = ''.join(str(e) for e in board)
    if visited_dict.has_key(str1):
            return True
    else:
            return False



def manhattan_dist(board):
    increment = 1
    manhattan_distance = 0
    misplaced = 0
    for i in range(0,4):
        for j in range(0,4):
            if board[i][j] == 0:
                continue
            if board[i][j] != goal_state[i][j]:
                g_row,g_col = goal_state_index(board[i][j])
                manhattan_distance += abs(i - g_row) + abs(j - g_col)

            else:
                continue
    manhattan_distance = int(math.floor(manhattan_distance / 3))
    return manhattan_distance


def row_swap(board,blank_row,blank_col,cost):
    swap_board = []
    path = ''
    temporary_board =[x[:] for x in board]
    swap_position = blank_col - 3
    for i in range(0,4):
        if swap_position == 0:
            swap_position += 1
            continue
        else:
            board = [x[:] for x in temporary_board]
            blank = board[blank_row].pop(blank_col)
            board[blank_row].insert((blank_col-swap_position),blank)
            if in_visited_list(board):
                swap_position += 1
                continue
            else:
                if swap_position < 0:
                    path = 'L' + str(abs(swap_position)) + str(blank_col+1)
                else:
                    path = 'R' + str(abs(swap_position)) + str(blank_col+1)
                board.append(path)
                swap_position += 1
                swap_board.append(board)
    return [col_swap(swap_board,temporary_board,blank_row,blank_col)]



def multi_swap_oncol(board,swap_pos,blank_row,blank_col):
    count = abs(swap_pos)
    swap_loc = swap_pos
    br = blank_row
    if swap_pos > 0:
        while count > 0:
            board[br][blank_col] = board[blank_row - swap_loc + (swap_pos -1)][blank_col]
            br = (blank_row - swap_loc + (swap_pos - 1))
            swap_loc += 1
            count -= 1
        path = 'D' + str(abs(swap_pos)) + str(blank_row+1)

    else:
        while count > 0:
            board[br][blank_col] = board[blank_row - swap_loc - (abs(swap_pos) - 1)][blank_col]
            br = (blank_row - swap_loc - (abs(swap_pos) - 1))
            swap_loc -= 1
            count -= 1
        path = 'U' + str(abs(swap_pos)) + str(blank_row+1)
    board[blank_row - swap_pos][blank_col] = 0
    board.append(path)
    return (board)


def col_swap(swap_board,board,blank_row,blank_col):
    multi_board = []
    temporary_board =[x[:] for x in board]
    swap_position = blank_row - 3
    for i in range(0,4):
        if swap_position == 0:
            swap_position += 1
            continue
        else:
            board = [x[:] for x in temporary_board]
            if abs(swap_position) > 1:
                multi_board = multi_swap_oncol(board,swap_position,blank_row,blank_col)
                swap_position +=1
                if in_visited_list(multi_board):
                    continue
                else:
                    swap_board.append(multi_board)
            else:
                board[blank_row][blank_col]=board[blank_row-swap_position][blank_col]
                board[blank_row-swap_position][blank_col] = 0
                if swap_position < 0:
                    path = 'U' + str(abs(swap_position)) + str(blank_row+1)
                else:
                    path = 'D' + str(abs(swap_position)) + str(blank_row+1)
                swap_position += 1
                if in_visited_list(board):
                    continue
                else:
                    board.append(path)
                    swap_board.append(board)
    return (swap_board)


def succ_list(board,cost):
    for i in range(0,4):
        for j in range(0,4):
            if board[i][j] == 0:
                blank_row = i
                blank_col = j
                break
    return [row_swap(board,blank_row,blank_col,cost)]




def solve(initial_board):
    path = ['S']
    initial_path = ['S']
    if initial_board == goal_state:
        return True
    top = heapq.heappop(h)
    str1 = ''.join(str(e) for e in top[3])
    visited_dict[str1] = 1
    successor_dict[str1] = 1
    cost = top[1]+1
    while len(h) > -1 :
            for s in succ_list(top[3],cost)[0][0]:
                s1 = s[0:4]
                state_path = s[4:]
                if s1 == goal_state:
                    path.append(state_path)
                    s1.append(path)
                    return s1
                else:
                    str1 = ''.join(str(e) for e in s1)
                    if successor_dict.has_key(str1):
                        continue
                    else:
                        path.append(state_path)
                        fn = manhattan_dist(s1) + cost
                        heapq.heappush(h, (fn,cost,path,s1))
                        successor_dict[str1] = 1
                        path = [x[:] for x in initial_path]
            top = heapq.heappop(h)
            initial_path = top[2]
            path = [x[:] for x in initial_path]
            str1 = ''.join(str(e) for e in top[3])
            visited_dict[str1] = 1
            cost = top[1]+1
    return False



cost = 0
visited_dict = {}
successor_dict = {}
h=[]
results = []
#path = []
goal_state = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
filename = sys.argv[1]
with open(filename) as inputfile:
    for line in inputfile:
        results.append(line.strip().split(' '))
results = [[int(col) for col in row] for row in results]
priority = manhattan_dist(results) + cost
heapq.heappush(h, (priority,cost,'S',results))
solution = solve(results)
answer = ' '.join(str(e) for e in solution[4] )
print(answer)
#print answer.translate(None, "S'[]")
