import argparse
from time import time
import json
import numpy


DAY = 3

P1_TEXT = '''
--- Day 3: Gear Ratios ---

You and the Elf eventually reach a gondola lift station; he says the gondola lift will take you up to the water source, but this is as far as he can bring you. You go inside.

It doesn't take long to find the gondolas, but there seems to be a problem: they're not moving.

"Aaah!"

You turn around to see a slightly-greasy Elf with a wrench and a look of surprise. "Sorry, I wasn't expecting anyone! The gondola lift isn't working right now; it'll still be a while before I can fix it." You offer to help.

The engineer explains that an engine part seems to be missing from the engine, but nobody can figure out which one. If you can add up all the part numbers in the engine schematic, it should be easy to work out which part is missing.

The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part number" and should be included in your sum. (Periods (.) do not count as a symbol.)

Here is an example engine schematic:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, two numbers are not part numbers because they are not adjacent to a symbol: 114 (top right) and 58 (middle right). Every other number is adjacent to a symbol and so is a part number; their sum is 4361.

Of course, the actual engine schematic is much larger. What is the sum of all of the part numbers in the engine schematic?
'''

P2_TEXT = '''
The engineer finds the missing part and installs it in the engine! As the engine springs to life, you jump in the closest gondola, finally ready to ascend to the water source.

You don't seem to be going very fast, though. Maybe something is still wrong? Fortunately, the gondola has a phone labeled "help", so you pick it up and the engineer answers.

Before you can explain the situation, she suggests that you look out the window. There stands the engineer, holding a phone in one hand and waving with the other. You're going so slowly that you haven't even left the station. You exit the gondola.

The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.

This time, you need to find the gear ratio of every gear and add them all up so that the engineer can figure out which gear needs to be replaced.

Consider the same engine schematic again:

467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
In this schematic, there are two gears. The first is in the top left; it has part numbers 467 and 35, so its gear ratio is 16345. The second gear is in the lower right; its gear ratio is 451490. (The * adjacent to 617 is not a gear because it is only adjacent to one part number.) Adding up all of the gear ratios produces 467835.

What is the sum of all of the gear ratios in your engine schematic?
'''

