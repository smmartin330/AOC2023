import argparse
from time import time

DAY = 7

PUZZLE_TEXT = """
--- Day 7: Camel Cards ---

Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends back to Island Island.

"Did you bring the parts?"

You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.

"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for; you're here to figure out why the sand stopped.

"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island, making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, but the machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.

You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. You agree automatically.

Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.

In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.
Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?
"""

SAMPLE_INPUT = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

PUZZLE_INPUT = """
3A399 27
46645 201
8A9K4 40
88333 578
55353 817
99Q99 146
553J5 45
AAQ2A 547
TKQ2K 120
57592 534
7Q49K 229
JK949 744
688T6 657
98888 392
4K638 337
J8888 96
Q92KJ 778
48J96 374
955J6 307
62TT6 896
934AK 776
44654 720
AJAAA 568
K6J5Q 162
T29A4 342
46342 467
22227 694
TQ4TT 468
88688 728
88999 183
Q7T6J 463
92T9J 884
KAQQQ 299
3275Q 913
Q5535 82
93A4J 48
J9888 552
2QTQ4 846
44554 795
JJJJJ 348
TT477 733
58883 460
77377 317
357J3 725
T9J4Q 346
88228 953
Q4858 982
5T5TT 405
TTKTT 322
QKKKK 197
A5Q5A 956
2T22A 962
TQJTT 734
84TAK 360
T39Q7 375
QJJTT 925
62236 928
474T7 302
37KK3 411
7J474 325
55K5J 850
TTJ2T 780
Q5259 127
93K6J 191
T996T 333
99929 193
9JKK3 115
2A647 409
3AAAA 966
85K58 464
22893 607
QJQJJ 471
59T9T 690
K8484 167
TKKK2 526
44243 273
KQ888 792
6J3K3 216
44446 169
325QK 461
47T2T 990
7J78J 410
A7JJA 562
2253J 598
QK385 103
65556 721
TTQQ9 943
Q4Q44 176
JJ8JJ 539
J799A 237
994QK 510
78996 458
AK663 145
QAA78 767
2Q662 797
A696A 572
QA82J 975
T7KJQ 126
722JT 416
2J222 57
6Q937 719
AKJ58 39
QQJQJ 582
AJATT 187
Q484A 384
T9T87 272
5T7T3 699
44K44 812
44228 505
983Q5 444
55355 74
J2JJ2 353
TJ2T2 883
Q96J9 708
7KKKK 447
557J5 280
AT4T7 407
AQ9JJ 73
K6K2J 597
K7Q7K 394
QQ4JQ 635
2JK35 269
94934 78
99K9K 235
K7K27 91
QQQTQ 588
773A3 702
26232 110
AA44A 909
33Q3Q 313
83335 518
7AA84 287
484T4 662
7JKK7 29
9J999 38
Q58T9 17
29JQ7 355
772TT 783
JK66K 473
TKKTK 433
52T56 318
8Q734 628
K43J7 226
AA569 77
J4A54 988
84J4J 500
97TQ9 240
4K554 305
27999 847
8QQ83 85
57638 521
K5KK9 974
97K3Q 234
T88TT 747
22JAT 71
TJ337 983
TA3QK 555
87686 372
5KKKK 828
QK868 168
99J59 813
AA28A 875
47382 837
27K77 46
2KKKJ 10
22292 448
K4KKK 774
A3A9K 428
99222 184
Q9Q4Q 336
QQQQ4 631
KJQTT 249
T3K46 644
929J9 165
2KK22 527
AKAA5 358
Q2224 369
T273J 265
282JJ 28
Q488Q 513
38J88 633
3T3T3 283
88855 863
6J39Q 75
J44K4 543
27272 731
5576K 880
JTTKT 400
55J55 750
2QQ99 919
4668Q 55
9A999 5
JK294 536
TJ937 692
KKKKJ 86
647J4 625
94227 308
6AJ5J 841
99AA5 224
685A7 24
TAAKK 112
286K4 762
J5Q8A 232
33323 494
2A6Q3 495
JQKT2 37
AAAQA 978
K34KJ 703
7J74T 994
2J828 723
5T3T4 535
48658 140
J99JJ 954
TT826 678
KK3J8 840
TTT6J 439
7QQ6T 589
58585 963
TTT2A 190
JQT52 261
66J76 682
925KQ 951
T3223 141
J78QJ 785
QQ277 567
4K6TK 349
K888K 309
2J664 713
75657 218
96J96 614
23727 610
89477 134
T8456 957
7K47A 230
A3AA3 107
24KK3 538
65J48 119
JA98K 647
KKT6T 935
A4AAK 248
K7779 225
J5574 438
Q6QQQ 697
39QTT 469
K9J62 282
2K242 971
QJJK6 41
49J77 122
393KK 403
Q222Q 789
88Q8Q 587
4Q8AA 247
63396 211
KKJJK 111
JQ4K7 918
79775 506
T5T55 532
8J558 125
2QAK8 641
59548 537
345K6 106
Q42K7 695
88KKK 934
4J8J6 519
644JJ 612
J796K 368
3J633 621
66T3A 707
7Q3K3 768
A258Q 866
9463A 820
58555 843
36T4J 914
96K4A 8
Q34J7 654
88QAA 651
AA5J5 58
73333 740
JTT9T 609
3QQQQ 871
33957 442
84888 446
83Q83 742
K2K3K 243
JKJ94 377
K62K2 385
6QJ87 704
847J7 61
87J89 594
77JQQ 54
56KA5 56
AAQQ9 233
A8AKT 236
37KKA 711
J8279 244
J2Q23 987
666J6 939
3JJ77 16
QQQKQ 104
96QQ4 398
J38JA 585
8QKQ8 899
4TJK2 806
66686 421
5T4T5 889
K4944 206
65KQ6 443
36366 59
TJT36 996
JAA3A 367
4985K 395
999QQ 926
832J6 821
88K7K 890
J7777 902
35855 991
332KK 710
76AT7 365
533K3 65
AAAA9 864
45TT4 758
TJJTT 418
282TT 178
T536K 474
J5J3A 259
Q3QAA 796
222JJ 793
Q4666 64
93TT9 219
69555 26
449JA 238
64935 754
7K24K 622
Q7999 932
55474 288
J5QQ5 929
J794A 669
44K4K 634
8T6A5 808
77252 7
JA8Q4 70
3JTKJ 181
34433 845
A3444 548
84889 262
4A9TQ 32
85A88 189
73883 321
7T776 274
K62QJ 138
TQ7TQ 80
6A7AA 786
TA379 872
25T33 584
73747 965
Q28KQ 1000
2A222 144
94993 345
A9238 172
8468T 630
99646 649
69KK7 210
QK5K6 457
6QJ6Q 12
36339 643
88A4J 63
K57JK 549
77888 382
T4J56 198
AQQA7 481
644K2 492
T46AA 397
5J3TJ 861
J7J79 20
3333A 42
QQ555 892
3AJT5 36
J4K8A 208
874TJ 376
J999J 215
A8AK3 782
84444 504
TT2TT 905
8746J 752
AA5A5 449
A75JT 204
55595 379
KK665 775
22244 364
22283 152
AA25A 149
AA3KA 826
K399K 981
93384 97
46494 347
3TQJ4 19
KKK7Q 158
776J2 267
7A77J 486
A4454 9
6857K 858
3J3TT 435
339J3 99
JAQJQ 105
82367 571
3QQ3Q 556
QJTJQ 599
696T3 334
JKA22 829
J6686 576
92Q4J 217
8288K 289
7JJKA 904
33383 613
J339T 315
88483 503
9995A 319
8K92J 483
TJ244 266
KJ957 574
74A44 148
77KK7 591
QJQ75 898
88J8J 885
92K54 137
64647 579
66226 560
JJ488 839
43J42 673
3K3K3 849
99977 108
JTT47 113
2634T 68
TJQT5 838
77Q77 763
2AAKA 972
78QJ7 257
6J923 544
2J2KK 164
259K3 882
88K78 602
4786Q 924
42444 650
8536T 52
AQTT5 546
3333J 581
3K984 501
A8832 685
34J55 133
62985 700
4353J 386
44454 23
77772 116
65665 679
KKK7J 124
A7578 749
5AQ54 396
7KK8Q 807
7T7T8 911
73JJT 157
98A99 753
446J4 477
4T43A 205
TT999 798
88885 915
9Q64J 659
7767K 357
A5329 559
85KKK 739
9969J 714
QJQQ9 427
KT4KT 15
5T5J5 638
J74AJ 736
56666 524
5T558 930
2233A 350
7AA4A 502
QAAA7 595
7737T 151
JQ4Q6 677
67864 691
2KK3Q 117
8272K 414
75J57 159
443J4 479
55KK5 207
K88TK 910
3Q9J9 332
JAJAJ 338
69369 339
82KJ6 335
K39KK 773
99492 422
3T663 270
T5958 328
9A45K 715
23593 922
JKK37 765
KJKT7 769
Q74QQ 173
6232T 729
227Q2 436
7AQK4 430
8Q4JQ 509
J8248 297
TT779 306
A3K34 852
97228 832
TJTJ7 300
A8898 553
82TJQ 4
92738 131
AAAJJ 440
TT972 51
69AQK 646
QQ7QJ 705
4JK85 718
7Q63T 220
44A24 737
7QAQT 292
66699 979
3Q974 329
TTT6T 648
85288 686
989QT 278
7Q6AK 964
66466 251
99744 271
TTQTQ 163
3433T 177
K2333 142
QQ4Q4 938
9Q6Q9 787
47T63 831
2J56T 493
94494 72
25552 869
936K2 390
A8AA8 605
3TT35 727
2A24T 129
94999 323
64A2J 824
K7676 756
QQQQ7 18
882J8 748
2J77A 611
222TJ 959
T6266 722
823J3 627
8T569 771
58KK3 331
59329 209
K9K87 6
82484 150
9444A 98
TQ445 487
J999K 462
JT4TT 246
5A455 640
67KAJ 687
6A83J 570
36J6J 90
6AK6A 573
88K88 781
5A3K4 931
22J27 499
44T44 948
K44TT 213
554K5 927
6528A 202
999JT 667
7J256 401
A2272 937
2QJ3Q 900
63736 973
32522 933
T666T 664
88992 706
JK267 603
QQ99Q 316
AKKKK 507
8688J 862
48858 970
66229 378
K495Q 14
79539 761
A33K3 491
QAQQQ 417
T92JA 620
AQQ8J 475
64A4K 295
4A824 231
8KTK3 453
229K5 969
Q3Q53 284
Q6K34 35
QJQ8Q 402
39922 69
J9TK8 920
4Q3K8 881
454AA 999
556Q9 531
22K22 496
6AA39 291
792K3 810
TQQTJ 660
J677K 764
QTTTT 998
22223 529
3333Q 842
2AAJA 755
J64K6 466
TJA4T 693
J2622 441
42442 566
754K8 459
35826 976
4743T 676
693TA 672
58887 391
K4899 434
TTTT3 88
356T2 894
77784 212
3373T 399
78777 895
Q97TT 950
88T8T 760
J48K2 663
J3A3A 424
555T5 25
37373 389
J6J46 174
4TAKT 171
6TKQ7 624
5A775 3
TT3T3 326
28558 489
TJ38T 936
6AK66 254
44664 223
77QQ7 87
Q2829 675
5TTJ5 995
T2T9J 454
7878A 264
83843 84
JKKK3 802
98436 192
3AA22 940
555A5 136
J333J 221
97KJ3 636
JK582 801
5Q82K 515
25J2T 180
34234 746
JQ4K9 255
224J2 668
68999 639
7T77T 886
6A92Q 629
JJ55J 161
99599 429
6JQ3Q 43
4699A 361
75AT2 917
T9TTT 514
55A95 551
J6A96 47
AAJAT 617
64669 222
QQ9QQ 626
44J44 688
Q3355 92
J8J8J 835
T4382 363
J359A 296
49Q49 653
AAT66 908
44T72 961
AKA44 901
49994 290
A344A 732
JJQJK 777
J8JQ8 819
A89T9 565
72A72 868
K7867 153
K6663 179
K76K7 854
9T265 419
9K7K9 865
7797J 426
25KKJ 670
75575 11
75955 431
TK99Q 684
KJ273 76
57525 285
J3AAJ 263
Q7QQT 590
Q77AQ 879
33626 423
AAA77 139
76584 730
2K9QQ 356
22225 857
44KKK 656
954K6 814
79TA5 135
KQKKJ 62
5QQ88 311
77K87 452
ATTTT 370
J64QA 815
29399 985
2T792 351
5782A 324
57T74 294
TQJ53 182
42222 645
K4Q92 320
77A7K 583
AA999 977
T77TK 279
5T586 799
6K67Q 301
6J8J2 67
99JJT 344
A395K 540
35AAA 779
68QT3 557
45T3K 175
587Q2 717
8QK39 616
73574 550
T8A36 986
333AA 800
2KKKK 393
9Q6T9 250
A88A8 203
J4J44 194
848J8 281
5A49Q 44
8J88A 406
8JTTT 877
77767 955
22K46 199
6A9AT 387
T5Q7K 482
52999 577
Q6685 632
TQJQQ 525
77477 712
K5656 601
KKA7A 380
AA66A 373
83ATT 942
3JJ9K 508
89988 791
TQ746 757
8J99T 743
KKK22 642
J44K2 980
K9KAA 830
9AAA9 260
558J5 870
KQKK2 352
JT4T4 498
K647T 967
9K364 569
44833 844
T2922 856
T3463 276
2TTT2 60
Q542A 724
7J724 992
KT92K 286
8K388 888
4394Q 600
Q747Q 818
433J4 945
66J45 381
55J59 912
9A5A5 606
3K98A 195
9J49A 523
2642J 944
9K8Q7 89
3J335 241
J639J 564
63J79 383
5Q4J7 455
777T7 674
6793A 166
KK9KK 277
4TA95 873
KQJA9 81
2T777 834
4K44A 109
93572 312
33537 258
756KQ 304
4J449 770
27JKQ 412
KK8KK 596
J9666 415
34943 93
85J6K 404
J6QJ5 118
4A452 343
7548A 327
6644J 472
T3A7Q 887
T3J3J 661
QQ79Q 516
73JAT 592
2QQQJ 413
QJ523 541
82878 488
722T2 256
4KA4K 923
96T99 490
3AKK6 696
6J6JJ 147
922JA 593
J88K6 371
52245 867
84664 637
T2T22 853
T26A9 952
8686J 253
J6AA3 53
6A65A 701
JAJTA 745
3843A 859
39399 114
J28Q3 121
98KT4 13
TTQTA 772
39KTT 683
53J53 298
47434 671
4J33Q 542
9Q9J9 214
TTTT8 984
A45K7 891
K488K 916
AJ636 997
7QQQ7 563
68877 359
655QQ 790
3AA4A 855
T4TTT 958
9246Q 666
85K48 485
AJ283 484
54J5K 21
KK9K9 2
Q69Q3 22
J4555 809
J322J 921
752J5 530
6K43K 480
6AAAA 836
92A29 803
66888 665
25529 83
2AJ22 558
89999 476
Q8777 155
7787J 388
Q2765 123
TJ2TK 833
55AA5 903
22662 33
7QQQ2 575
7J77J 561
72878 874
QQJQQ 154
T693Q 520
5TT3T 31
JQQ44 340
2JJ2Q 804
J24T2 784
K7J3J 811
7KTJT 156
8848Q 228
44944 947
K5426 893
A55A8 655
AAKK8 619
75555 751
Q2222 816
TJJ9J 906
J4224 314
26A7K 738
97J54 1
7KK7K 794
3KKK5 451
955K9 827
Q9QA2 293
J2A28 200
J2K77 341
83888 196
J97K7 823
75TJ9 186
J7638 49
46K36 128
92JJJ 735
29A87 185
89449 100
3KAJK 445
QQ343 586
8466J 79
T3T37 362
252T4 528
A3A5J 242
6QQQT 822
7AJA6 615
K9625 268
KK3AK 517
5Q5Q8 658
T87K3 618
57629 788
A7A7Q 160
889TQ 741
TT59T 425
Q2KQJ 30
A4K3K 143
6664K 456
KK4J4 726
TTTTJ 437
QT824 132
J555J 478
75KK9 354
94979 34
K846J 432
QQ887 130
TT97T 170
66TQ6 878
57K78 993
88JK8 608
AK5Q3 907
AATAA 989
QJQ8J 533
8QQQQ 522
5JQ49 102
T3T65 188
66446 759
3Q695 275
AAQTA 689
43J33 623
TJ444 968
Q28Q2 330
J777T 450
QT3JQ 420
T327A 897
QKQKK 580
92KA7 946
7A93K 497
6KAAA 239
889TA 50
K5KK5 511
J443J 303
TTT7J 310
QAK8A 252
J8658 805
896K6 680
88482 876
69QJQ 408
4A3J2 941
8868T 94
7766Q 851
62J25 825
3TT9T 716
Q5KKK 860
K7488 95
33343 766
JT888 366
J8885 681
J66J6 554
JA65K 604
QTJ44 848
583QJ 465
89Q79 66
27477 512
JTK33 101
TTTQK 652
A4ATA 545
J3A33 470
34QAK 245
6Q668 698
66777 709
5K557 227
43666 949
66A6A 960
"""

