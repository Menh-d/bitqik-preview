import re

original_path = "/Users/graphic/Desktop/bitqik/Artwork/Website/Web test/Home - bitqik - We make crypto easy.html"

with open(original_path, 'r', encoding='utf-8') as f:
    orig_html = f.read()

missing_ids = [
    "SR7_1_1",
    "cz_102453",
    "cz_103992",
    "cz_16115",
    "cz_25448",
    "cz_79829",
    "cz_93492"
]

print("--- Inspecting missing IDs in original HTML ---")
for id_val in missing_ids:
    # Let's find the start tag with this id
    pattern = rf'<[^>]*\bid=["\']{id_val}["\'][^>]*>'
    matches = list(re.finditer(pattern, orig_html))
    print(f"\nID: {id_val}")
    if matches:
        for match in matches:
            start_pos = match.start()
            # print surrounding 500 characters
            end_print = min(start_pos + 600, len(orig_html))
            print(f"Start Tag Match: {match.group(0)}")
            print("Content:")
            print(orig_html[start_pos:end_print])
    else:
        print("No start tag match found.")
