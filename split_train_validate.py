import csv

in_path  = "filtered_lichess/eval_db_processed.csv"
out_train = "filtered_lichess/eval_db_filtered_train[3].csv"
out_validate = "filtered_lichess/eval_db_filtered_validate[3].csv"

rows_written = 0

with open(in_path, "r", encoding="utf-8") as fin:
    reader = csv.reader(fin)
    headers = next(reader)  # Skip header line

    with open(out_train, "w", newline="", encoding="utf-8") as fout:
        with open(out_validate, "w", newline="", encoding="utf-8") as fout_:
            w = csv.writer(fout)
            w_ = csv.writer(fout_)

            # Headers: first and third columns named as requested ("FEN" and "side")
            w.writerow(["FEN", "cp", "Factor_1", "Factor_2", "Factor_3", "Factor_4", "Factor_5", "Factor_6", "Factor_7", "side"])
            w_.writerow(["FEN", "cp", "Factor_1", "Factor_2", "Factor_3", "Factor_4", "Factor_5", "Factor_6", "Factor_7", "side"])

            for line in reader:
                ID = line[0]
                cp = line[1]
                Factor_1 = line[2]
                Factor_2 = line[3]
                Factor_3 = line[4]
                Factor_4 = line[5]
                Factor_5 = line[6]
                Factor_6 = line[7]
                Factor_7 = line[8]
                side = line[9]

                if rows_written > 17146 and rows_written < 34292:
                    w_.writerow([ID, cp, Factor_1, Factor_2, Factor_3, Factor_4, Factor_5, Factor_6, Factor_7, side])
                else:
                    w.writerow([ID, cp, Factor_1, Factor_2, Factor_3, Factor_4, Factor_5, Factor_6, Factor_7, side])

                rows_written += 1

print(f"Rows written: {rows_written}")
