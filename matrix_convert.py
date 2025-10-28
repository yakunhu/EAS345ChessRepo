import numpy as np
import csv
import total_effect
import central_effect
import diag_control
import vertical_control
import material_count
import space
import adv_knights

file_path = "filtered_lichess/filtered_lichess_small.csv"
with open(file_path, 'r') as file:
    lines = file.readlines()[1:]
    with open("factors_proc.csv", mode="w",newline='',encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        header = ["ID","FEN","1","2","3","4","5","6","7","side"]
        writer.writerow(header)
        # row_num = 0
        for row in lines:
            # if row_num == 0:
                # row_num += 1
                # continue
            row_array = row.split(',')
            FEN = row_array[1]
            bp = ""
            c = 0
            for char in FEN:
                if char=='"':
                    continue
                elif char == " ":
                    side = FEN[c+1]
                    if side == 'b':
                        side = '0'
                    else: 
                        side = '1'                    
                    break
                else:
                    bp+=char
                c += 1
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
            factor_1 = vertical_control.vertical_count(matrix)
            factor_2 = central_effect.central_effect(matrix)
            factor_3 = diag_control.total_control(matrix)
            factor_4 = adv_knights.knight_count(matrix)
            factor_5 = space.pawn_space(matrix)
            factor_6 = material_count.material_count(matrix)
            factor_7 = total_effect.total_effect(matrix)  
            data = [row_array[0],row_array[1],str(factor_1),str(factor_2),str(factor_3),str(factor_4),str(factor_5),str(factor_6),str(factor_7),side]
            writer.writerow(data)
            # break

