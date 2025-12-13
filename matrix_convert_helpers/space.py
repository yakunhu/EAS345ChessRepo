import numpy as np
def pawn_space(matrix):
    w_sum = 0
    b_sum = 0
    
    # row
    for i in range(8):  
        # column
        for j in range(8):     
            piece = matrix[i, j]
            # white pawn starts at 6
            if piece == "P":   
                w_sum += 6 - i 
            # black pawn starts on row 1   
            elif piece == "p":      
                b_sum += i - 1      
    #print("white sum: ", w_sum)
    #print("black sum: ", b_sum)
    #print("total: ")
    return w_sum - b_sum