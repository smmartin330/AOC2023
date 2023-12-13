from aoc import *
from puzzle_data import *

from time import time
from itertools import combinations
import re

DAY = 12

PATTERN = r"(?<![?#])#{groupsize}(?![#?])"

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

class SpringRow():
    def __init__(self,row):
        row = row.split(' ')
        self.springs = row[0]
        self.groups = [int(group) for group in row[1].split(',')]
        self.group_count = len(self.groups)
        self.length = len(self.springs)
        
        self.spaces_needed = sum(self.groups) + ( self.group_count - 1 )
        self.empty_spaces = self.length - self.spaces_needed
        
        self.combos = list(combinations(range(self.group_count+self.empty_spaces),self.group_count))
        self.count = len(self.combos)
 
class Puzzle():
    def __init__(self,input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split('\n')

        self.spring_rows = []
        
        for row in self.input_list:
            self.spring_rows.append(SpringRow(row))
        
        
        

    def p1(self):
        self.p1_solution = 0
        for row in self.spring_rows:
            self.p1_solution += row.count

          
        return True

    def p2(self):
        self.p2_solution = 0
        
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