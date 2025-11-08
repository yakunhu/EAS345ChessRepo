import json
import csv

in_path  = "filtered_lichess/a_milli_positions.jsonl"
out_path = "filtered_lichess/eval_db_filtered.csv"

rows_written = 0

with open(in_path, "r", encoding="utf-8") as fin, \
     open(out_path, "w", newline="", encoding="utf-8") as fout:

    w = csv.writer(fout)
    # Headers: first and third columns named as requested ("FEN" and "side")
    w.writerow(["FEN", "max_cp", "side"])

    for line in fin:
        line = line.strip()
        if not line:
            continue

        obj = json.loads(line)
        fen = obj.get("fen", "")
        evals = obj.get("evals", []) or []

        # Collect all cp values across all evals/pvs for this FEN
        cps = []
        for ev in evals:
            for pv in (ev.get("pvs") or []):
                cp = pv.get("cp", None)
                if isinstance(cp, (int, float)):
                    cps.append(int(cp))

        if not cps:
            continue

        # Filter to those with |cp| > 300
        big_cps = [cp for cp in cps if abs(cp) > 300 and abs(cp) < 750]

        # Require at least TWO such cps
        if len(big_cps) < 3:
            continue

        # Pick the cp with the largest absolute value (keep the sign)
        max_abs_cp_signed = max(big_cps, key=lambda v: abs(v))

        # Determine side: 'w' if positive, 'b' if negative
        side = "w" if max_abs_cp_signed > 0 else "b"

        w.writerow([fen, max_abs_cp_signed, side])
        rows_written += 1

print(f"Rows written: {rows_written}")
