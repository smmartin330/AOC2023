from aoc import *
from puzzle_data import *

from time import time
import copy

DAY = 16

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

def beam_tracer(start_beams,contraption):
    contraption_after = contraption.copy()
    beams = start_beams.copy()
    loop_finder = set()

    while len(beams) > 0:
        new_beams = []
        beam = beams.pop(0)
        loop_finder.add(beam)
        b_x,b_y,direction = beam[0],beam[1],beam[2]
        contraption_after[b_y] = contraption_after[b_y][0:b_x] + "#" + contraption_after[b_y][b_x+1:]
        match direction:
            case "R":
                next_x = b_x + 1
                next_y = b_y
            case "L":
                next_x = b_x - 1
                next_y = b_y
            case "U":
                next_x = b_x
                next_y = b_y - 1
            case "D":
                next_x = b_x
                next_y = b_y + 1
        try:
            if next_x >= 0 and next_y >= 0:
                next_char = contraption[next_y][next_x]
                match next_char:
                    case '.':
                        next_dir = direction
                    case '+':
                        match direction:
                            case "R":
                                next_dir = "D"
                            case "L":
                                next_dir = "U"
                            case "U":
                                next_dir = "L"
                            case "D":
                                next_dir = "R"                    
                    case '/':
                        match direction:
                            case "R":
                                next_dir = "U"
                            case "L":
                                next_dir = "D"
                            case "U":
                                next_dir = "R"
                            case "D":
                                next_dir = "L"   
                    case '-':
                        match direction:
                            case "R":
                                next_dir = direction
                            case "L":
                                next_dir = direction
                            case "U":
                                next_dir = "SRL"
                            case "D":
                                next_dir = "SRL"   
                    case '|':
                        match direction:
                            case "R":
                                next_dir = "SUD"
                            case "L":
                                next_dir = "SUD"
                            case "U":
                                next_dir = direction
                            case "D":
                                next_dir = direction
            
                match next_dir:
                    case "SRL":
                        new_beams.append((next_x,next_y,"R"))
                        new_beams.append((next_x,next_y,"L"))
                    case "SUD":
                        new_beams.append((next_x,next_y,"U"))
                        new_beams.append((next_x,next_y,"D"))
                    case _:
                        new_beams.append((next_x,next_y,next_dir))
                
        except:
            pass
            # Beam leaving the playing field, discard it.
        
        for new_beam in [ new_beam for new_beam in new_beams if new_beam not in loop_finder ]:
            beams.append(new_beam)
            loop_finder.add(new_beam)
        
    energized = 0
    for row in contraption_after:
        energized += row.count("#")
        
    return energized  


class Puzzle():
    def __init__(self,input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split('\n')

        
    def p1(self):
        self.p1_solution = 0
        self.contraption = self.input_list
        self.contraption_after = self.contraption.copy()
        
        self.beams = [ ]
        if self.contraption[0][0] == '+' or self.contraption[0][0] == '|':
            start_beam = (0,0,"D")
        else:
            start_beam = (0,0,"R")
        
        self.p1_solution = beam_tracer([start_beam],self.contraption)
        return True

    def p2(self):
        self.p2_solution = 0
        self.contraption = self.input_list
        self.mirror_counts = []
        
        top_edge = []
        bottom_edge = []
        left_edge = []
        right_edge = []
        for x in range(0,len(self.contraption[0])):
            top_edge.append((x,0))
            bottom_edge.append((x,len(self.contraption)-1))
        
        for y in range(0,len(self.contraption)):
            left_edge.append((0,y))
            right_edge.append(((len(self.contraption[0])-1,y)))
            
        for start in top_edge:
            start_x,start_y = start[0],start[1]
            start_beams = [ ]
                        
            if self.contraption[start_y][start_x] == '+': # \
                start_beams.append((start_x,start_y,"R"))
            elif self.contraption[start_y][start_x] == '/':
                start_beams.append((start_x,start_y,"L"))
            elif self.contraption[start_y][start_x] == '-':
                start_beams.append((start_x,start_y,"R"))
                start_beams.append((start_x,start_y,"L"))
            else:
                start_beams.append((start_x,start_y,"D"))
            
            if (4,0,'D') in start_beams:
                pass
            
            this_energized = beam_tracer(start_beams,self.contraption)
            self.mirror_counts.append(this_energized)
                
        for start in bottom_edge:
            start_x,start_y = start[0],start[1]
            start_beams = [ ]
            
            if self.contraption[start_y][start_x] == '+':
                start_beams.append((start_x,start_y,"L"))
            elif self.contraption[start_y][start_x] == '/':
                start_beams.append((start_x,start_y,"R"))
            elif self.contraption[start_y][start_x] == '-':
                start_beams.append((start_x,start_y,"R"))
                start_beams.append((start_x,start_y,"L"))
            else:
                start_beams.append((start_x,start_y,'U'))
            
            this_energized = beam_tracer(start_beams,self.contraption)
            self.mirror_counts.append(this_energized)
            
        for start in left_edge:
            start_x,start_y = start[0],start[1]
            start_beams = [ ]
            
            if self.contraption[start_y][start_x] == '+': # \
                start_beams.append((start_x,start_y,"D"))
            elif self.contraption[start_y][start_x] == '/':
                start_beams.append((start_x,start_y,"U"))
            elif self.contraption[start_y][start_x] == '|':
                start_beams.append((start_x,start_y,"U"))
                start_beams.append((start_x,start_y,"D"))
            else:
                start_beams.append((start_x,start_y,'R'))
            
            this_energized = beam_tracer(start_beams,self.contraption)
            self.mirror_counts.append(this_energized)

        for start in right_edge:
            start_x,start_y = start[0],start[1]
            start_beams = [ ]
            
            if self.contraption[start_y][start_x] == '+': # \
                start_beams.append((start_x,start_y,"U"))
            elif self.contraption[start_y][start_x] == '/':
                start_beams.append((start_x,start_y,"D"))
            elif self.contraption[start_y][start_x] == '|':
                start_beams.append((start_x,start_y,"U"))
                start_beams.append((start_x,start_y,"D"))
            else:
                start_beams.append((start_x,start_y,'L'))
            
            if (0,5,'D') in start_beams:
                pass
            this_energized = beam_tracer(start_beams,self.contraption)
            self.mirror_counts.append(this_energized)

        self.p2_solution = max(self.mirror_counts)
          
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