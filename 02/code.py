import argparse
from time import time
import json
import math

DAY = 2

PUZZLE_TEXT = '''
--- Day 2: Cube Conundrum ---

You're launched high into the atmosphere! The apex of your trajectory just barely reaches the surface of a large island floating in the sky. You gently land in a fluffy pile of leaves. It's quite cold, but you don't see much snow. An Elf runs over to greet you.

The Elf explains that you've arrived at Snow Island and apologizes for the lack of snow. He'll be happy to explain the situation, but it's a bit of a walk, so you have some time. They don't get many visitors up here; would you like to play a game in the meantime?

As you walk, the Elf shows you a small bag and some cubes which are either red, green, or blue. Each time you play this game, he will hide a secret number of cubes of each color in the bag, and your goal is to figure out information about the number of cubes.

To get information, once a bag has been loaded with cubes, the Elf will reach into the bag, grab a handful of random cubes, show them to you, and then put them back in the bag. He'll do this a few times per game.

You play several games and record the information from each game (your puzzle input). Each game is listed with its ID number (like the 11 in Game 11: ...) followed by a semicolon-separated list of subsets of cubes that were revealed from the bag (like 3 red, 5 green, 4 blue).

For example, the record of a few games might look like this:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, three sets of cubes are revealed from the bag (and then put back again). The first set is 3 blue cubes and 4 red cubes; the second set is 1 red cube, 2 green cubes, and 6 blue cubes; the third set is only 2 green cubes.

The Elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?

In the example above, games 1, 2, and 5 would have been possible if the bag had been loaded with that configuration. However, game 3 would have been impossible because at one point the Elf showed you 20 red cubes at once; similarly, game 4 would also have been impossible because the Elf showed you 15 blue cubes at once. If you add up the IDs of the games that would have been possible, you get 8.

Determine which games would have been possible if the bag had been loaded with only 12 red cubes, 13 green cubes, and 14 blue cubes. What is the sum of the IDs of those games?

--- Part Two ---

The Elf says they've stopped producing snow because they aren't getting any water! He isn't sure why the water stopped; however, he can show you how to get to the water source to check it out for yourself. It's just up ahead!

As you continue your walk, the Elf poses a second question: in each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the game possible?

Again consider the example games from earlier:

Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
In game 1, the game could have been played with as few as 4 red, 2 green, and 6 blue cubes. If any color had even one fewer cube, the game would have been impossible.
Game 2 could have been played with a minimum of 1 red, 3 green, and 4 blue cubes.
Game 3 must have been played with at least 20 red, 13 green, and 6 blue cubes.
Game 4 required at least 14 red, 3 green, and 15 blue cubes.
Game 5 needed no fewer than 6 red, 3 green, and 2 blue cubes in the bag.
The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together. The power of the minimum set of cubes in game 1 is 48. In games 2-5 it was 12, 1560, 630, and 36, respectively. Adding up these five powers produces the sum 2286.

For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?
'''

