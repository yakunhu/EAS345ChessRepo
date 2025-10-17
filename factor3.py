import numpy as np
#counts the total diagonal control for a bishop or queen
#count all empty squares until it hits another piece 
#if it's an enemy peice, count that sqaure too
def D_Control(position, matrix):
    row, col = position
    piece = matrix[row, col]

    directions = [
        (-1, -1),  # up-left
        (-1, +1),  # up-right
        (+1, -1),  # down-left
        (+1, +1)   # down-right
    ]

    control = 0

    for row_step, col_step in directions:
        r, c = row + row_step, col + col_step

        while 0 <= r <= 7 and 0 <= c <= 7:
            target = matrix[r, c]

            if target == "":
                control += 1
            else:
                #check color
                if piece.isupper() and target.islower():
                    control += 1  
                elif piece.islower() and target.isupper():
                    control += 1  
                break  

            r += row_step
            c += col_step

    return control

def total_control(matrix):
    w_E = 0
    b_E = 0
    i = 0
    for rank in matrix:
        j = 0
        for piece in rank:
         