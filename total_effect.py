import numpy as np

def N_Effect(coords,matrix):
    print(coords)
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
                else:
                    if piece == "n":
                        b_E += N_Effect(np.array([i,j]),matrix)
            j+=1
        i+=1
    return w_E - b_E

