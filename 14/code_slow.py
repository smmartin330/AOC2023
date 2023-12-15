from aoc import *
from puzzle_data import *

from time import time

DAY = 14

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

def move_rocks(grid):
    for y in range(1,grid.height): # Y
        for x in range(0,grid.width):
            if grid.gridmap[y][x] == 'O':
                for y_mover in range(y-1,-1,-1):
                    if y_mover == 0 and grid.gridmap[y_mover][x] == '.':
                        grid.gridmap[y_mover][x] = 'O'
                        grid.gridmap[y_mover+1][x] = '.'
                        break
                    elif grid.gridmap[y_mover][x] == '.':
                        grid.gridmap[y_mover][x] = 'O'
                        grid.gridmap[y_mover+1][x] = '.'
                        continue
                    else:
                        break
    return True    
                    
class Puzzle():
    def __init__(self,input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split('\n')
        
        self.dishes = Grid(self.input_list)


    def p1(self):
        self.p1_solution = 0

        move_rocks(grid=self.dishes)
        for y in range(0,self.dishes.height):
            rocks = self.dishes.gridmap[y].count('O')
            row_value = self.dishes.height - y
            row_score = rocks * row_value
            self.p1_solution += row_score
          
        return True

    def p2(self):
        self.p2_solution = 0
        
        check_score = 0
        for spins in range (0,1000000000):
            self.dishes.g_rot90(-1)
            move_rocks(grid=self.dishes)
            
            if spins % 100000 == 0:
                print(f'Spins: {spins}')
                # current_score = 0
                # for y in range(0,self.dishes.height):
                #     rocks = self.dishes.gridmap[y].count('O')
                #     row_value = self.dishes.height - y
                #     current_score += rocks * row_value
                    
                # if current_score == check_score:
                #     self.p2_solution = row_score
                #     return True
                # else: check_score =  current_score
        
        for y in range(0,self.dishes.height):
            rocks = self.dishes.gridmap[y].count('O')
            row_value = self.dishes.height - y
            row_score = rocks * row_value
            self.p1_solution += row_score
        
        return True

def main():

    if P1_SAMPLE_SOLUTION:
        print("PART 1\nTesting Sample...\n")
        start_time = time()
        sample = Puzzle(input_text=P1_SAMPLE)
        sample.p1()
        if P1_SAMPLE_SOLUTION == sample.p1_solution:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P1_SAMPLE_SOLUTION}, got {sample.p1_solution}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            puzzle = Puzzle(input_text=PUZZLE_INPUT)
            puzzle.p1()
            print("Processing Input...\n")
            start_time = time()
            print(f'SOLUTION: {puzzle.p1_solution}')
            print(f"Elapsed time {elapsed_time(start_time)}")

    if P2_SAMPLE_SOLUTION:
        print("PART 2\nTesting Sample...\n")
        start_time = time()
        sample.p2()
        if P2_SAMPLE_SOLUTION == sample.p2_solution:
            print("Sample correct.")
        else:
            print(f"Sample failed; Expected {P2_SAMPLE_SOLUTION}, got {sample.p2_solution}")
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            print("Processing Input...\n")
            start_time = time()
            puzzle.p2()
            print(f'SOLUTION: {puzzle.p2_solution}')
            print(f"Elapsed time {elapsed_time(start_time)}")

if __name__ == "__main__":
    main()