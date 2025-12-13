import numpy as np
import csv
from matrix_convert_helpers import (
    total_effect,
    central_effect,
    diag_control,
    vertical_control,
    material_count,
    space,
    adv_knights
)

file_path = "filtered_lichess/eval_db_filtered.csv"
with open(file_path, 'r') as file:
    lines = file.readlines()[1:]
    with open("filtered_lichess/eval_db_processed.csv", mode="w",newline='',encoding='utf-8') as out_file:
        writer = csv.writer(out_file)
        header = ["ID","FEN","1","2","3","4","5","6","7","side"]
        writer.writerow(header)
        # row_num = 0
        for row in lines:
            # if row_num == 0:
                # row_num += 1
                # continue
            row_array = row.split(',')
            FEN = row_array[0]
            bp = ""
            for i, char in enumerate(FEN):
                if char=='"':
                    continue
                elif char == " ":
                    # side = FEN[i+1]
                    side = row_array[2]
                    side = side.replace('"','').strip()
                    # print("Side = " + side)
                    if side == 'b':
                        side = '0' # reverse the side to move for Puzzle FENs
                    else: 
                        side = '1'                    
                    break
                else:
                    bp+=char
            print(bp)
            bp = bp.split('/')
            # print(bp)
            print(bp[0])
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
            print(matrix)
            factor_1 = vertical_control.vertical_count(matrix)
            factor_2 = central_effect.central_effect(matrix)
            factor_3 = diag_control.total_control(matrix)
            factor_4 = adv_knights.knight_count(matrix)
            factor_5 = space.pawn_space(matrix)
            factor_6 = material_count.material_count(matrix)
            if factor_6 == None:
                continue
            factor_7 = total_effect.total_effect(matrix)  
            data = [row_array[0],row_array[1],str(factor_1),str(factor_2),str(factor_3),str(factor_4),str(factor_5),str(factor_6),str(factor_7),side]
            writer.writerow(data)
            print("Factor 1:", factor_1)
            print("Factor 2:", factor_2)
            print("Factor 3:", factor_3)
            print("Factor 4:", factor_4)
            print("Factor 5:", factor_5)
            print("Factor 6:", factor_6)
            print("Factor 7:", factor_7)
            # break

