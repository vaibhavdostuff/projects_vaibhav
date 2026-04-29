import csv

fixed_rows = []

with open(r"E:\GithubA\projects_vaibhav\paraphrasing_app\data.csv", "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

for line in lines:
    try:
        row = list(csv.reader([line]))[0]

        if len(row) != 3:
            continue

        inp, out, quality = row

        if not inp or not out:
            continue

        fixed_rows.append([inp.strip(), out.strip(), quality.strip()])

    except:
        continue

with open("clean_data.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Input", "Output", "Quality"])
    writer.writerows(fixed_rows)

print("CSV fixed ✅ Use clean_data.csv")