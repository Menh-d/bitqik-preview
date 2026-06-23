from html.parser import HTMLParser

class IDParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
    
    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name == 'id' and value:
                self.ids.append(value)

original_path = "/Users/graphic/Desktop/bitqik/Artwork/Website/Web test/Home - bitqik - We make crypto easy.html"
modified_path = "/Users/graphic/.gemini/antigravity/scratch/bitqik-home/index.html"

with open(original_path, 'r', encoding='utf-8') as f:
    orig_html = f.read()

with open(modified_path, 'r', encoding='utf-8') as f:
    mod_html = f.read()

parser_orig = IDParser()
parser_orig.feed(orig_html)

parser_mod = IDParser()
parser_mod.feed(mod_html)

orig_ids = parser_orig.ids
mod_ids = parser_mod.ids

print(f"Original IDs count: {len(orig_ids)} (unique: {len(set(orig_ids))})")
print(f"Modified IDs count: {len(mod_ids)} (unique: {len(set(mod_ids))})")

print("\n--- IDs in Original but NOT in Modified ---")
missing_ids = sorted(list(set(orig_ids) - set(mod_ids)))
for id_val in missing_ids:
    print(id_val)

print("\n--- IDs in Modified but NOT in Original ---")
new_ids = sorted(list(set(mod_ids) - set(orig_ids)))
for id_val in new_ids:
    print(id_val)
