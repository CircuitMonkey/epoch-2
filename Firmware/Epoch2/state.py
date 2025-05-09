# State Machine

"""

0 = Start/Configure
1 = Mode Select
2 = Manual
3 = Cycle
4 = Pendulum
5 = Plunge
6 = Pull
...
20 = Config 1
21 = Config 2
22 = Config 3
23 = Config 4
24 = Config 5
25 = Config 6
26 = Config 7
27 = Config 8
...
30 = Save to Faves
31 = Load from Faves
"""
modes = [
    [1, 31, 32, 20, 21, 22, 23, 24, 25, 26, 27], # 0 - Configure
    [2,3,4,5,6], # 1 - Mode Select
    [1], # 2 - Manual
    [1], # 3 - Cycle
    [1], # 4 - Pendulum
    [1], # 5 - Plunge
    [1], # 6 - Pull
    [1], # 7 - XX (future mode)
    [1], # 8 - XX
    [1], # 9 - XX
    [1], # 10 - XX
    [1], # 11 - XX
    [1], # 12 - XX
    [1], # 13 - XX
    [1], # 14 - XX
    [1], # 15 - XX
    [1], # 16 - XX
    [1], # 17 - XX
    [1], # 18 - XX
    [1], # 19 - XX
    [0], # 20 - Config Ch. 1
    [0], # 21 - Config Ch. 2
    [0], # 22 - Config Ch. 3
    [0], # 23 - Config Ch. 4
    [0], # 24 - Config Ch. 5
    [0], # 25 - Config Ch. 6
    [0], # 26 - Config Ch. 7
    [0], # 27 - Config Ch. 8
    [0], # 28 - XX (unused)
    [0], # 29 - XX (unused)
    [0], # 30 - Save to Favs
    [0]  # 31 - Load from Favs
]

mode = 0

title = ["Configure", "Select Mode",
    "Manual", "Cycle", "Pendulum", "Plunge", "Pull",
    "Unused", "Unused", "Unused", "Unused", "Unused",
    "Unused", "Unused", "Unused", "Unused", "Unused",
    "Unused", "Unused", "Unused",
    "Configure 1", "Configure 2", "Configure 3", "Configure 4",
    "Configure 5", "Configure 6", "Configure 7", "Configure 8",
    "Unused", "Unused",
    "Save to Faves", "Load from Faves"
]
