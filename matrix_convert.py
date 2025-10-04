import numpy as np

file_path = "filtered_lichess/filtered_lichess_small.csv"
with open(file_path, 'r') as file:
    lines = file.readlines()[1:]
    for row in lines:
        row_array = row.split(',')
        FEN = row_array[1]
        bp = ""
        for char in FEN:
            if char=='"':
                continue
            elif char == " ":
                break
            else:
                bp+=char
        # print(bp)
        bp = bp.split('/')
        # print(bp)
        print(bp[0])
        matrix = np.empty((8,8),dtype=str)
        print(matrix)
        i = 0
        for rank in bp:
            j = 0
            for sq in rank:
                if sq.isdigit():
                    j+=int(sq)-1 
                else:
                    matrix[i,j] = sq
                j+=1
            i+=1
        print(matrix)    
        break
