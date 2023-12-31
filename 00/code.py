from aoc import *
from puzzle_data import *

from time import time

DAY = 0

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

class Puzzle():
    def __init__(self,input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split('\n')

        

    def p1(self):
        self.p1_solution = 0

          
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