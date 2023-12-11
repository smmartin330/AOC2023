from aoc import *
from puzzle_data import *

from time import time
from itertools import combinations

DAY = 11

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

class Puzzle():
    def __init__(self,input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split('\n')

        self.universe = []
        self.universe_width = len(self.input_list[0])
        self.column_checker = [*range(0,self.universe_width)]
        for row in self.input_list:
            self.universe.append(row)
            if '#' in row:
                for x in range(0,self.universe_width):
                    if row[x] == '#':
                        if x in self.column_checker:
                            self.column_checker.remove(x)
            else:
                self.universe.append(row.replace('.','o')) # double the row

        self.column_checker.reverse()
        self.universe_width += len(self.column_checker)
        self.universe_height = 0
        self.expanded_universe = []
        self.galaxies = []
        for row in self.universe:
            self.universe_height += 1
            for column in self.column_checker:
                row = row[0:column] + 'o' + row[column:]
            self.expanded_universe.append(row)

        for y in range(0,self.universe_height):
            for x in range(0,self.universe_width):
                if self.expanded_universe[y][x] == '#':
                    self.galaxies.append((x,y))

        self.galaxy_pairs = list(combinations(self.galaxies,2))

    def p1(self):
        self.p1_solution = 0
        for pair in self.galaxy_pairs:
            start_x, start_y = pair[0][0], pair[0][1]
            end_x, end_y = pair[1][0], pair[1][1]
            
            distance = 0
            if start_x > end_x:
                x_inc = -1
            else:
                x_inc = 1
                
            if start_y > end_y:
                y_inc = -1
            else:
                y_inc = 1
                
            for x in range(start_x, end_x, x_inc):
                    distance += 1
            
            for y in range(start_y,end_y,y_inc):
                    distance += 1
            
            self.p1_solution += distance
        return True

    def p2(self):
        self.p2_solution = 0
        for pair in self.galaxy_pairs:
            start_x, start_y = pair[0][0], pair[0][1]
            end_x, end_y = pair[1][0], pair[1][1]
            
            distance = 0
            if start_x > end_x:
                x_inc = -1
            else:
                x_inc = 1
                
            if start_y > end_y:
                y_inc = -1
            else:
                y_inc = 1
                
            for x in range(start_x, end_x, x_inc):
                if self.expanded_universe[start_y][x] == "o":
                    distance += 999999
                else:
                    distance += 1
            
            for y in range(start_y,end_y,y_inc):
                if self.expanded_universe[y][end_x] == "o":
                    distance += 999999
                else:
                    distance += 1
            
            self.p2_solution += distance
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