P1_SAMPLE_SOLUTION = 6440

P2_SAMPLE_SOLUTION = 5905

HAND_TYPES = {
    7: "Five of a Kind",
    6: "Four of a Kind",
    5: "Full House",
    4: "Three of a Kind",
    3: "Two Pair",
    2: "One Pair",
    1: "High Card",
}

P1_CARD_MAPPING = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 11,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2
}

P2_CARD_MAPPING = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 1,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2
}


def elapsed_time(start_time):
    return f"{round(time() - start_time, 8)}s\n"


class Hand:
    def __init__(self, cards, bid, type):
        self.cards = cards
        self.bid = bid
        self.unique_cards = set(cards)


class Puzzle:
    def __init__(self, input_text):
        self.input_text = input_text
        self.input_list = input_text.strip().split("\n")


    def p1(self):
        self.hands = []
        self.hands_reverse = []
        for hand in self.input_list:
            hand = hand.split()
            cards, bid = [*hand[0]], int(hand[1])
            uniques = set(cards)
            if len(uniques) == 1:
                # 1 unique = 5 of a kind
                hand_type = 7
            elif len(uniques) == 2:
                # 2 uniques = 4 of a kind OR full house
                if ( 
                    cards.count(cards[0]) == 4
                    or cards.count(cards[1]) == 4
                    or cards.count(cards[2]) == 4
                    or cards.count(cards[3]) == 4
                    or cards.count(cards[4]) == 4
                ):
                    hand_type = 6
                else:
                    hand_type = 5
            elif len(uniques) == 3:
                # 3 uniques = 3 of a kind OR two pair
                if (
                    cards.count(cards[0]) == 3
                    or cards.count(cards[1]) == 3
                    or cards.count(cards[2]) == 3
                    or cards.count(cards[3]) == 3
                    or cards.count(cards[4]) == 3
                ):
                    hand_type = 4
                else:
                    hand_type = 3
            elif len(uniques) == 4:
                # 4 uniques = one pair
                hand_type = 2
            else:
                # 5 uniques = high card.
                hand_type = 1
            cards = list(map(lambda x: P1_CARD_MAPPING[x], cards))
            this_hand = [hand_type] + cards + [bid]
            self.hands.append(this_hand)
            self.hands_reverse.append(this_hand)

        self.hands.sort()
        self.hands_reverse.sort()
        self.hands_reverse.reverse()
        self.p1_solution = 0
        rank = 1
        for hand in self.hands:
            score = rank * hand[6]
            self.p1_solution += score
            rank += 1

        return True

    def p2(self):
        self.hands = []
        self.hands_reverse = []
        for hand in self.input_list:
            hand = hand.split()
            cards, bid = [*hand[0]], int(hand[1])
            uniques = set(cards)
            jokers = cards.count('J')
            if len(uniques) == 1:
                # 1 unique = 5 of a kind
                hand_type = 7
            elif len(uniques) == 2:
                # 2 uniques = 4 of a kind OR full house
                if ( 
                    cards.count(cards[0]) == 4
                    or cards.count(cards[1]) == 4
                    or cards.count(cards[2]) == 4
                    or cards.count(cards[3]) == 4
                    or cards.count(cards[4]) == 4
                ):
                    if jokers >= 1: # 4 of a kind + a joker bumps to 5 of a kind
                        hand_type = 7
                    else:
                        hand_type = 6
                else:
                    if jokers == 3 or jokers == 2: # Full house but either the set or pair is jokers, that becomes 5 of a kind.
                        hand_type = 7
                    else:
                        hand_type = 5
            elif len(uniques) == 3:
                # 3 uniques = 3 of a kind OR two pair
                if (
                    cards.count(cards[0]) == 3
                    or cards.count(cards[1]) == 3
                    or cards.count(cards[2]) == 3
                    or cards.count(cards[3]) == 3
                    or cards.count(cards[4]) == 3
                ):
                    if jokers == 3: # the set is 3 jokers, that is going to turn into 4 of a kind.
                        hand_type = 6
                    elif jokers == 2: # this shouldn't be possible!!! a set + 2 jokers should have been caught as a full house.
                        pass
                    elif jokers == 1: # 3 of a kind + 1 joker = 4 of a kind
                        hand_type = 6
                    else: # no jokers
                        hand_type = 4
                else:
                    if jokers == 2: #2 pairs, but one pair is jokers. that is 4 of a kind
                        hand_type = 6
                    elif jokers == 1: # 2 pairs PLUS a lone joker creates a full house. 
                        hand_type = 5
                    else: # no jokers, it's just 2 pairs. 
                        hand_type = 3
            elif len(uniques) == 4:
                # 4 uniques = one pair
                if jokers == 2: # 1 pair and they are jokers. this means 3 of a kind. 
                    hand_type = 4
                elif jokers == 1: # 1 pair PLUS a lone joker creates 3 of a kind. 
                    hand_type = 4
                else: # no jokers, it's just 2 pairs. 
                    hand_type = 2
            else:
                # 5 uniques = high card.
                if jokers == 1: # high card but one is a joker, we got a pair
                    hand_type = 2
                else: # high card without jokers is high card. 
                    hand_type = 1

            cards = list(map(lambda x: P2_CARD_MAPPING[x], cards))
            this_hand = [hand_type] + cards + [bid]
            self.hands.append(this_hand)
            self.hands_reverse.append(this_hand)

        self.hands.sort()
        self.hands_reverse.sort()
        self.hands_reverse.reverse()
        
        self.p2_solution = 0
        rank = 1
        for hand in self.hands:
            score = rank * hand[6]
            self.p2_solution += score
            rank += 1
        return True


def main():
    parser = argparse.ArgumentParser(description=f"AOC2023 Puzzle Day { DAY }")
    parser.add_argument(
        "-p", "--showpuzzle", help="Display Puzzle Text", action="store_true"
    )
    parser.add_argument(
        "-s", "--showsample", help="Display Sample Input", action="store_true"
    )
    args = parser.parse_args()

    if args.showpuzzle:
        print(f"###############\nAOC 2023 DAY {DAY} PUZZLE TEXT\n###############")
        print(PUZZLE_TEXT)

    if args.showsample:
        print(f"###############\nAOC 2023 DAY {DAY} SAMPLE INPUT\n###############")
        print(SAMPLE_INPUT.strip())
        print(
            f"\n###############\nAOC 2023 DAY {DAY} P1 SAMPLE SOLUTION\n###############"
        )
        print(P1_SAMPLE_SOLUTION)
        print(
            f"\n###############\nAOC 2023 DAY {DAY} P2 SAMPLE SOLUTION\n###############"
        )
        print(P2_SAMPLE_SOLUTION)

    if P1_SAMPLE_SOLUTION:
        print("PART 1\nTesting Sample...\n")
        start_time = time()
        sample = Puzzle(input_text=SAMPLE_INPUT)
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
