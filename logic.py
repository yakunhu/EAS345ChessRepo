import numpy as np
import math
import total_effect
import central_effect
import diag_control
import vertical_control
import material_count
import space
import adv_knights


def fen_to_matrix(fen):
# Take only the board part (everything before the first space)
    board_part = ""
    for ch in fen:
        if ch == " ":
            break
        board_part += ch

    ranks = board_part.split('/')

    matrix = np.empty((8,8), dtype=str)

    i = 0
    for rank in ranks:
        j = 0
        for sq in rank:
            if sq.isdigit():
                j += int(sq)-1
            else:
                matrix[i, j] = sq
                j += 1
        i += 1

    # Fill any remaining empty entries with ''
    #matrix[matrix == None] = ''
    return matrix

def analyze_fen(fen):
    try:
        matrix = fen_to_matrix(fen)
    except Exception as e:
        raise ValueError(f"Invalid FEN or parsing error: {e}")

    # compute factors using your functions
    factor_1 = vertical_control.vertical_count(matrix)
    factor_2 = central_effect.central_effect(matrix)
    factor_3 = diag_control.total_control(matrix)
    factor_4 = adv_knights.knight_count(matrix)
    factor_5 = space.pawn_space(matrix)
    factor_6 = material_count.material_count(matrix)
    factor_7 = total_effect.total_effect(matrix)  

    factors = [factor_1, factor_2, factor_3, factor_4, factor_5, factor_6, factor_7]
    
    factors_info = [
    {"name": "Vertical effect of rooks and queens", "value": factor_1 },
    {"name": "Total effect on the 4 central squares", "value": factor_2},
    {"name": "Diagnol effect of bishops and queens", "value": factor_3},
    {"name": "Knights on the 5th and 6th ranks", "value": factor_4},
    {"name": "Diffrence between a pawn's current rank of occupation and it's starting rank", "value": factor_5},
    {"name": "Material Count", "value": factor_6},
    {"name": "Total effect on pieces, attack and defense", "value": factor_7},]

    logit = (0.448497 + factor_1 * 0.167184 + factor_2 * 0.028319 + factor_3 * 0.137382
         + factor_4 * 1.208941 + factor_5 * 0.107188 + factor_6 * 0.393939
         + factor_7 * 0.141307)
    odds = math.exp(logit)
    prob_white = odds / (1 + odds)
    prob_black = 1 - prob_white


    return {
        "factors_info": factors_info,
        "prob_black": round(prob_black * 100, 2),
        "prob_white": round(prob_white * 100, 2),
    }

