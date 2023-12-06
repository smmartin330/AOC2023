import argparse
from time import time
import re

DAY = 5

PUZZLE_TEXT = '''
--- Day 5: If You Give A Seed A Fertilizer ---

You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48
The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.
The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?

--- Part Two ---

Everyone will starve if you only plant such a small number of seeds. Re-reading the almanac, it looks like the seeds: line actually describes ranges of seed numbers.

The values on the initial seeds: line come in pairs. Within each pair, the first value is the start of the range and the second value is the length of the range. So, in the first line of the example above:

seeds: 79 14 55 13
This line describes two ranges of seed numbers to be planted in the garden. The first range starts with seed number 79 and contains 14 values: 79, 80, ..., 91, 92. The second range starts with seed number 55 and contains 13 values: 55, 56, ..., 66, 67.

Now, rather than considering four seed numbers, you need to consider a total of 27 seed numbers.

In the above example, the lowest location number can be obtained from seed number 82, which corresponds to soil 84, fertilizer 84, water 84, light 77, temperature 45, humidity 46, and location 46. So, the lowest location number is 46.

Consider all of the initial seed numbers listed in the ranges on the first line of the almanac. What is the lowest location number that corresponds to any of the initial seed numbers?


'''

SAMPLE_INPUT = '''
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''

PUZZLE_INPUT = '''
seeds: 2276375722 160148132 3424292843 82110297 1692203766 342813967 3289792522 103516087 2590548294 590357761 1365412380 80084180 3574751516 584781136 4207087048 36194356 1515742281 174009980 6434225 291842774

seed-to-soil map:
4170452318 3837406401 124514978
2212408060 1593776674 105988696
3837406401 4016132523 278834773
1475766470 1699765370 492158296
3698488336 1475766470 118010204
2318396756 2191923666 46351359
4116241174 3961921379 54211144
2193579298 3791037069 18828762
2364748115 2578360543 354997036
3085506703 3439828590 106510622
1967924766 3546339212 219021823
2719745151 3765361035 25676034
2745421185 2238275025 340085518
2186946589 3809865831 6632709
3192017325 2933357579 506471011

soil-to-fertilizer map:
2067774073 3521970321 52706909
3338663639 285713733 377282283
4175452431 2125409520 119514865
3950920796 1900877885 224531635
285713733 3604616580 690350716
976064449 3368036703 153933618
2120480982 662996016 210956413
2763248642 1355402238 545475647
3715945922 873952429 49638562
3765584484 3182700391 185336312
2331437395 923590991 431811247
1129998067 2244924385 937776006
3308724289 3574677230 29939350

fertilizer-to-water map:
1898912715 0 159034880
0 781591504 125461131
4234890433 2427770485 8749678
176481534 1845116986 384152450
822014814 539693831 241897673
125461131 907052635 47763268
1476125220 244008638 19613711
3828547378 4170474998 124492298
2643114268 2457193301 126243103
173224399 2229269436 3257135
2916187764 3376015556 236473226
764735505 186729329 57279309
2427770485 3802085897 160735547
2895514626 2436520163 20673138
3152660990 2671736916 584987016
1495738931 1131222975 403173784
1339983969 1534396759 136141251
2588506032 3612488782 54608236
3737648006 2583436404 88300512
737041056 159034880 27694449
2057947595 1677521625 167595361
1063912487 263622349 276071482
3953039676 4041226796 129248202
2225542956 1670538010 6983615
560633984 954815903 176407072
2847762723 3328263653 47751903
2769357371 3962821444 78405352
3825948518 3256723932 2598860
4082287878 3667097018 134988879
4243640111 3276936468 51327185
4217276757 3259322792 17613676

water-to-light map:
527906959 2908176499 284796856
1306013866 0 139756297
500839409 1466481782 27067550
1269694476 139756297 36319390
0 778456518 2402633
4218077327 4154765934 76889969
812703815 4004150799 56130996
153843304 3657154694 8975056
2402633 905946004 132694584
3795108796 2776082693 132093806
3927202602 1422228955 44252827
1445770163 1493549332 1282533361
3794865694 780859151 243102
2728303524 176075687 602380831
162818360 3666129750 338021049
3330684355 3319846298 337308396
4154765934 4231655903 63311393
135097217 887199917 18746087
3667992751 3192973355 126872943
3971455429 781102253 88826366
1252423178 869928619 17271298
868834811 1038640588 383588367

light-to-temperature map:
2621973104 3678827401 230150807
1333642604 1531317439 615453278
3364444750 2854318675 314483239
2978187907 3908978208 107198609
1117308885 1110453605 216333719
1951157390 4016176817 152726483
4168382203 2717095112 26843204
0 312822387 5553076
287414983 245463475 67358912
1949095882 2597527252 2061508
3836867339 1522015715 9301724
648138229 2599588760 117506352
4132690450 1486323962 35691753
2852123911 4168903300 126063996
2468610361 3525464658 153362743
526108840 988424216 122029389
5553076 0 148736111
3265904462 1326787324 98540288
4195225407 716774234 17303853
181751976 318375463 105663007
843084177 3275513023 249951635
2214264232 734078087 254346129
154289187 218000686 27462789
3146382866 684048190 32726044
765644581 2433292104 77439596
3179108910 2510731700 86795552
3846169063 2146770717 286521387
2103883873 2743938316 110380359
3085386516 1425327612 60996350
3678927989 526108840 157939350
4212529260 3193074987 82438036
354773895 148736111 69264575
1093035812 3168801914 24273073

