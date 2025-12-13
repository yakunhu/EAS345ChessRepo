import numpy as np

def N_Effect(coords,matrix):
    # print(coords)
    effects = 0
    rank,file = coords
    one = np.array([rank-2,file+1])
    two = np.array([rank-1,file+2])
    four = np.array([rank+1,file+2])
    five = np.array([rank+2,file+1])
    seven = np.array([rank+2,file-1])
    eight = np.array([rank+1,file-2])
    ten = np.array([rank-1,file-2])
    eleven = np.array([rank-2,file-1])
    movements = np.array([one,two,four,five,seven,eight,ten,eleven])
    for direction in movements:
        if direction[0] <=7 and direction[0] >=0 and direction[1] <=7 and direction[1] >=0:
            if matrix[direction[0],direction[1]] != "":
                # print(matrix[direction[0],direction[1]])
                # print(direction[0],direction[1])
                effects+=1
    # print(effects)
    return effects

def V_Effect(coords, matrix):
    # print(coords)
    effects = 0
    rank, file = coords

    # 4 rook directions (ranks/files)
    movements = np.array([
        [-1,  0],  # up
        [ 1,  0],  # down
        [ 0, -1],  # left
        [ 0,  1],  # right
    ])

    for dr, df in movements:
        r, f = rank + dr, file + df
        while 0 <= r <= 7 and 0 <= f <= 7:
            if matrix[r, f] != "":
                effects += 1
                break
            r += dr
            f += df
    return effects

def D_Effect(position, matrix):

    # Get the row and col of the piece
    row = position[0]
    col = position[1]

    directions = [
        (-1, -1),  # northwest (up-left)
        (-1, +1),  # northeast (up-right)
        (+1, -1),  # southwest (down-left)
        (+1, +1)   # southeast (down-right)
    ]

    effects = 0

    # Check each direction
    for row_step, col_step in directions:
        # step into direction 
        r = row + row_step
        c = col + col_step

        # Keep looping as long as r and c are valid board coordinates (between 0 and 7)
        while 0 <= r <= 7 and 0 <= c <= 7:
            # If we find a piece count it and stop this direction
            if matrix[r, c] != "":
                effects += 1
                break
            # Move one more step along the same diagonal
            r += row_step
            c += col_step
    # print(position)
    # print(effects)
    return effects

def K_Effect(coords, matrix):
    effects = 0
    rank,file = coords
    N = np.array([rank-1,file])
    S = np.array([rank+1,file])
    E = np.array([rank,file+1])
    W = np.array([rank,file-1])
    NW = np.array([rank-1,file-1])
    NE = np.array([rank-1,file+1])
    SW = np.array([rank+1,file-1])
    SE = np.array([rank+1,file+1])
    movements = np.array([N,S,E,W,NW,NE,SW,SE])
    for direction in movements:
        if direction[0] <=7 and direction[0] >=0 and direction[1] <=7 and direction[1] >=0:
            if matrix[direction[0],direction[1]] != "":
                # print(matrix[direction[0],direction[1]])
                # print(direction[0],direction[1])
                effects+=1
    # print(coords)
    # print(effects)
    return effects

def P_Effect(coords, matrix):
    """
    Count how many *occupied* squares are on a pawn's capture diagonals
    from `coords`. Matches N_Effect semantics:
      - Only counts occupied targets ("" is empty → not counted)
      - White pawns capture up-left/up-right (row - 1)
      - Black pawns capture down-left/down-right (row + 1)
    """
    # print(coords)  # mirror N_Effect debug
    effects = 0
    rank, file = coords
    piece = matrix[rank,file]

    # Absolute target squares for pawn captures (NOT forward pushes)
    if piece.isupper():  # White pawn
        movements = np.array([
            [rank - 1, file - 1],
            [rank - 1, file + 1],
        ])
    else:                # Black pawn
        movements = np.array([
            [rank + 1, file - 1],
            [rank + 1, file + 1],
        ])

    for r, f in movements:
        if 0 <= r <= 7 and 0 <= f <= 7:       # on board
            if matrix[r, f] != "":            # occupied → count
                effects += 1
    # print(coords)
    # print(effects)
    return effects

def total_effect(matrix):
    w_E = 0
    b_E = 0
    i = 0
    for rank in matrix:
        j = 0
        for piece in rank:
            if piece != "":
                if piece.isupper():
                    if piece == "N":
                        w_E += N_Effect(np.array([i,j]),matrix)
                    if piece == "Q":
                        w_E += V_Effect(np.array([i, j]), matrix)
                        w_E += D_Effect(np.array([i, j]), matrix)
                    if piece == "R":
                        w_E += V_Effect(np.array([i, j]), matrix)
                    if piece == "B":
                        w_E += D_Effect(np.array([i, j]), matrix)
                    if piece == "K":
                        w_E += K_Effect(np.array([i,j]),matrix)
                    if piece == "P":
                        w_E += P_Effect(np.array([i,j]),matrix)

                else:
                    if piece == "n":
                        b_E += N_Effect(np.array([i,j]),matrix)
                    if piece == "q":
                        b_E += V_Effect(np.array([i, j]), matrix)
                        b_E += D_Effect(np.array([i, j]), matrix)
                    if piece == "r":
                        b_E += V_Effect(np.array([i, j]), matrix)
                    if piece == "b":
                        b_E += D_Effect(np.array([i, j]), matrix)
                    if piece == "k":
                        b_E += K_Effect(np.array([i,j]),matrix)
                    if piece == "p":
                        b_E += P_Effect(np.array([i,j]),matrix)
            j+=1
        i+=1
    # print(w_E)
    # print(b_E)
    return w_E - b_E

