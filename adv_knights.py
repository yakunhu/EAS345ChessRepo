def knight_count(matrix):
    """
    Count knights (N/n) only on rows 2–5 (0-indexed).
    """
    w_E = 0
    b_E = 0

    # White: rows 2, 3
    for i in (2, 3):
        for j in range(8):
            if matrix[i][j] == "N":
                w_E += 1

    # Black: rows 4, 5
    for i in (4, 5):
        for j in range(8):
            if matrix[i][j] == "n":
                b_E += 1

    print(w_E)
    print(b_E)
    return w_E - b_E