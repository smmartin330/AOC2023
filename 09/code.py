import argparse
from time import time
import collections

DAY = 9

PUZZLE_TEXT = '''
--- Day 9: Mirage Maintenance ---

You ride the camel through the sandstorm and stop where the ghost's maps told you to stop. The sandstorm subsequently subsides, somehow seeing you standing at an oasis!

The camel goes to get some water and you stretch your neck. As you look up, you discover what must be yet another giant floating island, this one made of metal! That must be where the parts to fix the sand machines come from.

There's even a hang glider partially buried in the sand here; once the sun rises and heats up the sand, you might be able to use the glider and the hot air to get all the way up to the metal island!

While you wait for the sun to rise, you admire the oasis hidden here in the middle of Desert Island. It must have a delicate ecosystem; you might as well take some ecological readings while you wait. Maybe you can report any environmental instabilities you find to someone so the oasis can be around for the next sandstorm-worn traveler.

You pull out your handy Oasis And Sand Instability Sensor and analyze your surroundings. The OASIS produces a report of many values and how they are changing over time (your puzzle input). Each line in the report contains the history of a single value. For example:

0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
To best protect the oasis, your environmental report should include a prediction of the next value in each history. To do this, start by making a new sequence from the difference at each step of your history. If that sequence is not all zeroes, repeat this process, using the sequence you just generated as the input sequence. Once all of the values in your latest sequence are zeroes, you can extrapolate what the next value of the original history should be.

In the above dataset, the first history is 0 3 6 9 12 15. Because the values increase by 3 each step, the first sequence of differences that you generate will be 3 3 3 3 3. Note that this sequence has one fewer value than the input sequence because at each step it considers two numbers from the input. Since these values aren't all zero, repeat the process: the values differ by 0 at each step, so the next sequence is 0 0 0 0. This means you have enough information to extrapolate the history! Visually, these sequences can be arranged like this:

0   3   6   9  12  15
  3   3   3   3   3
    0   0   0   0
To extrapolate, start by adding a new zero to the end of your list of zeroes; because the zeroes represent differences between the two values above them, this also means there is now a placeholder in every sequence above it:

0   3   6   9  12  15   B
  3   3   3   3   3   A
    0   0   0   0   0
You can then start filling in placeholders from the bottom up. A needs to be the result of increasing 3 (the value to its left) by 0 (the value below it); this means A must be 3:

0   3   6   9  12  15   B
  3   3   3   3   3   3
    0   0   0   0   0
Finally, you can fill in B, which needs to be the result of increasing 15 (the value to its left) by 3 (the value below it), or 18:

0   3   6   9  12  15  18
  3   3   3   3   3   3
    0   0   0   0   0
So, the next value of the first history is 18.

Finding all-zero differences for the second history requires an additional sequence:

1   3   6  10  15  21
  2   3   4   5   6
    1   1   1   1
      0   0   0
Then, following the same process as before, work out the next value in each sequence from the bottom up:

1   3   6  10  15  21  28
  2   3   4   5   6   7
    1   1   1   1   1
      0   0   0   0
So, the next value of the second history is 28.

The third history requires even more sequences, but its next value can be found the same way:

10  13  16  21  30  45  68
   3   3   5   9  15  23
     0   2   4   6   8
       2   2   2   2
         0   0   0
So, the next value of the third history is 68.

If you find the next value for each history in this example and add them together, you get 114.

Analyze your OASIS report and extrapolate the next value for each history. What is the sum of these extrapolated values?

--- Part Two ---

Of course, it would be nice to have even more history included in your report. Surely it's safe to just extrapolate backwards as well, right?

For each history, repeat the process of finding differences until the sequence of differences is entirely zero. Then, rather than adding a zero to the end and filling in the next values of each previous sequence, you should instead add a zero to the beginning of your sequence of zeroes, then fill in new first values for each previous sequence.

In particular, here is what the third example history looks like when extrapolating back in time:

5  10  13  16  21  30  45
  5   3   3   5   9  15
   -2   0   2   4   6
      2   2   2   2
        0   0   0
Adding the new values on the left side of each sequence from bottom to top eventually reveals the new left-most history value: 5.

Doing this for the remaining example data above results in previous values of -3 for the first history and 0 for the second history. Adding all three new values together produces 2.

Analyze your OASIS report again, this time extrapolating the previous value for each history. What is the sum of these extrapolated values?



'''

