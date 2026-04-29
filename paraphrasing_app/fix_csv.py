import csv
import os

# -------------------------------
# SET PROJECT PATH (AUTO)
# -------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))

input_path = os.path.join(base_dir, "data.csv")
output_path = os.path.join(base_dir, "clean_data.csv")

fixed_rows = []
seen = set()

# -------------------------------
# READ FILE SAFELY
# -------------------------------
with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# -------------------------------
# CLEAN DATA
# -------------------------------
for line in lines:
    try:
        row = list(csv.reader([line]))[0]

        # Must have exactly 3 columns
        if len(row) != 3:
            continue

        inp, out, quality = row

        inp = inp.strip()
        out = out.strip()
        quality = quality.strip().lower()

        # Skip empty
        if not inp or not out:
            continue

        # Skip duplicate rows
        if (inp, out) in seen:
            continue
        seen.add((inp, out))

        # Skip identical input-output (VERY IMPORTANT)
        if inp.lower() == out.lower():
            continue

        # Skip weak outputs
        if len(out.split()) < 6:
            continue

        # Optional: keep only good + unrated
        if quality not in ["good", "unrated"]:
            quality = "unrated"

        fixed_rows.append([inp, out, quality])

    except:
        continue

# -------------------------------
# SAVE CLEAN FILE (INSIDE PROJECT)
# -------------------------------
with open(output_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Input", "Output", "Quality"])
    writer.writerows(fixed_rows)

# -------------------------------
# DEBUG INFO
# -------------------------------
print("✅ CSV fixed successfully")
print(f"📁 Saved at: {output_path}")
print(f"📊 Total clean rows: {len(fixed_rows)}")