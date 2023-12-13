from aoc import *
from puzzle_data import *

from time import time

DAY = 13


def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"


def check_mirror(pattern, required_smudges=0):
    for row in range(1, len(pattern)):
        smudges = 0
        offset = 0
        max_offset = abs(row - len(pattern))
        max_offset = min([row, max_offset])
        possible_fold = True
        for offset in range(0, max_offset):
            bottom = pattern[row + offset]
            top = pattern[row - (offset + 1)]
            if bottom == top:
                offset += 1
            else:
                for x in range(0, len(bottom)):
                    if top[x] != bottom[x]:
                        smudges += 1
                    if smudges > required_smudges:
                        break
                    else:
                        offset += 1
            if smudges > 1:
                possible_fold = False
                break
        if possible_fold == True and smudges == required_smudges:
            return (True, row, smudges)
    return (False, False, False)


class Pattern:
    def __init__(self, pattern):
        self.pattern = pattern.split("\n")
        self.pattern = [list(pattern) for pattern in self.pattern]
        self.width = len(self.pattern[0])
        self.height = len(self.pattern)
        self.pattern_t = []

        for row in self.pattern:
            for x in range(0, self.width):
                try:
                    self.pattern_t[x].append(row[x])
                except:
                    self.pattern_t.append([row[x]])

        self.pattern_t.reverse()


class Puzzle:
    def __init__(self, input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split("\n\n")

    def p1(self):
        self.p1_solution = 0
        self.patterns = []

        for pattern in self.input_list:
            this_pattern = Pattern(pattern)
            vertical_fold = check_mirror(this_pattern.pattern_t)
            if vertical_fold[0] == True:
                self.p1_solution += this_pattern.width - vertical_fold[1]
                continue
            horizontal_fold = check_mirror(this_pattern.pattern)
            if horizontal_fold[0] == True:
                self.p1_solution += horizontal_fold[1] * 100
                continue

            raise ValueError(f"Invalid pattern: \n {this_pattern.pattern}")
        return True

    def p2(self):
        self.p2_solution = 0
        self.patterns = []

        for pattern in self.input_list:
            this_pattern = Pattern(pattern)
            vertical_fold = check_mirror(this_pattern.pattern_t, required_smudges=1)
            if vertical_fold[0] == True and vertical_fold[2] == 1:
                self.p2_solution += this_pattern.width - vertical_fold[1]
                continue
            horizontal_fold = check_mirror(this_pattern.pattern, required_smudges=1)
            if horizontal_fold[0] == True and horizontal_fold[2] == 1:
                self.p2_solution += horizontal_fold[1] * 100
                continue

            raise ValueError(f"Invalid pattern: \n {this_pattern.pattern}")

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
            print(
                f"Sample failed; Expected {P1_SAMPLE_SOLUTION}, got {sample.p1_solution}"
            )
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            puzzle = Puzzle(input_text=PUZZLE_INPUT)
            puzzle.p1()
            print("Processing Input...\n")
            start_time = time()
            print(f"SOLUTION: {puzzle.p1_solution}")
            print(f"Elapsed time {elapsed_time(start_time)}")

    if P2_SAMPLE_SOLUTION:
        print("PART 2\nTesting Sample...\n")
        start_time = time()
        sample.p2()
        if P2_SAMPLE_SOLUTION == sample.p2_solution:
            print("Sample correct.")
        else:
            print(
                f"Sample failed; Expected {P2_SAMPLE_SOLUTION}, got {sample.p2_solution}"
            )
        print(f"Elapsed time {elapsed_time(start_time)}")
        if PUZZLE_INPUT:
            print("Processing Input...\n")
            start_time = time()
            puzzle.p2()
            print(f"SOLUTION: {puzzle.p2_solution}")
            print(f"Elapsed time {elapsed_time(start_time)}")


if __name__ == "__main__":
    main()