SAMPLE_INPUT = '''
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''

PUZZLE_INPUT = '''
0 7 18 31 55 131 378 1093 2953 7398 17321 38257 80352 161507 312219 582730 1053014 1845605 3139788 5182383 8283893
15 27 57 121 247 494 997 2057 4308 9015 18584 37400 73185 139294 259011 474529 866940 1600988 3022302 5859292 11622118
23 37 70 142 281 521 891 1405 2093 3158 5416 11299 26914 66014 157340 357768 775231 1607747 3208430 6191572 11602387
10 26 43 61 80 100 121 143 166 190 215 241 268 296 325 355 386 418 451 485 520
25 50 95 171 295 490 783 1201 1765 2482 3335 4271 5187 5914 6199 5685 3889 178 -6257 -16429 -31585
27 38 57 98 180 337 634 1203 2336 4705 9824 20927 44511 92886 188187 368438 696417 1272256 2250923 3865976 6461254
19 27 38 55 95 203 473 1080 2328 4736 9232 17624 33708 65754 131904 271681 570227 1208648 2566648 5426856 11370615
12 13 16 21 32 71 217 696 2069 5602 13965 32510 71539 150214 303108 590879 1117202 2054955 3685766 6458435 11073498
9 4 1 20 94 275 657 1438 3051 6394 13184 26456 51229 95362 170601 293721 487401 779884 1201343 1772880 2480796
4 14 29 51 85 134 187 210 166 121 560 3169 12569 39852 109328 270806 621414 1344325 2778523 5546750 10792071
3 22 54 103 193 384 795 1639 3275 6282 11560 20463 34969 57892 93141 146031 223651 335294 492954 711895 1011297
11 21 32 49 83 154 294 550 987 1691 2772 4367 6643 9800 14074 19740 27115 36561 48488 63357 81683
9 22 41 84 194 461 1058 2308 4817 9733 19224 37310 71236 133636 245813 442548 778953 1340000 2253491 3707384 5972558
5 13 40 101 218 431 817 1508 2701 4662 7742 12446 19626 30906 49491 81563 138525 240419 420916 734355 1265394
-6 3 20 41 62 81 100 127 178 279 468 797 1334 2165 3396 5155 7594 10891 15252 20913 28142
8 22 58 125 229 371 549 774 1117 1822 3566 8059 19434 47435 114561 271578 630022 1427838 3157194 6804801 14289067
18 29 43 53 45 7 -43 -8 357 1530 4316 9940 20126 37146 63820 103445 159628 235995 335745 461015 612019
16 28 44 75 145 292 576 1103 2074 3879 7288 13868 26938 53798 110905 235631 512131 1126181 2476979 5396320 11562098
12 26 56 116 241 508 1070 2215 4484 8912 17499 34094 66024 127087 243048 461660 870648 1629258 3022150 5548924 10068791
6 16 49 131 296 579 1009 1616 2486 3926 6835 13415 28396 60989 127819 257124 494534 910764 1611565 2750275 4543296
12 18 24 34 57 107 203 369 634 1032 1602 2388 3439 4809 6557 8747 11448 14734 18684 23382 28917
8 12 26 55 104 193 399 946 2377 5869 13800 30760 65362 133571 265067 515807 993107 1905236 3657357 7032801 13529817
4 11 24 46 86 164 307 547 954 1767 3732 8829 21693 52261 120627 266005 563563 1156582 2318471 4572259 8918535
7 12 29 64 123 212 337 504 719 988 1317 1712 2179 2724 3353 4072 4887 5804 6829 7968 9227
19 29 48 92 192 409 869 1832 3824 7893 16101 32436 64423 125833 241036 451720 826905 1477421 2576294 4386796 7300266
2 -4 -16 -26 -8 94 383 1031 2306 4604 8486 14720 24328 38638 59341 88553 128882 183500 256220 351578 474920
5 17 35 70 160 394 958 2208 4770 9671 18540 34034 60942 109079 200396 385173 776495 1619697 3426197 7222570 15001448
15 36 71 131 241 459 906 1808 3555 6797 12630 22993 41539 75544 140053 266779 522955 1050734 2148445 4435983 9186897
-1 9 38 91 177 321 597 1210 2668 6108 13886 30641 65261 134627 270864 535339 1045161 2021911 3878338 7367515 13831325
5 2 -2 -12 -23 6 200 845 2508 6230 13845 28513 55624 104382 190699 342652 610871 1088090 1945040 3494314 6300307
10 18 43 88 159 286 554 1156 2500 5427 11627 24375 49749 98537 189090 351433 633006 1106472 1880099 3111298 5023979
22 38 68 126 234 433 811 1559 3067 6070 11848 22484 41229 73213 127287 221083 394151 739503 1474123 3087351 6637859
4 -2 -7 -9 3 62 248 742 1933 4622 10428 22657 48247 102129 216744 461997 985310 2088658 4370919 8981399 18056439
9 15 25 53 141 381 955 2201 4713 9484 18103 33020 57897 98068 161137 257750 402585 615613 923693 1362575 1979397
22 47 86 155 288 554 1101 2255 4730 10046 21312 44626 91506 183053 357057 680146 1268582 2323769 4192434 7467421 13153956
17 38 75 138 237 382 583 850 1193 1622 2147 2778 3525 4398 5407 6562 7873 9350 11003 12842 14877
26 38 60 112 220 411 716 1192 1977 3398 6168 11749 23049 45799 91272 181527 359172 704846 1367348 2613742 4910018
14 11 10 31 116 339 829 1820 3742 7379 14166 26807 50622 96470 186916 368780 737710 1484471 2978870 5916367 11565216
9 8 12 28 64 137 295 666 1570 3768 8975 20832 46615 100057 205772 405898 769719 1407184 2487414 4263476 7104906
19 41 73 110 158 240 409 793 1724 4044 9736 23097 52753 114913 238370 471882 894705 1631203 2870627 4893336 8104928
9 28 52 81 115 154 198 247 301 360 424 493 567 646 730 819 913 1012 1116 1225 1339
2 0 5 21 52 102 175 275 406 572 777 1025 1320 1666 2067 2527 3050 3640 4301 5037 5852
19 26 42 88 206 470 1000 1987 3744 6816 12232 22098 40957 78727 156599 318005 647505 1300842 2548802 4834740 8838864
1 -1 -3 -5 -7 -9 -11 -13 -15 -17 -19 -21 -23 -25 -27 -29 -31 -33 -35 -37 -39
15 31 72 163 346 680 1240 2132 3567 6088 11136 22302 47892 105913 233394 503263 1054047 2140757 4219856 8087669 15100566
25 50 86 133 191 260 340 431 533 646 770 905 1051 1208 1376 1555 1745 1946 2158 2381 2615
18 37 78 143 236 382 664 1282 2635 5428 10814 20601 37611 66449 115400 201254 361128 679695 1347950 2782587 5855742
-3 11 50 122 246 466 865 1579 2811 4845 8060 12944 20108 30300 44419 63529 88873 121887 164214 217718 284498
27 55 97 166 285 496 887 1639 3105 5957 11478 22150 42845 83275 163110 322688 645079 1300255 2630431 5308874 10624741
15 27 39 51 63 75 87 99 111 123 135 147 159 171 183 195 207 219 231 243 255
6 22 49 87 136 196 267 349 442 546 661 787 924 1072 1231 1401 1582 1774 1977 2191 2416
10 29 65 129 246 467 886 1664 3067 5544 9927 17976 33812 67444 142859 315389 706888 1573692 3433513 7297872 15096042
4 0 2 12 31 59 95 144 241 505 1239 3095 7326 16150 33254 64469 118650 208798 353464 578478 919049
6 29 70 141 273 542 1109 2274 4544 8715 15968 27979 47043 76212 119447 181784 269514 390377 553770 770969 1055365
-4 -8 -20 -44 -84 -144 -228 -340 -484 -664 -884 -1148 -1460 -1824 -2244 -2724 -3268 -3880 -4564 -5324 -6164
28 44 77 147 278 502 865 1445 2417 4231 8015 16411 35277 77191 168736 365586 783270 1658662 3470536 7172300 14636694
9 19 29 39 49 59 69 79 89 99 109 119 129 139 149 159 169 179 189 199 209
6 1 -4 -9 -14 -19 -24 -29 -34 -39 -44 -49 -54 -59 -64 -69 -74 -79 -84 -89 -94
11 36 89 193 391 769 1490 2854 5427 10334 19907 39055 78043 157953 321205 651677 1313283 2624488 5203073 10247281 20077431
14 28 60 131 271 510 867 1352 2006 3017 4985 9496 20354 46205 106060 240785 536786 1174442 2526194 5352561 11186981
9 26 46 79 153 329 724 1553 3229 6614 13601 28330 59500 124432 255762 511895 992629 1861662 3378028 5938877 10136431
-1 14 51 113 199 305 425 552 679 800 911 1011 1103 1195 1301 1442 1647 1954 2411 3077 4023
17 25 44 91 198 426 882 1736 3245 5807 10087 17276 29560 50886 88113 152625 262457 444941 739814 1202641 1908290
9 27 50 78 111 149 192 240 293 351 414 482 555 633 716 804 897 995 1098 1206 1319
-6 1 19 50 94 145 187 190 106 -135 -629 -1502 -2914 -5063 -8189 -12578 -18566 -26543 -36957 -50318 -67202
19 48 100 181 295 444 628 845 1091 1360 1644 1933 2215 2476 2700 2869 2963 2960 2836 2565 2119
12 9 0 -8 2 59 206 502 1024 1869 3156 5028 7654 11231 15986 22178 30100 40081 52488 67728 86250
26 44 78 152 301 568 1007 1693 2745 4386 7109 12111 22323 44629 94255 202839 432376 898068 1804084 3497318 6545373
14 27 54 114 232 443 803 1405 2394 3971 6372 9804 14316 19579 24545 26951 22630 4587 -38206 -122346 -271920
22 28 26 11 -7 18 195 729 1960 4408 8824 16247 28067 46094 72633 110565 163434 235540 332038 459043 623741
24 33 53 102 219 492 1112 2466 5282 10839 21255 39866 71709 124122 207474 336038 529020 811757 1217097 1786974 2574191
7 17 48 117 244 456 814 1473 2780 5404 10469 19618 34866 58003 89199 124381 150969 141787 47566 -210361 -743548
9 19 38 75 144 269 489 864 1483 2475 4024 6389 9930 15141 22691 33474 48669 69811 98874 138367 191444
24 51 95 161 254 379 541 745 996 1299 1659 2081 2570 3131 3769 4489 5296 6195 7191 8289 9494
20 47 92 158 242 342 479 735 1319 2702 5920 13257 29734 66216 145609 314700 665942 1376443 2776969 5475497 10586448
22 32 39 45 55 77 122 204 340 550 857 1287 1869 2635 3620 4862 6402 8284 10555 13265 16467
15 41 87 159 274 480 898 1801 3745 7767 15665 30375 56460 100726 172980 286945 461347 721189 1099227 1637663 2390070
9 31 75 156 296 533 945 1709 3234 6430 13202 27289 55603 110262 211554 392116 702663 1219657 2055365 3370818 5392250
17 16 24 58 149 352 765 1562 3047 5742 10527 18857 33113 57256 98244 169297 297277 538492 1010530 1952780 3835717
-4 -10 -6 22 101 279 642 1364 2830 5903 12459 26389 55357 113705 227048 439477 825411 1511359 2721312 4879994 8854674
7 18 38 71 127 231 428 784 1385 2344 3849 6332 10919 20443 41475 88061 188155 394118 799120 1561845 2942567
14 41 89 169 296 496 816 1345 2271 4027 7622 15315 31875 66782 137867 277067 539188 1014829 1848927 3266741 5609506
18 40 77 136 239 443 865 1721 3399 6597 12568 23525 43270 78122 138230 239368 405320 670974 1086255 1721038 2671193
25 44 82 164 338 686 1343 2544 4740 8868 16940 33257 66813 135948 277250 562450 1130183 2244970 4405312 8539594 16359044
19 33 52 76 105 139 178 222 271 325 384 448 517 591 670 754 843 937 1036 1140 1249
5 3 8 37 129 362 874 1895 3810 7300 13657 25448 47820 90901 173969 332340 628275 1167633 2124510 3776711 6555611
2 0 2 7 20 76 284 891 2370 5549 11820 23498 44440 81083 144118 251084 430242 726174 1207646 1978377 3191468
18 38 78 145 245 395 643 1098 1989 3804 7610 15726 33013 69157 142477 286113 558311 1060805 1974813 3636314 6697044
12 15 31 80 207 502 1124 2320 4430 7874 13131 20764 31668 48014 75998 132765 262240 568849 1285555 2905416 6427525
9 20 57 129 242 411 683 1182 2199 4362 8933 18291 36672 71249 133647 242000 423669 718752 1184529 1900997 2977662
20 36 71 146 299 598 1163 2197 4026 7148 12291 20480 33113 52046 79687 119099 174112 249444 350831 485166 660647
6 6 4 0 -6 -14 -24 -36 -50 -66 -84 -104 -126 -150 -176 -204 -234 -266 -300 -336 -374
11 22 42 83 183 424 959 2050 4130 7935 14826 27579 52254 102430 208386 436124 925032 1959227 4097209 8398790 16809360
3 10 28 56 96 156 253 428 807 1773 4347 10907 26420 60490 130890 270136 538547 1050824 2029470 3908702 7528608
19 27 41 67 115 211 432 979 2303 5299 11583 23867 46447 85819 151438 256635 419707 665195 1025365 1541907 2267867
10 16 32 64 128 261 537 1088 2130 3994 7162 12308 20344 32471 50235 75588 110954 159300 224212 309976 421664
16 32 77 161 296 508 852 1422 2345 3755 5769 8552 12703 20486 38958 86905 208771 500560 1155348 2540791 5331527
3 14 40 79 135 225 391 729 1465 3144 7068 16254 37435 85089 189348 411361 873311 1818185 3731682 7595842 15421763
-6 1 31 101 245 521 1010 1818 3107 5196 8788 15394 28040 52358 98177 181745 328728 578147 987429 1638763 2646967
9 17 34 60 95 139 192 254 325 405 494 592 699 815 940 1074 1217 1369 1530 1700 1879
25 39 65 117 214 384 668 1124 1831 2893 4443 6647 9708 13870 19422 26702 36101 48067 63109 81801 104786
-2 15 47 94 156 233 325 432 554 691 843 1010 1192 1389 1601 1828 2070 2327 2599 2886 3188
8 17 25 35 65 166 450 1127 2556 5343 10593 20588 40495 82334 173586 374960 815974 1765347 3770455 7935871 16483923
12 30 57 111 226 453 868 1610 2994 5781 11752 24845 53298 113528 236903 481174 949176 1818536 3387603 6144707 10870234
9 23 48 87 146 232 365 612 1142 2298 4697 9421 18479 35938 70480 140679 285031 579709 1168110 2307407 4438328
5 9 13 17 21 25 29 33 37 41 45 49 53 57 61 65 69 73 77 81 85
4 17 52 115 211 349 564 978 1929 4204 9419 20596 42994 85258 160957 290589 504138 844275 1370302 2162945 3330109
10 15 12 7 15 63 212 623 1708 4428 10826 24914 54069 111134 217466 407224 733246 1274925 2148560 3520729 5625307
22 38 64 107 179 301 507 848 1396 2248 3530 5401 8057 11735 16717 23334 31970 43066 57124 74711 96463
12 24 44 80 145 251 400 572 710 702 360 -604 -2605 -6215 -12196 -21536 -35488 -55612 -83820 -122424 -174187
23 44 87 160 266 401 552 695 793 794 629 210 -572 -1849 -3778 -6543 -10357 -15464 -22141 -30700 -41490
14 21 37 69 123 204 316 462 644 863 1119 1411 1737 2094 2478 2884 3306 3737 4169 4593 4999
11 15 28 56 122 292 709 1640 3565 7387 14929 30019 60658 123030 248458 494847 964695 1832407 3384426 6076610 10614346
13 22 31 40 49 58 67 76 85 94 103 112 121 130 139 148 157 166 175 184 193
2 1 4 11 22 37 56 79 106 137 172 211 254 301 352 407 466 529 596 667 742
-1 4 20 56 137 314 676 1380 2738 5433 10973 22539 46480 94958 190859 377455 738137 1437094 2802250 5490714 10810339
3 -3 -12 -21 -20 13 127 432 1161 2769 6078 12477 24186 44593 78673 133498 218847 347925 538200 812367 1199448
14 25 44 76 126 202 323 530 898 1545 2638 4419 7338 12529 23187 48062 109558 261253 623704 1454122 3276214
3 -3 -11 -21 -33 -47 -63 -81 -101 -123 -147 -173 -201 -231 -263 -297 -333 -371 -411 -453 -497
13 11 16 34 74 151 288 517 879 1423 2204 3280 4708 6539 8812 11547 14737 18339 22264 26366 30430
13 26 64 140 267 458 726 1084 1545 2122 2828 3676 4679 5850 7202 8748 10501 12474 14680 17132 19843
-8 -16 -16 1 36 77 93 22 -257 -987 -2661 -6250 -13551 -27620 -53134 -96307 -163630 -258170 -371398 -467465 -455446
17 37 79 151 261 417 627 899 1241 1661 2167 2767 3469 4281 5211 6267 7457 8789 10271 11911 13717
2 4 7 14 34 90 228 537 1201 2617 5632 11982 25061 51205 101735 196083 366596 666669 1187211 2095303 3729248
13 22 31 40 49 58 67 76 85 94 103 112 121 130 139 148 157 166 175 184 193
13 16 20 21 19 38 172 682 2179 5939 14412 32011 66301 129753 242284 434870 754593 1271562 2088228 3351689 5269647
16 34 64 111 202 410 888 1921 4006 7970 15150 27728 49513 87902 158574 295840 573702 1145960 2319114 4681787 9334734
12 41 82 143 256 491 980 1961 3852 7365 13670 24619 43040 73111 120824 194549 305708 469569 706170 1041383 1508128
0 0 19 80 224 534 1171 2432 4865 9521 18495 36009 70412 137592 266370 506408 938914 1689834 2944111 4957746 8061548
15 21 21 15 16 53 166 390 725 1089 1251 741 -1266 -6095 -15748 -33116 -62229 -108547 -179295 -283845 -434148
0 1 8 21 40 65 96 133 176 225 280 341 408 481 560 645 736 833 936 1045 1160
8 0 -5 -5 -4 -18 -79 -230 -504 -880 -1209 -1103 220 4142 12909 29960 60328 111120 192083 316263 500764
8 18 39 82 181 407 897 1907 3906 7742 14943 28304 53137 100083 191490 375546 756444 1556154 3235883 6725970 13846021
-2 4 19 51 109 209 400 820 1802 4072 9115 19831 41661 84433 165260 312916 574222 1023092 1773019 2993923 4934437
10 38 90 189 382 757 1463 2730 4886 8368 13724 21603 32730 47863 67729 92936 123858 160490 202270 247865 294918
25 45 69 94 126 191 350 718 1487 2953 5547 9870 16732 27195 42620 64718 95605 137861 194593 269502 366954
6 10 24 47 75 101 115 104 52 -60 -254 -555 -991 -1593 -2395 -3434 -4750 -6386 -8388 -10805 -13689
28 51 97 184 348 658 1237 2303 4260 7901 14841 28398 55335 109272 217364 433327 862544 1709463 3364725 6560652 12640466
28 56 100 169 282 482 870 1680 3431 7206 15120 31052 61737 118354 218820 391127 678262 1145556 1891748 3065659 4891188
27 40 57 89 163 345 772 1688 3479 6702 12103 20619 33359 51559 76506 109426 151331 202820 263829 333325 408939
17 28 48 83 153 314 700 1597 3561 7592 15376 29607 54401 95814 162476 266353 423649 655860 990992 1464955 2123145
25 51 91 158 277 485 831 1376 2193 3367 4995 7186 10061 13753 18407 24180 31241 39771 49963 62022 76165
20 28 43 70 115 199 377 757 1520 2967 5670 10886 21511 44020 92118 193416 401919 822901 1666024 3363761 6837330
6 5 1 8 65 260 767 1896 4156 8331 15569 27484 46271 74834 116927 177308 261906 378001 534417 741728 1012477
5 9 28 72 153 285 484 768 1157 1673 2340 3184 4233 5517 7068 8920 11109 13673 16652 20088 24025
12 11 10 9 8 7 6 5 4 3 2 1 0 -1 -2 -3 -4 -5 -6 -7 -8
5 7 18 57 157 363 727 1305 2163 3395 5144 7611 11094 16359 26390 52309 129885 360031 999386 2649213 6628119
3 9 28 67 132 225 344 494 733 1307 2972 7659 19710 47999 109352 233794 472279 907701 1670140 2957467 5062616
-1 -4 -6 -5 1 14 36 69 115 176 254 351 469 610 776 969 1191 1444 1730 2051 2409
4 8 17 46 124 295 619 1173 2052 3370 5261 7880 11404 16033 21991 29527 38916 50460 64489 81362 101468
0 11 37 82 161 316 630 1232 2284 3939 6257 9064 11737 12896 9982 -1302 -27712 -79373 -170907 -322810 -563111
17 22 29 45 84 174 372 805 1775 3993 9039 20180 43714 91043 181710 347662 639021 1131656 1936849 3213335 5181968
12 26 65 137 258 463 827 1503 2776 5121 9235 15993 26284 40780 59995 85683 125964 208908 413109 929625 2178262
3 9 41 118 263 511 920 1591 2722 4758 8770 17321 36289 78483 170555 366011 769802 1585644 3209184 6414821 12733220
3 8 18 49 125 278 560 1078 2070 4062 8202 16982 35772 75975 161327 340264 710134 1464957 2990559 6054904 12186988
22 33 62 123 245 483 924 1697 3006 5210 8979 15575 27367 48824 88485 162835 303686 571647 1079652 2032395 3790001
9 23 39 56 73 92 134 275 703 1787 4127 8517 15720 25986 38463 51254 64137 88239 170635 447326 1245663
3 10 29 72 156 301 528 872 1445 2605 5304 11708 26235 57306 120454 244142 480915 928628 1769795 3342008 6259370
5 15 50 123 247 435 700 1055 1513 2087 2790 3635 4635 5803 7152 8695 10445 12415 14618 17067 19775
8 6 0 -11 -28 -52 -84 -125 -176 -238 -312 -399 -500 -616 -748 -897 -1064 -1250 -1456 -1683 -1932
-7 -11 -22 -49 -99 -165 -202 -89 428 1833 5033 11764 25428 52752 106971 213807 422547 826329 1598788 3059145 5785527
1 9 23 44 73 111 159 218 289 373 471 584 713 859 1023 1206 1409 1633 1879 2148 2441
2 -2 -6 -10 -14 -18 -22 -26 -30 -34 -38 -42 -46 -50 -54 -58 -62 -66 -70 -74 -78
6 25 52 87 130 181 240 307 382 465 556 655 762 877 1000 1131 1270 1417 1572 1735 1906
4 25 73 169 346 659 1200 2127 3740 6690 12503 24754 51450 109490 232478 483686 976612 1906367 3596069 6563535 11614858
10 15 24 54 145 365 817 1649 3059 5271 8428 12287 15487 13981 -1993 -53129 -178748 -445305 -948568 -1789600 -2978159
20 27 50 107 229 469 911 1679 2946 4943 7968 12395 18683 27385 39157 54767 75104 101187 134174 175371 226241
24 43 66 97 152 278 591 1339 2996 6393 12892 24609 44692 77660 129809 209691 328672 501575 747414 1090225 1560000
17 36 73 145 295 609 1245 2481 4789 8942 16161 28309 48139 79603 128229 201573 309753 466072 687737 996681 1420495
3 -2 -16 -47 -107 -212 -382 -641 -1017 -1542 -2252 -3187 -4391 -5912 -7802 -10117 -12917 -16266 -20232 -24887 -30307
28 40 56 79 118 207 432 975 2194 4768 9946 19949 38584 72139 130638 229545 392016 651808 1056964 1674403 2595554
22 37 48 62 111 274 717 1768 4057 8784 18255 36985 73971 147292 293167 583260 1156756 2278107 4438142 8526500 16118459
20 28 31 22 1 -12 48 346 1256 3565 8855 20240 43830 91682 187762 379947 764040 1531414 3062391 6106278 12121515
3 21 64 151 305 555 938 1495 2255 3212 4339 5782 8590 16750 42050 114636 304527 763720 1806688 4062716 8763847
-5 -8 -9 -7 4 51 217 708 1974 4919 11262 24171 49413 97482 187530 354488 661589 1221666 2232177 4030997 7182714
4 8 25 79 212 492 1033 2047 3961 7645 14810 28648 54799 102743 187728 333358 574978 964006 1573375 2504261 3894286
-2 5 30 101 276 661 1445 2973 5884 11344 21405 39519 71223 124967 212945 351550 560622 859875 1259620 1740949 2217666
-7 -8 -9 4 60 203 492 1001 1819 3050 4813 7242 10486 14709 20090 26823 35117 45196 57299 71680 88608
16 37 60 83 118 213 481 1140 2576 5449 10870 20685 37910 67369 116595 197062 325824 527645 837712 1305031 1996614
-2 13 39 81 164 348 759 1651 3529 7404 15326 31454 64073 129153 256256 497822 943088 1738095 3113393 5421135 9183226
12 22 24 21 26 68 197 489 1071 2213 4574 9756 21440 47597 104678 225502 474273 975871 1974631 3955014 7892109
12 22 47 91 153 239 387 708 1450 3102 6578 13564 27181 53221 102358 193929 362128 665766 1203129 2133921 3710817
5 14 33 77 169 338 613 1010 1514 2069 2610 3208 4460 8351 19956 50551 122979 280488 600743 1217335 2351891
11 18 30 56 128 306 674 1321 2312 3676 5476 8092 12961 24204 51862 117901 266777 583230 1221162 2449016 4719086
2 7 9 13 43 168 541 1459 3460 7479 15092 28892 53083 94494 164504 283014 486910 847911 1508995 2755743 5150299
16 26 35 45 58 76 101 135 180 238 311 401 510 640 793 971 1176 1410 1675 1973 2306
22 40 77 152 302 603 1211 2440 4916 9889 19855 39743 79064 155606 301497 572753 1063786 1928774 3412297 5892226 9938522
14 28 58 121 244 465 837 1448 2483 4367 8041 15436 30223 58930 112530 208617 374300 649958 1094012 1788883 2848318
-4 5 23 62 155 378 896 2049 4496 9435 18929 36416 67605 122240 217822 387670 698361 1286870 2437869 4740610 9399742
11 37 80 146 251 428 734 1257 2123 3503 5620 8756 13259 19550 28130 39587 54603 73961 98552 129382 167579
11 16 27 51 93 168 326 699 1580 3540 7580 15301 29056 52024 88117 141597 216241 313848 431833 559599 673319
11 32 67 117 181 256 337 417 487 536 551 517 417 232 -59 -479 -1053 -1808 -2773 -3979 -5459
20 37 75 143 251 410 637 972 1514 2483 4315 7797 14249 25760 45485 78010 129792 209681 329531 504907 755895
11 20 41 77 137 247 475 977 2062 4276 8538 16450 31078 58797 113250 223134 446445 895044 1775007 3450259 6539535
-10 -5 16 73 210 515 1151 2402 4745 8983 16524 29977 54385 99704 185751 352169 678720 1326687 2622432 5222501 10431052
4 13 19 18 6 -21 -67 -136 -232 -359 -521 -722 -966 -1257 -1599 -1996 -2452 -2971 -3557 -4214 -4946
16 22 32 43 47 25 -58 -250 -583 -984 -1075 215 5380 19814 55156 137406 326686 763622 1772714 4080627 9254333
9 17 31 56 108 238 563 1300 2807 5660 10855 20342 38296 73825 146230 294555 594328 1187117 2335500 4533656 8745983
0 6 25 68 164 384 882 1965 4221 8772 17786 35486 70043 136942 264673 503931 941918 1723834 3084231 5391592 9210294
-1 11 49 120 225 362 546 863 1575 3289 7198 15402 31331 60332 110563 194477 331399 552023 906111 1475292 2393669
'''

P1_SAMPLE_SOLUTION = 114

P2_SAMPLE_SOLUTION = 2

def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"

class History():
    def __init__(self,base):
        self.base = collections.deque(map(lambda x: int(x), base.split()))
        self.steps = [ self.base ]
        self.predicted_new_value = None
        self.predicted_old_value = None
        
        
    def next_step(self):
        this_step = collections.deque()
        this = None
        last = None
        for value in self.steps[-1]:
            last = this
            this = value
            if last != None:
                this_step.append(this - last)
                last = this
        
        self.steps.append(this_step)
        
        if this_step.count(0) == len(this_step):
            return True
        else:
            return False
        
    def find_bottom(self):
        step = self.next_step()
        while step == False:
            step = self.next_step()
            
        return True
            
    def predict_new_value(self):
        self.steps.reverse()
        carry_up = 0
        for step in self.steps:
            if step[-1] == 0:
                step.append(0)
                carry_up = 0
            else:
                carry_up += step[-1]
                step.append(carry_up)
        
        self.predicted_new_value = carry_up
        return carry_up

    def predict_old_value(self):
        carry_up = 0
        for step in self.steps:
            if step[-1] == 0:
                step.appendleft(0)
                carry_up = 0
            else:
                carry_up = step[0] - carry_up
                step.appendleft(carry_up)
        
        self.predicted_old_value = carry_up
        return carry_up


class Puzzle():
    def __init__(self,input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split('\n')
        self.oasis_rows = []
        for line in self.input_list:
            self.oasis_rows.append(History(line))
            
    def p1(self):
        self.p1_solution = 0
        for row in self.oasis_rows:
            row.find_bottom()
            row.predict_new_value()
            self.p1_solution += row.predicted_new_value
            
        return True

    def p2(self):
        self.p2_solution = 0
        for row in self.oasis_rows:
            row.predict_old_value()
            self.p2_solution += row.predicted_old_value
            
        return True

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