temperature-to-humidity map:
1008510114 1939290935 27755995
2205283444 4197517502 16218189
1119061522 3123774174 108864966
1566495924 221087407 33939034
3089618547 3728555042 25452278
2341294643 3455988869 16076350
2286651827 3754007320 54642816
704748216 2542375745 76754089
445299830 3938069116 259448386
1036266109 1300576315 82795413
178337856 1565003866 40230920
2122934367 1605234786 81339593
1484902828 980285858 81593096
2823460240 1967046930 266158307
3827446421 1526750766 38253100
984919715 1161567987 23590399
218568776 1061878954 99689033
4049237602 3232639140 223349729
953670836 2233205237 3881060
318257809 3472065219 89705062
1727156113 3113814046 9960128
3733360236 444372828 94086185
4272587331 3688491436 22379965
910921285 178337856 42749551
781502305 3808650136 129418980
957551896 2798966448 27367819
1870217811 1686574379 252716556
407962871 2998327877 37336959
2508087592 2826334267 171993610
1600434958 3561770281 126721155
3865699521 812829188 167456670
1737116241 1185158386 115417929
1852534170 3710871401 17683641
3420360273 255026441 38629788
1227926488 2620139318 178827130
4033156191 4250190027 16081411
2204273960 2619129834 1009484
2250197491 4213735691 36454336
2680081202 1383371728 143379038
3458990061 538459013 274370175
3115070825 2237086297 305289448
2357370993 293656229 150716599
1406753618 3035664836 78149210
2221501633 4266271438 28695858

humidity-to-location map:
2849843584 4147982382 56632112
3849085050 3618212322 355529444
1632881348 407047779 65646492
3056274757 2246063521 686771203
2729873863 4028012661 26534599
3779070915 1543896540 70014135
2571854216 2932834724 91402738
2192942437 1028113266 378911779
2960746591 932585100 95528166
765942740 0 407047779
2663256954 1441254676 66616909
2756408462 4054547260 93435122
1698527840 1407025045 34229631
0 3024237462 156854744
3743045960 1507871585 36024955
156854744 3181092206 437120116
1172990519 472694271 459890829
2906475696 3973741766 54270895
593974860 2074095641 171967880
1732757471 1613910675 460184966
'''

P1_SAMPLE_SOLUTION = 35

P2_SAMPLE_SOLUTION = 46

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

def map_seeds(seed,source_start,dest_start,range_length):
    if seed in range(source_start,source_start+range_length):
        new_seed = dest_start + (seed - source_start)

        return new_seed
    return seed
    


class Puzzle():
    def __init__(self,input_text):
        self.input_text = input_text
        self.input_groups = input_text.strip().split('\n\n')

        
                                    
    def p1(self):
        self.seeds = []
        new_seeds = []
        for group in self.input_groups:
            this_group = group.split('\n')
            this_group = [line for line in this_group if ':' not in line]
            which = re.match(r"^(?P<heading>.*):",group)
            match which.group('heading'):
                case "seeds":
                    self.seeds = list(map(int,group[7:].split()))
                case _:
                    print(which.group('heading'))                    
                    for line in this_group:
                        unchanged_seeds = []
                        line = line.split()
                        dest_start, source_start, range_length = int(line[0]), int(line[1]), int(line[2])
                        source_end = source_start + range_length
                        while len(self.seeds) > 0:
                            old_seed = self.seeds.pop()
                            if old_seed in range(source_start,source_end):
                                new_seed = dest_start + (old_seed - source_start)
                                new_seeds.append(new_seed)
                            else:
                                unchanged_seeds.append(old_seed)
                        self.seeds = unchanged_seeds
                    self.seeds += new_seeds
                    new_seeds = []
        self.p1_solution = min(self.seeds)
        return True

    def p2(self):
        self.seeds = set()
        new_seeds = []
        for group in self.input_groups:
            this_group = group.split('\n')
            this_group = [line for line in this_group if ':' not in line]
            which = re.match(r"^(?P<heading>.*):",group)
            match which.group('heading'):
                case "seeds":
                    i=0
                    self.seed_ranges = list(map(int,group[7:].split()))
                    # how many pairs?
                    pair_count = len(self.seed_ranges) // 2
                    print(f' there are {pair_count} pairs.')
                    for i in range(0,pair_count):
                        print(f' for pair {i+1}, the seed is at {i*2} and the range length is at {(i*2)+1}.')
                        start = self.seed_ranges[2*i]
                        range_len = self.seed_ranges[(2*i)+1]
                        for x in range(start,start+range_len):
                            self.seeds.add(x)
                    
                case _:
                    print(which.group('heading'))                    
                    for line in this_group:
                        unchanged_seeds = []
                        line = line.split()
                        dest_start, source_start, range_length = int(line[0]), int(line[1]), int(line[2])
                        source_end = source_start + range_length
                        while len(self.seeds) > 0:
                            old_seed = self.seeds.pop()
                            if old_seed in range(source_start,source_end):
                                new_seed = dest_start + (old_seed - source_start)
                                new_seeds.append(new_seed)
                            else:
                                unchanged_seeds.append(old_seed)
                        self.seeds = unchanged_seeds
                    self.seeds += new_seeds
                    new_seeds = []
        self.p2_solution = min(self.seeds)
        return True

def main():
    parser = argparse.ArgumentParser(description=f'AOC2023 Puzzle Day { DAY }')
    parser.add_argument("-p", "--showpuzzle", help="Display Puzzle Text", action='store_true')
    parser.add_argument("-s", "--showsample", help="Display Sample Input", action='store_true')
    args = parser.parse_args()
    
    if args.showpuzzle:
        print(f"###############\nAOC 2023 DAY {DAY} PUZZLE TEXT\n###############")
        print(PUZZLE_TEXT)
    
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