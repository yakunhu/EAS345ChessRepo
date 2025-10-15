import numpy as np
import csv
import total_effect
import central_effect 

file_path = "filtered_lichess/filtered_lichess_small.csv"
with open(file_path, 'r') as file:
    lines = file.readlines()[1:]
    with open("factors_proc.csv", mode="w",newline='',encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        header = ["ID","FEN","1","2","3","4","5","6","7"]
        writer.writerow(header)
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
            # print(bp[0])
            matrix = np.empty((8,8),dtype=str)
            # print(matrix)
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
            # print(matrix)
            # coords = np.array([4,6])
            factor_2 = central_effect.central_effect(matrix)
            factor_7 = total_effect.total_effect(matrix)  
            data = [row_array[0],row_array[1],"N/A",str(factor_2),"N/A","N/A","N/A","N/A",str(factor_7)]
            writer.writerow(data)
            break

