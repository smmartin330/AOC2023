from aoc import *
from puzzle_data import *
from collections import deque

from time import time

DAY = 15


def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"


def hash_string(string, current_value=0):
    """
    Determine the ASCII code for the current character of the string.
    Increase the current value by the ASCII code you just determined.
    Set the current value to itself multiplied by 17.
    Set the current value to the remainder of dividing itself by 256.
    """
    new_value = current_value
    ascii_val = ord(string[0])
    remaining_string = string[1:]
    new_value += ascii_val
    new_value *= 17
    new_value = new_value % 256

    if remaining_string == "":
        # print(f'Returning: {new_value}')
        return new_value
    else:
        return hash_string(remaining_string, new_value)


class Puzzle:
    def __init__(self, input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split(",")

    def p1(self):
        self.p1_solution = 0

        for instruction in self.input_list:
            self.p1_solution += hash_string(instruction)
        return True

    def p2(self):
        boxes = []
        
        for x in range(0, 256):
            boxes.append(deque([]))

        self.p2_solution = 0
        for instruction in self.input_list:
            
            # Each step begins with a sequence of letters that 
            # indicate the label of the lens on which the step
            # operates. The result of running the HASH algorithm 
            # on the label indicates the correct box for that step.
            label = instruction[0:2]
            box_number = hash_string(label)
            # The label will be immediately followed by a character 
            # that indicates the operation to perform: either an 
            # equals sign (=) or a dash (-).
            operation = instruction[2]
            
            
            if operation == '-':
                remove_lens = False
                # if operation is -:
                # go to relevant box
                # remove lens w/ given label IF PRESENT.
                # move any remaining lenses as far forward as they can go w/o changing order.
                # If no lens in that box has the given label, NOTHING HAPPENS.
                for lens in boxes[box_number]:
                    if lens[0] == label:
                        remove_lens = True
                if remove_lens == True:
                    boxes[box_number].remove((label,lens[1]))
            
            elif operation == '=':
                lens_index = False
                add_lens = False
                # If operation is an =
                    # Number is a focal length of lens
                focal_length = instruction[3]
                # mark lens w/ label
                new_lens = (label,focal_length)
                if len(boxes[box_number]) == 0:
                    boxes[box_number].appendleft(new_lens)
                else:
                    for lens in boxes[box_number]:
                        if lens[0] == label:
                            lens_index = boxes[box_number].index(lens)
                            break
                        else:
                            add_lens = True
                            # if there is not already a lens w/ same label
                            # add lens behind any others in the box.
                    if add_lens == True:
                        boxes[box_number].appendleft(new_lens)
                    if lens_index != False:
                        boxes[box_number][lens_index] = new_lens

        for box in boxes:
            box_power = 0
            for lens in box:
                box_power += int(lens[1])
                
            self.p2_solution += box_power
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
