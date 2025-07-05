import json

with open("normalHasla.json", "r", encoding="utf-8") as f:
    data = json.load(f)

unique = {}
resolved = set()
output = []

for entry in data:
    tekst = entry["tekst"]
    kat = entry["kategoria"]

    if tekst not in unique:
        unique[tekst] = [entry]
    else:
        unique[tekst].append(entry)

for tekst, entries in unique.items():
    if tekst in resolved:
        continue
    if len(entries) == 1:
        output.append(entries[0])
        resolved.add(tekst)
    else:
        categories = [e["kategoria"] for e in entries]
        if all(cat == categories[0] for cat in categories):
            output.append(entries[0])
        else:
            print(f"\nDuplicate found: \"{tekst}\"")
            for i, e in enumerate(entries):
                print(f"{i + 1}: {e['tekst']} ({e['kategoria']})")
            print("X: Keep all")
            choice = input("Which to keep (e.g. 1 3 or X): ").strip().upper()

            if choice == "X":
                output.extend(entries)
            else:
                try:
                    indices = [int(c) - 1 for c in choice.split() if c.isdigit()]
                    selected = [entries[i] for i in indices if 0 <= i < len(entries)]
                    output.extend(selected)
                except Exception as e:
                    print("Invalid input, skipping.")

        resolved.add(tekst)

with open("normalHasla.json", "w", encoding="utf-8") as f:
    f.write("[\n")
    for i, item in enumerate(output):
        line = json.dumps(item, ensure_ascii=False)
        f.write("  " + line + (",\n" if i < len(output) - 1 else "\n"))
    f.write("]\n")
