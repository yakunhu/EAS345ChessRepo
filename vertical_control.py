import numpy as np

def is_enemy(piece, target):
    """
    Return True if 'target' is an enemy of 'piece' based on case.
    Uppercase = White, lowercase = Black.
    """
    if target == "":
        return False
    return (piece.isupper() and target.islower()) or (piece.islower() and target.isupper())


def QR_vertical_spaces(coords, matrix):
    """
    Count vertical squares (up/down) for a queen or rook, including enemy capture squares
    and excluding friendly blockers.
    """
    r, c = coords
    piece = matrix[r, c]
    # if piece not in ("Q", "q", "R", "r"):
    #     return 0

    total = 0
    for dr in (-1, 1):  # scan up and down
        rr = r + dr
        while 0 <= rr <= 7:
            target = matrix[rr, c]
            if target == "":
                total += 1
                rr += dr
                continue
            if is_enemy(piece, target):
                total += 1
            break  # stop on first occupied square
    return total


def vertical_count(matrix):
    """
    Calculates total vertical mobility advantage (White - Black)
    for all queens and rooks on the board.

    Returns:
        > 0  => White advantage
        < 0  => Black advantage
        = 0  => Balanced
    """
    w_E = 0
    b_E = 0
    i = 0
    while i < 8:
        j = 0
        while j < 8:
            current = matrix[i, j]
            if current in ("Q", "q", "R", "r"):
                coords = np.array([i, j])
                spaces = QR_vertical_spaces(coords, matrix)
                if current.isupper():
                    w_E += spaces
                else:
                    b_E += spaces
            j += 1
        i += 1
    return w_E - b_E
# Why are we only making it for vertical spaces and not for horizontal spaces /diagonal spaces /other pieces?