P1_SAMPLE_INPUT = '''
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''

P2_SAMPLE_INPUT = '''
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
'''

PUZZLE_INPUT = '''
Game 1: 19 blue, 12 red; 19 blue, 2 green, 1 red; 13 red, 11 blue
Game 2: 1 green, 1 blue, 1 red; 11 red, 3 blue; 1 blue, 18 red; 9 red, 1 green; 2 blue, 11 red, 1 green; 1 green, 2 blue, 10 red
Game 3: 3 blue, 2 red, 6 green; 4 blue, 6 green, 1 red; 11 green, 12 blue; 2 red, 6 green, 4 blue; 4 green
Game 4: 10 red, 5 green, 5 blue; 3 red, 3 blue, 6 green; 2 blue, 9 red, 6 green; 8 green, 10 red, 4 blue; 9 red, 2 green, 3 blue; 1 blue, 5 red, 15 green
Game 5: 11 green, 7 blue; 5 green, 5 red, 1 blue; 1 green, 1 red, 4 blue; 1 red, 1 blue, 4 green; 4 blue, 1 red, 10 green; 5 red, 6 green
Game 6: 1 green, 1 red, 11 blue; 1 blue, 2 green; 1 red, 5 green, 9 blue; 7 blue; 1 red, 2 green, 9 blue; 12 blue, 1 red, 2 green
Game 7: 1 blue, 10 red, 7 green; 14 blue, 10 green; 12 red, 2 green; 16 red, 13 blue, 1 green; 12 green, 10 red, 3 blue; 9 red, 19 blue, 11 green
Game 8: 3 blue, 1 green, 3 red; 4 blue, 10 red, 6 green; 1 green, 10 red, 9 blue; 9 blue, 7 red, 8 green; 8 green, 12 red, 8 blue; 6 blue, 1 green, 13 red
Game 9: 10 green, 2 blue, 11 red; 2 green, 2 red; 6 blue, 8 red, 13 green
Game 10: 8 red, 3 blue, 5 green; 5 green, 7 blue, 1 red; 3 red, 10 blue, 6 green; 2 red, 6 green, 7 blue; 3 blue, 11 red, 4 green; 8 red, 8 blue, 4 green
Game 11: 14 green, 9 red; 3 blue, 6 green, 8 red; 14 green
Game 12: 10 red, 5 blue, 1 green; 4 blue, 8 red; 5 blue, 1 green, 6 red; 14 red, 4 blue; 1 green, 11 red, 3 blue
Game 13: 1 blue, 16 green, 1 red; 6 red, 2 blue, 5 green; 2 blue, 12 red, 10 green; 3 red, 4 blue, 13 green; 14 red, 4 blue, 12 green; 7 red, 2 green
Game 14: 17 red, 11 blue, 3 green; 16 red, 3 blue, 8 green; 3 green, 9 red, 13 blue; 4 green, 15 red, 14 blue
Game 15: 7 blue, 2 red, 2 green; 1 green, 5 red, 6 blue; 3 green, 6 red, 2 blue
Game 16: 3 red, 3 green; 6 green, 4 red, 3 blue; 3 red, 4 blue; 4 blue, 2 red, 4 green
Game 17: 6 red, 1 blue, 5 green; 3 red, 1 green, 12 blue; 13 green, 1 blue; 5 blue, 7 green, 6 red; 5 blue, 14 green, 2 red; 4 green, 6 red, 10 blue
Game 18: 4 red, 8 blue; 8 blue, 4 red; 12 blue, 1 green
Game 19: 1 blue, 15 green, 9 red; 1 red, 3 green; 4 blue, 2 green, 1 red
Game 20: 7 blue, 4 green, 12 red; 1 red, 9 green, 8 blue; 4 blue, 2 green; 13 green, 8 blue; 3 red, 4 green, 1 blue; 6 green, 7 red, 3 blue
Game 21: 9 green, 4 blue, 8 red; 5 blue; 7 red, 8 blue, 1 green
Game 22: 3 green, 4 red; 6 red, 3 green; 4 red, 1 blue, 1 green; 11 red, 3 green, 1 blue; 7 red, 1 blue
Game 23: 3 blue, 4 green; 3 green, 1 red; 1 red, 2 blue, 4 green
Game 24: 2 blue, 3 green; 9 red, 4 green; 2 blue, 9 red; 2 green, 10 red, 1 blue; 1 blue, 1 red, 5 green
Game 25: 8 green, 4 blue; 9 blue, 7 red; 5 green, 15 blue, 11 red; 11 green, 14 red, 10 blue
Game 26: 3 blue; 2 red, 1 green; 2 red, 3 blue; 10 blue, 1 red, 3 green; 1 green, 2 red; 1 green, 6 blue
Game 27: 1 green, 6 blue; 2 green, 1 red, 6 blue; 1 red, 2 blue, 1 green
Game 28: 8 blue, 1 red, 5 green; 1 red; 3 green, 4 red, 2 blue; 4 green, 2 red, 4 blue; 5 blue, 3 red, 7 green
Game 29: 2 green, 4 blue; 7 blue, 4 red, 10 green; 7 blue, 9 green; 14 green, 7 red, 5 blue
Game 30: 19 green, 3 red; 19 green; 1 blue, 14 green; 2 blue, 5 green; 3 red, 19 green
Game 31: 3 red, 1 green, 4 blue; 10 blue; 3 red, 4 green, 5 blue; 10 blue, 1 red, 6 green
Game 32: 19 red, 1 green, 2 blue; 1 blue, 6 green, 13 red; 10 green, 9 red; 11 red, 2 blue, 6 green; 8 green, 5 red
Game 33: 2 red, 8 blue, 2 green; 1 red, 3 green; 9 red, 9 blue, 1 green; 6 red, 1 green; 9 blue, 1 green, 8 red; 5 green, 10 red, 8 blue
Game 34: 1 red, 6 blue, 2 green; 7 red; 14 red, 13 blue; 13 red, 12 blue; 1 green, 9 red, 13 blue; 2 green, 15 blue
Game 35: 8 blue, 2 red, 3 green; 2 green, 2 red; 3 red, 6 blue, 2 green; 2 green, 6 blue; 1 green, 5 blue, 4 red; 3 green, 6 blue
Game 36: 3 red, 5 blue, 10 green; 1 red, 1 green, 7 blue; 2 blue, 2 green, 1 red
Game 37: 8 red, 7 green; 5 green, 1 blue, 6 red; 7 red, 6 blue, 11 green
Game 38: 4 green, 10 red, 9 blue; 12 green, 2 blue, 2 red; 6 red, 6 blue, 9 green; 1 blue, 1 green, 6 red; 3 blue, 1 red, 5 green; 5 blue, 2 red, 12 green
Game 39: 1 blue, 2 red; 7 blue, 2 green, 1 red; 7 blue, 11 green, 3 red; 8 blue, 13 green, 1 red; 6 green, 6 blue, 3 red
Game 40: 8 green, 5 blue; 5 green, 1 blue, 10 red; 9 green, 3 blue; 3 green, 7 red; 2 green, 3 blue, 5 red
Game 41: 7 green, 8 red; 3 blue, 15 green, 7 red; 2 red, 2 green, 4 blue; 10 green, 4 red, 5 blue; 3 red, 8 blue, 9 green; 7 red, 8 green
Game 42: 6 blue, 12 green; 3 red, 1 green; 1 red, 12 green, 3 blue; 10 red, 9 green; 9 red, 4 green, 5 blue
Game 43: 11 red, 6 green; 2 blue, 11 red; 3 red, 1 blue; 3 green, 11 red, 2 blue; 4 red, 5 green, 1 blue; 8 green, 2 blue, 17 red
Game 44: 2 green, 9 blue, 3 red; 7 blue, 1 green, 4 red; 1 green
Game 45: 1 green, 10 red; 5 red, 10 green, 1 blue; 11 red, 3 green, 2 blue; 2 blue, 3 green, 4 red; 7 green, 3 red, 2 blue; 1 blue, 10 red
Game 46: 1 green, 4 blue, 7 red; 13 blue, 2 green, 9 red; 7 blue, 3 red, 1 green
Game 47: 4 blue; 2 green, 2 red, 1 blue; 1 green, 1 red, 4 blue; 1 green, 2 red, 2 blue; 2 blue, 2 red
Game 48: 5 green, 10 red; 7 red, 5 green; 1 green, 11 red; 12 red, 11 green; 11 red, 1 blue, 1 green
Game 49: 2 green, 1 red, 1 blue; 1 blue, 2 red; 2 green, 1 red, 2 blue; 1 blue, 1 red, 1 green
Game 50: 5 green, 2 blue; 4 green, 4 blue, 3 red; 1 red, 7 green, 3 blue
Game 51: 9 green, 1 red, 2 blue; 7 red, 3 blue, 6 green; 5 green, 4 blue, 5 red
Game 52: 2 green, 4 blue, 1 red; 2 blue, 2 red, 13 green; 8 blue, 3 green; 3 green, 4 blue, 2 red; 2 green
Game 53: 3 red; 4 blue, 4 red; 2 blue, 2 red; 6 blue, 1 red, 2 green; 1 red, 1 green, 6 blue; 2 blue, 4 red
Game 54: 3 blue, 3 green, 18 red; 4 blue, 18 red, 3 green; 7 blue, 4 green
Game 55: 1 green, 2 red, 3 blue; 1 red, 4 blue, 1 green; 3 blue, 2 red; 2 blue, 1 green; 3 blue, 2 red; 1 blue, 1 green, 1 red
Game 56: 12 green, 2 red, 1 blue; 11 green, 16 red, 13 blue; 7 red, 5 blue, 12 green; 4 blue, 16 red; 5 red, 1 blue, 3 green
Game 57: 5 green, 17 blue, 11 red; 6 blue, 1 green; 1 green, 5 blue, 8 red; 9 green, 11 red, 1 blue; 9 green, 11 blue, 7 red; 8 green, 4 blue
Game 58: 5 red, 10 blue, 6 green; 5 green, 11 blue, 5 red; 9 green; 4 red, 2 green
Game 59: 2 red, 6 blue, 1 green; 1 green, 12 blue; 2 red
Game 60: 6 blue, 10 green, 9 red; 8 red, 19 blue, 2 green; 16 red, 10 green, 12 blue; 13 red, 12 blue, 6 green
Game 61: 12 green, 1 red, 3 blue; 3 red, 4 blue, 19 green; 1 blue, 7 green
Game 62: 7 red, 6 blue, 8 green; 10 blue, 3 green, 17 red; 13 blue, 3 red, 10 green; 13 red, 5 blue, 9 green; 12 blue, 4 red; 10 red, 4 green
Game 63: 19 green, 4 red; 5 blue, 4 red, 1 green; 4 red, 2 blue, 15 green; 5 green, 4 red, 5 blue
Game 64: 6 red, 3 green; 6 green, 3 red, 3 blue; 3 blue, 8 red, 5 green; 3 blue, 7 red, 1 green; 1 blue, 6 red, 6 green
Game 65: 1 green, 9 blue; 6 blue, 4 green, 6 red; 6 blue, 5 green; 3 red, 1 blue, 4 green
Game 66: 1 blue, 2 red; 2 green, 1 blue; 2 red, 1 blue, 1 green; 1 blue, 1 green
Game 67: 16 blue, 1 green; 1 blue, 2 green, 2 red; 1 red, 9 blue; 12 blue, 4 green, 1 red; 6 green, 11 blue, 3 red
Game 68: 6 blue, 2 red, 1 green; 2 blue, 2 green; 1 green, 7 red, 15 blue; 14 blue, 12 green, 3 red; 13 green, 10 red, 6 blue; 2 green, 5 blue, 1 red
Game 69: 2 red, 1 blue, 2 green; 1 blue, 7 green, 1 red; 3 blue, 1 red, 7 green; 2 red, 1 blue, 11 green
Game 70: 2 green, 9 red, 3 blue; 12 blue, 1 green, 13 red; 6 red, 1 green, 5 blue; 1 red, 17 blue
Game 71: 7 red, 5 green, 6 blue; 5 blue, 5 green; 7 green, 4 blue; 2 green, 4 blue, 8 red; 10 red, 8 green; 3 blue, 13 red, 7 green
Game 72: 13 red, 17 green; 9 red, 20 green, 3 blue; 1 green, 3 blue, 8 red
Game 73: 1 blue, 7 red, 2 green; 2 green, 1 blue, 8 red; 1 blue, 2 red; 4 red, 7 green; 4 red, 5 green; 3 green, 7 red
Game 74: 2 green, 14 blue; 1 red, 1 blue, 7 green; 1 red, 8 green, 11 blue; 4 green, 12 blue; 1 green, 5 blue
Game 75: 12 blue, 1 red; 1 red, 7 blue, 4 green; 4 blue, 6 green; 4 green, 3 blue, 1 red
Game 76: 7 green, 5 red, 6 blue; 18 red, 1 green; 14 green, 4 red, 15 blue; 4 blue, 6 red
Game 77: 2 blue, 2 green, 2 red; 2 blue, 1 red, 1 green; 2 green, 1 red; 6 blue, 4 green; 1 red, 1 blue, 6 green
Game 78: 5 red, 16 blue, 12 green; 11 blue, 3 red, 2 green; 13 blue, 4 red
Game 79: 9 red, 11 green, 6 blue; 1 red, 3 green; 7 blue, 7 red, 11 green; 8 red, 9 blue, 11 green; 7 red, 11 green, 4 blue
Game 80: 7 green, 5 red, 2 blue; 1 blue, 7 green, 1 red; 2 red, 2 blue; 1 red, 4 blue, 12 green; 4 green, 2 blue
Game 81: 5 blue, 2 green, 12 red; 2 green, 1 blue, 5 red; 3 blue, 13 red, 3 green; 3 green, 9 blue, 3 red; 10 blue, 4 red, 3 green
Game 82: 11 blue, 1 red, 9 green; 11 green, 1 blue, 12 red; 13 red, 6 blue, 19 green
Game 83: 6 red, 5 blue, 16 green; 4 green, 17 blue, 9 red; 15 red, 2 green, 9 blue
Game 84: 19 green, 11 blue, 3 red; 1 blue, 18 green, 6 red; 17 blue, 5 green, 4 red; 18 blue, 7 green, 3 red
Game 85: 3 green, 15 blue; 12 blue; 2 green, 1 red; 1 red, 9 blue, 1 green; 12 blue, 3 red, 1 green
Game 86: 3 green, 4 blue, 5 red; 9 red, 4 green, 1 blue; 6 green, 1 blue, 8 red; 3 green, 2 blue, 5 red
Game 87: 2 red, 8 blue, 5 green; 3 red, 5 blue, 10 green; 2 red, 3 green
Game 88: 16 green, 13 red; 7 green, 1 blue, 2 red; 7 red, 12 green; 5 red, 7 green, 2 blue; 2 blue, 10 green, 7 red; 8 red, 16 green
Game 89: 1 blue, 8 red; 2 green, 10 red, 12 blue; 13 green, 14 blue; 10 blue, 15 red, 13 green; 2 green, 5 red, 13 blue
Game 90: 16 blue, 7 red, 4 green; 4 green, 6 red, 11 blue; 2 red, 8 blue, 2 green; 5 green, 8 red, 10 blue; 4 red, 2 green, 7 blue; 4 green, 5 blue, 5 red
Game 91: 4 red, 4 green, 1 blue; 3 blue, 2 green; 6 blue, 4 green, 5 red; 2 red, 6 blue, 4 green; 6 blue, 1 green
Game 92: 1 red, 3 green; 3 blue, 6 green; 5 blue, 1 red, 11 green; 1 red; 3 green, 13 blue
Game 93: 1 red, 14 blue, 6 green; 10 blue, 6 red; 9 green, 15 red, 17 blue; 9 red, 1 green, 9 blue
Game 94: 3 red, 14 green; 3 blue, 15 green, 3 red; 2 red, 15 green
Game 95: 4 blue, 13 red; 5 blue, 1 green, 11 red; 3 green, 3 blue, 10 red; 13 red, 6 blue; 2 green, 5 blue; 3 green, 11 red
Game 96: 7 blue, 1 green; 1 green, 4 blue; 1 green, 2 red, 5 blue; 1 red, 2 blue, 1 green; 1 blue
Game 97: 15 green, 9 blue; 14 blue, 14 red, 2 green; 18 red, 12 blue, 2 green
Game 98: 1 green, 9 red; 1 red, 2 green, 7 blue; 8 red, 1 blue; 6 red, 2 green; 1 green, 6 blue
Game 99: 1 green, 2 red, 6 blue; 6 red, 1 green, 5 blue; 11 blue, 6 red; 11 red, 1 green; 1 green, 11 red, 9 blue
Game 100: 12 green, 8 blue, 2 red; 7 blue, 14 red, 8 green; 14 red, 1 blue, 4 green
'''

P1_SAMPLE_SOLUTION = 8

P2_SAMPLE_SOLUTION = 2286

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

class Puzzle():
    def __init__(self,input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split('\n')
        self.strings = {
            'one': '1',
            'two': '2',
            'three': '3',
            'four': '4',
            'five': '5',
            'six': '6',
            'seven': '7',
            'eight': '8',
            'nine': '9'
        }
                
    def p1(self):
        self.p1_solution = 0
        max_red = 12
        max_blue = 14
        max_green = 13

        for line in self.input_list:
            this_line = line.split(': ')
            this_game_number = int(this_line[0][5:])
            this_games = this_line[1].split('; ') 
            bad_game = False
            for game in this_games:
                pulls = game.split(', ')
                for pull in pulls:
                    pull = pull.split()
                    if pull[1] == "red" and int(pull[0]) > max_red:
                        bad_game = True
                        break
                    elif pull[1] == "blue" and int(pull[0]) > max_blue:
                        bad_game = True
                        break
                    elif pull[1] == "green" and int(pull[0]) > max_green:
                        bad_game = True
                        break
            if bad_game == False:
                self.p1_solution += this_game_number
        return True

    def p2(self):
        self.p2_solution = 0

        for line in self.input_list:

            max_red = 0
            max_blue = 0
            max_green = 0
            this_line = line.split(': ')
            this_games = this_line[1].split('; ') 
            for game in this_games:
                pulls = game.split(', ')
                for pull in pulls:
                    pull = pull.split()
                    if pull[1] == "red" and int(pull[0]) > max_red:
                        max_red = int(pull[0])
                    elif pull[1] == "blue" and int(pull[0]) > max_blue:
                        max_blue = int(pull[0])
                    elif pull[1] == "green" and int(pull[0]) > max_green:
                        max_green = int(pull[0])
            self.p2_solution += ( max_blue * max_red * max_green )

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
        print(f"###############\nAOC 2023 DAY {DAY} P1 SAMPLE INPUT\n###############")
        print(P1_SAMPLE_INPUT.strip())
        print(f"###############\nAOC 2023 DAY {DAY} P2 SAMPLE INPUT\n###############")
        print(P2_SAMPLE_INPUT.strip())
        print(f"\n###############\nAOC 2023 DAY {DAY} P1 SAMPLE SOLUTION\n###############")
        print(P1_SAMPLE_SOLUTION)
        print(f"\n###############\nAOC 2023 DAY {DAY} P2 SAMPLE SOLUTION\n###############")
        print(P2_SAMPLE_SOLUTION)
    

    if P1_SAMPLE_SOLUTION:            
        print("PART 1\nTesting Sample...\n")
        start_time = time()
        sample = Puzzle(input_text=P1_SAMPLE_INPUT)
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
        sample = Puzzle(input_text=P2_SAMPLE_INPUT)
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