SAMPLE_INPUT = '''
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''

PUZZLE_INPUT = '''
.242......276....234............682.......................958..695..742................714......574..............833.........159....297.686.
.............*............................612*......304..*..........*.......@175...#...*...........*890...........*.............*..*........
..........346......................997........923......*..253..........698........122.746.....-832..........766.432..229.....674....415.....
...............#76...........332....*...............111...........785..............................=..720..*........*.......................
........204............396..*.....357..438*694...............154.................................26...*....422...200.../201.................
....859*......496.598.+....810........................816.......*713...........802#.........330......540...........................%344.....
..............*.....*..........344.......................*.............671............994.................467...............................
........$..388.........152*141..*......73.719...$526....830...759......%......943............541.624.781...*...$150.............966.........
.....877.......................67.....*.....*.............................859..*..502+........$..*.....*.425........778.../........*........
................142.....569..........563...57......786..........303.......*...255.......*638....979..704...........*.......181..............
...........560.....%....+......................276...=..................939..........194.........................675..............741.......
......681...*..................882..714................741......650.........&.................374...542/..........................*.........
344*.....%.340......$.....%......=.....*.....799...990...*.........*733..811.....................-...............8........844...660.........
....937.........301.227.775.24+....=.146..../.....*.......983...+.....................*822.898&.................*.....611*..............693.
...........&.....................328............254..582.......528...359&..........536..........*889........%...........................#...
..901.497.9.........473................193...........*....................168...........................382.450..@..........................
..............................279..612..*..........795.......431......$............104....................*.......988....................920
............614....478..430+....*..../...505...363...................195....642....-............493....852...612.........556................
.............*................570....................961.....................=........178...23.$..................667...........=....415....
...323*795....363.................414%.........$....@..................54.........680*.....*.....415.......34..........598.......74.........
..................904.124....766.........-..546....................-........100........167.424..*.........%.........83*................*....
..906@.+.....-......&..........*..951.342.......208...........887...711....*...........*........627...............................=597..478.
.......323.187..+.............192...@......367.*.....107.........$......715.....923....103...........*991.....+....749..146.................
.................170.....511...........-................*...........943.....95..............................215.........*.....126...........
..166................809..*.........590...733.896.....575.333.......*......*...229...122.........................%.......860..-...315.......
.....*856....4.....%.-...826.174............&...*............*..851..655...692..*......*....*................346..659.......................
.............+...77............&.541$...........227.......329.....*............483..463...551....38......527.*...............168.....665@...
....915..635.........960...209........710.....................538..449..........................*.........*..586......574...................
..../.../.....61............*...........*...489..........510..@...........#.........254....52.411........894......932..*...206.121....=911..
..................900..525.450.591...#..178.+..............%......125...433...362..*.......*.......................*..111.....*.............
.........736*134...*....*..........720..........#...................*.........&.....197..450......................252...........=516........
...................638.314.....................510.........*..475....629...............................................930..................
...........................926......../....*.......776....798../................/..............982..............437.....@.....937...........
....502-........-595..........*.....439.282.965...............................+..853..884.419..+......244*873....*........#....*.......309..
...............................257..............937...413.199...@195..../....248.....+.....*..................100..585.....791..959.........
...............*912.......410......@...........*.........*.............4....................321....................*........................
......653..................*.......817..#511.131..=785.........468/......128........#144..............*170...559..146..........625/..976....
......&..................997..............................711..............*.................792...450......$..............12..........#....
..................412.....................33...............*................672...=........3...*.7.................739.567...........#......
......................569#.#.......850....*......381........621.253+...............355....*..942../........371.....*....*....285*118.754....
.....-......................899............327...*.....................+........*......575..........*892........618......511................
...91............................958-..........532..................914......925.............=.457&..........#......948*..........27.....382
...................771......857.......-..................79...............................156.........938....389........353...502*..........
..............................*.......847...............*....238....................161..............*.............*................164.660.
..995..........872.....690.....888...........69..=123..353......*..621..736*........+...87...887....518...........590...429....*254...&.*...
....*.584.631.......$....................980.*...............569......*.....14..........*.....*...............399..........*.............199
..446..-..%.........200.933...385*.........*..150..........=..........169........374#.322......806...........+.....*........553.............
............@66.........*.........559...580.................120..147-..............................757..............933............644......
.....................641...943................143..634.648................-...288...................*.............+.........%....$...*......
..........273.............-...............430....&......@.........*.......876./........826..........67.......801.86......121.....210........
...842....=...................599*17..182*.....@...................902.............980*........................@.............826............
....*.......238................................769.....-.......................124......763...........98.491.....420....@901.*.........84...
...564.......&...........296........................503...591..967......162...=.........*...238..386........#.........#......629.26.........
...................423......*723........559$...................*..................849...342........./...............521............@........
..833*.....3*974..+..............718..........884.#.............503..........284.....*.........223......................................*...
......................532....=.....*..........*....255.............................287..................31...........*....757%.977.......753
640.....846...............252.....351.....372.258......................................871.........@33..*..149....624..........*.....537....
...=.........495.....846..............526*..............622....*899.....870......81......%...&.........786...............891...668..........
................*......*.....................+.........*....211.....498....*......-.654....368.....................916.................698..
986......629....115..749.........=....925.858..........233............*.151....78......@.......593..684........916...@......................
.........&....@................@.500.%.........681..+.........431...488..........*932....291=.#.......*........*.........782....$799........
.....131.....319.944.........577...............*.....777.....................448................614..901..287..722.....&...*................
....*....157.......*........................966...........442#....472..925...#...359..519......*.........*............937.39..........%639..
..388......*..266..703...........................................*........@.........*....*......109....424......672...............601.......
...........89...=.................911...949.....#.............487....61.......*491.822.113.................250........*34............*9.....
..15...............345....703..%....*...-....673....239...191........*........................26.130.......*........20........393...........
....*991..%..........*.......*..453.70...............#.....-..597.491...328.....122..........*..........492....701......508....*..274.......
...........838........893...............53..658.865........................#....*.....-....570........$...........&........*........./...486
................438.............71.............*.....854..+..107*647...200......575...932...........573....606...........850................
................../.........838...*674..............#....69.............*......................534.........*..................235*..........
.....877*8............184...*.................................*.........191...........*707........*...198..363......305.*338......392..657..
.................98...=....953...362......148...335.........781.............484....608............207.*..............*......................
................................*........*........@...............584@......%................418.......675.......520..260.............639...
41.$....952....133@.999......953..*.....64...792.................................$....111.......*...................*.................*.....
...572....*.........+............18............+.494..694.......+.....93.......443....#......861..................304...696....+487...89....
...........3............................................+.....461.868...*........................596...#.710..793.......%...................
................362.................%684.........716...................420...............53......*...706.......*../.......@142......*.......
........@...696...*......489....434...............*........................670.......187*......992...........730.48..............443.986....
.......904.....*.260....%..........#.139.....850..592..187.....137..987.......=.195................366..%.............596.427/..............
............284.............*141...../...739...............131......*...........@..........510......*..112...-........*.....................
......192................313.......*........*.......43*......*.....309......557......669.....+.....386.......765.....567......758.287.......
..139...........................535.848..#..519........277....778..........*.........*...................526...................*......968...
.....*....-........664..45..............426..........................603.560..&558...909...................%....934......392.395............
......755..928......-......197....126..................227.......689.+....................170.....@805.............*122.....................
..........................*.........*........909.......*...........*............263..475......201......193..................689..799.../2...
...407..977.........918%...109...332.........*.......910.........730...170.........*....*428....*.....$........185..637......&..............
...../...$....713....................501......842.........258............*.........872.......822..879....*626....*....*........255.......229
................*.....633*631.....=....*..................................722.....................*...736........339.171..........-..279....
...531*393......714............828......384.830.....90..............................683.........647............&...........820@.......*.....
...........3...........965.........153........*.....................552.-.....709....*......413..........503....831.............289....138..
..........*...906......*......................34..692.........941..+....205.....@..73..........*................................+...........
.........830./........473..388.648........563....*..............*.....................589.....345.....276..........=.471.931........854.....
135*315..........-604.........*....$.......&......134...=....565.......65.............../.............+.........866....=.%.....908.....*....
....................................446......751.........437.....@.......*.140.....495....607#..783........625.............734*.......758...
...........141......915.....................*.....*...............137.664....&..29.+............/.....113#.*......118.290........715........
..614.396...........*......................459.....368..........................*...........352.............254..*....*............@...168..
.....*............746....859..........650........%.....735....../....../198......619..718......-..................147.909..826.......*......
.........79.............*.............=..........808...*........306.....................@.618......659..3...................*.....852.714...
...157....*.901...957...422...369.......................236.............289........893.......*..............184*399..........958............
...*........*.......................370.../....................2.990.62..../..........*......992...91.................816...................
...419..731..546..868*10..726........*..13..@........................./.........326.94..829.......%.............@...................354.....
..........*....................868..377.....319.....122=.787................463.........*...*.311...384..........418....774........*........
..........762.#...&906........*..........................*........464.....*....*.....242..324.+...........444..............*..821.128.......
..............918..........375.........%825....&.........27...227*.........711.239.........................*..............838.-........496..
....783............................$...........661.....&.............................839.................508.........%......................
.....*.....106........138....50.....237..............776...&............................*..&825......337......*...550.......337..587#.......
..878.....*....391...=........*.733.......................32....353+..................265.......944..*...516..635...........*.........761...
........212................716................444=...........*.......73....469............=..#.$....823..@...............105................
...................68..=.............626...............@...88.531..............981......139.37.....................................522......
.........898.......*..255........969*.......593*886....222.........860.497*168....*.150..................................586..........*.....
............*177..58......681...........928..................131.....*..........560..#............................536......*...........860..
..613......................*....-.......#.....363........701....*.116...565.....................-348....874...953..$..671..748..............
......................$..408.....139.........*.............*............=..............615............*....+..*..........*............41....
.....710..343....@...391.............$.....181..778........795..........................*.............201......875.....22...............*...
629...*..*......769........482.....511.........*......699..........366...%510........518....101...424.......................................
....374...875.........804...*...................395......*.........*.............162.......*.........*..........959............298$.........
..............74.834.........345.....=..540.248.........401....977..454.695.....*....................17........*......536...@...............
......807.......*........780.........54....*....................*........*...294...720...14&.................245........%....773......960...
.........$..132..........*.......652..........$....907.....@.344....848=.397..........*......747............................................
....541*....&...*.....663...146...........364..611....*.440.....................455.336.209.......751....539................................
........408.....377...........*..............*......541.........&.......988*150...*.......-........=....*.........#...../..39..306+.........
...%325..................*49...37.............922........344#...717.............179.400...............617.874...943...232...................
...........424........569............865.............978...................978......-......+....23=..........*..............................
..........=....................782..*.........755........41......823.......@...............427............484.......-.....310.......401.....
...........................&..*....704....168*......264.............@...............240*...........................190................*..384
617*.........710.....28.492..425............................-....4......=...757*283.....674....467....680......775.............$.....826....
....975.....+........*...........100..........795..........67..........91...........946...........................*......138...390..........
..........*.........808.............*474.....+.....141.........156.....................*..........194...........273.473..*...@.....86..+....
.......589.919..........452.....842.......*.......*....472........*..................765...........*........$.........$..79.644.........905.
................452.....%.........*....223........121.*............816.-949..837..............-830...818.451.....703........................
.527..934.625.....*..........461...........842-.......455.....................@...866..97...........*..............$..819...............*919
................472.........*..........930............................208.........*...&.........767.563....%..../......*..422...............
.......%.389..............993..325.650..............344...*................651.379..............+.......516......607.142..+....284%.........
....575.............498...........*.....760...+.........47.385....#.91......*...........957.......@.........................................
.............588....*......./389.........*..839................567..*.....607..............*......377..460=...............260......491.282..
.....137.........340................961.................383*.......295........................506...........*.....................*....*....
......../..670..............52.....*.......802..950.........207..........334..377.625.....871...*........622..160.130..#.....295.30...216...
.............*............=.*.......34.941.=.......*............&.12......*....*...........*...20..356...........*......804.*...............
..........335..........562...258........*..........761.......758...*.....................602................................955........512..
.........................................882........................730..........................566..............................202.......
'''

P1_SAMPLE_SOLUTION = 4361

P2_SAMPLE_SOLUTION = 467835

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

def look_right(sarch_pos,grid):
    try:
        lookup = grid.pos(sarch_pos,x_offset=1)
        return lookup
    except:
        return False

def look_left(sarch_pos,grid):
    try:
        lookup = grid.pos(sarch_pos,x_offset=-1)
        return lookup
    except:
        return False

class Grid: # We're bringing this back from 2022! Maybe!
    def __init__(self, raw_grid) -> None:
        """takes in the input data (a list of strings) and converts it to a 2D array (a list of lists). provides functionality to search the grid easily. provide raw_grid (the puzzle input processed as a list)

        Args:
            raw_grid (list): the puzzle data for processing.
            
        values:
            self.gridmap (list): a 2D array. (x,y) is found at self.gridmap[y][x]
            self.gridmap_t (list): the 2D array transposed along axes so that (x,y) is found at self.gridmap[x][y]
            self.unique_values (list): all unique values found in the grid
            self.height (int): the height of the grid (how many rows)
            self.width (int): the width of the grid (how many columns)
            self.every_node (list): a list of every node that can be used for elimination of possibilities.
        """
        self.gridmap = []
        self.unique_values = []
        for row in raw_grid:
            this_row = []
            for char in row:
                this_row.append(char)
                if char not in self.unique_values:
                    self.unique_values.append(char)
            self.gridmap.append(this_row)

        self.gridmap_t = numpy.transpose(self.gridmap).tolist()
        self.height = len(self.gridmap)
        self.width = len(self.gridmap_t)
        self.every_node = []
        for x in range(0, self.width):
            for y in range(0, self.height):
                self.every_node.append((x, y))

    def pos(self, coordinate, x_offset=0, y_offset=0):
        """Returns the value either at a particular coordinate or at a particular offset from that coordinate.

        Args:
            coordinate (list): the coordinate itself
            x_offset (int, optional): the x-offset to the coordinate. negative values to the left, positive to the right. Defaults to 0.
            y_offset (int, optional): the y-offset to the coordinate. negative values towards the top, positive towards the bottom. Defaults to 0.

        Returns:
            str: the value found. 
        """
        x, y = coordinate[0] + x_offset, coordinate[1] + y_offset
        return self.gridmap[y][x]

    def pos_set(self, coordinate, new, x_offset=0, y_offset=0):
        """set the value at a coordinate

        Args:
            coordinate (list): the coordinate itself
            new (str): the new value to set
            x_offset (int, optional): the x-offset to the coordinate. negative values to the left, positive to the right. Defaults to 0.
            y_offset (int, optional): the y-offset to the coordinate. negative values towards the top, positive towards the bottom. Defaults to 0.

        Returns:
            bool: confirmation of success (needs error handling.)
        """
        x, y = coordinate[0] + x_offset, coordinate[1] + y_offset
        self.gridmap[y][x] = new
        self.gridmap_t[x][y] = new
        return True
    
    def adj(self, coordinate) -> "dict":
        """provides a dictionary of all adjacents, including diagonals, and their values.

        Args:
            coordinate (list): the coordinate itself

        Returns:
            dict: the adjacent coordinates and their values. 
        """
        x, y = coordinate[0], coordinate[1]
        adj = {}
        adj_x = list(range(max(0, x - 1), min(self.width, x + 2)))
        adj_y = list(range(max(0, y - 1), min(self.height, y + 2)))
        for _x in adj_x:
            for _y in adj_y:
                if (_x, _y) != (x, y) and self.gridmap[_y][_x] != ".":
                    adj[(_x, _y)] = self.gridmap[_y][_x]

        return adj

    def adj_card(self, coordinate) -> "dict":
        """returns a dictionary of only cardinally adjacent coordinates and their values.

        Args:
            coordinate (list): the origin coordinate

        Returns:
            dict: the cardinally adjacent coordinates and their values. 
        """
        x, y = coordinate[0], coordinate[1]
        adj_card = {}

        if x > 0 and self.gridmap[y][x] != ".":
            adj_card[(x - 1, y)] = self.gridmap[y][x - 1]
        if x < self.width - 1 and self.gridmap[y][x] != ".":
            adj_card[(x + 1, y)] = self.gridmap[y][x + 1]
        if y > 0 and self.gridmap[y][x] != ".":
            adj_card[(x, y - 1)] = self.gridmap[y - 1][x]
        if y < self.height - 1 and self.gridmap[y][x] != ".":
            adj_card[(x, y + 1)] = self.gridmap[y + 1][x]

        return adj_card
    
    def adj_x(self, coordinate) -> "dict":
        """returns a dictionary of the horizontal adjacencies

        Args:
            coordinate (list): the origin coordinate

        Returns:
            dict: the horizontally adjacent coordinates and their values. 
        """
        x, y = coordinate[0], coordinate[1]
        adj_x = {}

        if x > 0 and self.gridmap[y][x] != ".":
            adj_x[(x - 1, y)] = self.gridmap[y][x - 1]
        if x < self.width - 1 and self.gridmap[y][x] != ".":
            adj_x[(x + 1, y)] = self.gridmap[y][x + 1]

        return adj_x
    
    def adj_y(self, coordinate) -> "dict":
        """returns a dictionary of vertically adjacent coordinates and their values.

        Args:
            coordinate (list): the origin coordinate

        Returns:
            dict: the vertically adjacent coordinates and their values. 
        """
        x, y = coordinate[0], coordinate[1]
        adj_y = {}

        if y > 0 and self.gridmap[y][x] != ".":
            adj_y[(x, y - 1)] = self.gridmap[y - 1][x]
        if y < self.height - 1 and self.gridmap[y][x] != ".":
            adj_y[(x, y + 1)] = self.gridmap[y + 1][x]

        return adj_y

class Symbol():
    def __init__(self,coordinate,symbol):
        self.coordinate = coordinate
        self.symbol = symbol
        self.parts = []

class Puzzle():
    def __init__(self,input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split('\n')
                
    def p1(self):
        
        self.engine = Grid(raw_grid=self.input_list)
        
        # identify all the unique symbols
        not_symbols = ['.', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        numbers = [ '1', '2', '3', '4', '5', '6', '7', '8', '9', '0' ]
        self.symbols = [ char for char in self.engine.unique_values if char not in not_symbols ]
        
        # initialize list of part numbers
        self.part_numbers = []
        self.p1_solution = 0
        
        # initialize a list of coordinates already identified as part of a part number
        self.symbol_nodes = {}
        part_number_nodes = {}
        
        # search through the grid for symbols
        for y in range(0, self.engine.height):
            for x in range(0, self.engine.width):
                this_pos = (x,y)
                this_val = self.engine.pos((x,y))
                part_number = '' # clear the part number
                if this_pos not in self.symbol_nodes: # if we have not searched this node as adjacent to a symbol already
                    if self.engine.gridmap[y][x] in self.symbols: # if it is a symbol
                        self.symbol_nodes[this_pos] = Symbol(this_pos,this_val) # create an entry for the symbol
                        adj = self.engine.adj(this_pos) # get the adjacents
                        for pos,val in adj.items(): # for each adjacent
                            if pos not in part_number_nodes:
                                # pos remains our starting value so after we search to the right, we can return and search left.
                                part_number_nodes[pos] = val # mark the node as searched
                                if val in numbers: # if the value is a number
                                    part_number = val # initialize the part number string with the found number
                                    search_pos = pos # mark where we are searching and start looking to the right for the end of the number
                                    next_val = True # initialize our next_val for while loop
                                    while next_val != False: # until we hit a not-number
                                        next_val = look_right(search_pos,self.engine)
                                        if next_val in numbers: # if we find a number
                                            part_number += next_val # append it to the part number
                                            search_pos = (search_pos[0]+1,search_pos[1]) # update the search position
                                            part_number_nodes[search_pos] = val # mark the node as searched # add that node to searched
                                        else:
                                            next_val = False # mark next_val as bad and get out of the loop
                                    search_pos = pos # return to the original position and start looking left for the beginning
                                    next_val = True # initialize our next_val for while loop
                                    while next_val != False: # until we hit a not-number
                                        next_val = look_left(search_pos,self.engine)
                                        if next_val in numbers: # if we find a number
                                            part_number = next_val + part_number # prepend it to the part number
                                            search_pos = (search_pos[0]-1,search_pos[1]) # move the search position left
                                            part_number_nodes[search_pos] = val # mark the node as searched # add that node to searched                                            
                                        else:
                                            next_val = False # mark next_val as bad and get out of the loop
                            if part_number != '': # if we've built a part number
                                self.symbol_nodes[this_pos].parts.append(part_number) # add the part number to the symbol
                                self.part_numbers.append(part_number) # add the part numbrer to the list of part numbers (ended up not being needed.)
                                self.p1_solution += int(part_number) # add the part number to the solution total
                                part_number = '' # clear the part number buffer
        
        return True

    def p2(self):
        self.p2_solution = 0
        for symbol, data in self.symbol_nodes.items(): # look at all the symbols
            if data.symbol == "*" and len(data.parts) > 1: # if it is a * with two parts, it's a gear
                self.p2_solution += int(data.parts[0]) * int(data.parts[1]) # the gear ratio is the product of the two parts. calculate and add to solution.
        return True

def main():
    parser = argparse.ArgumentParser(description=f'AOC2023 Puzzle Day { DAY }')
    parser.add_argument("-p", "--showpuzzle", help="Display Puzzle Text", action='store_true')
    parser.add_argument("-s", "--showsample", help="Display Sample Input", action='store_true')
    args = parser.parse_args()
    
    if args.showpuzzle:
        print(f"###############\nAOC 2023 DAY {DAY} PUZZLE TEXT\n###############")
        print(f"###############\nPART ONE\n###############")
        print(P1_TEXT)
        print(f"###############\nPART TWO\n###############")
        print(P1_TEXT)
    
    if args.showsample:
        print(f"###############\nAOC 2023 DAY {DAY} SAMPLE INPUT\n###############")
        print(SAMPLE_INPUT.strip())
        print(f"\n###############\nAOC 2023 DAY {DAY} P1 SAMPLE SOLUTION\n###############")
        print(P1_SAMPLE_SOLUTION)
        print(f"\n###############\nAOC 2023 DAY {DAY} P2 SAMPLE SOLUTION\n###############")
        print(P2_SAMPLE_SOLUTION)
    

    if P1_SAMPLE_SOLUTION:            
        print("PART 1\nTesting Sample...\n")
        start_time = time()
        sample = Puzzle(input_text=SAMPLE_INPUT)
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