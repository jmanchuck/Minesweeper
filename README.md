# Minesweeper  

Requires: Python 3, numpy

Written by: jmanchuck, stanleyycheung

## Gameplay

Run main.py.

Change board arguments in ```main.py``` to customise number of cells and number of bombs. 
``` 
board = Board(n size, number of bombs) 
```

Left click to open a cell, right click to flag a cell and left click an already open cell to auto reveal neighbours when all its neighbours have been flagged.

## Change Log


15/07 
* initialized
* written basic pygame interface: initialized white screen

31/07
* updated ```objects.py``` features with auto-open and win/lose conditions

01/08
* updated ```main.py```
* fixed gameplay for opening cells, added auto-open to pygame
* added replay condition and win/lose conditions to pygame

04/08
* made pygame interface variable sized for different nxn Minesweeper games

05/08
* moved auto open to left click, added icons for bombs and flags, updated colours

09/09
* update ```objects.py```, removed redundant methods, combined neighbour board and bomb board and cell board
