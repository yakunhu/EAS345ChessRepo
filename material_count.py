import numpy as np

def material_count(matrix):
    w_M = 0
    b_M = 0
    i = 0
    for rank in matrix:
        j = 0
        for piece in rank:
            if piece != "":
                if piece.isupper():
                    if piece == "N":
                        w_M += 3
                    if piece == "Q":
                        w_M += 9
                    if piece == "R":
                        w_M += 5
                    if piece == "B":
                        w_M += 3
                    if piece == "K":
                        w_M += 0
                    if piece == "P":
                        w_M += 1

                else:
                    if piece == "n":
                        b_M += 3
                    if piece == "q":
                        b_M += 9
                    if piece == "r":
                        b_M += 5
                    if piece == "b":
                        b_M += 3
                    if piece == "k":
                        b_M += 0
                    if piece == "p":
                        b_M += 1
            j+=1
        i+=1
    print(w_M)
    print(b_M)
    if w_M < 25 and b_M < 25:
        return None
    else: 
        return w_M - b_M

