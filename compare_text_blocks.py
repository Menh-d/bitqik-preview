import re
from html.parser import HTMLParser

class TextBlockParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.current_block = []
        self.in_script_or_style = False
        
    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style']:
            self.in_script_or_style = True
        # Block level tags reset current block
        if tag in ['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'section', 'li', 'ul', 'ol']:
            self.flush()

    def handle_endtag(self, tag):
        if tag in ['script', 'style']:
            self.in_script_or_style = False
        if tag in ['div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'section', 'li', 'ul', 'ol']:
            self.flush()

    def handle_data(self, data):
        if not self.in_script_or_style:
            text = data.strip()
            if text:
                self.current_block.append(text)
                
    def flush(self):
        if self.current_block:
            block_text = " ".join(self.current_block).strip()
            # Clean up whitespace
            block_text = re.sub(r'\s+', ' ', block_text)
            if block_text and len(block_text) > 3:
                self.blocks.append(block_text)
            self.current_block = []

original_path = "/Users/graphic/Desktop/bitqik/Artwork/Website/Web test/Home - bitqik - We make crypto easy.html"
modified_path = "/Users/graphic/.gemini/antigravity/scratch/bitqik-home/index.html"

with open(original_path, 'r', encoding='utf-8') as f:
    orig_html = f.read()

with open(modified_path, 'r', encoding='utf-8') as f:
    mod_html = f.read()

parser_orig = TextBlockParser()
parser_orig.feed(orig_html)
parser_orig.flush()

parser_mod = TextBlockParser()
parser_mod.feed(mod_html)
parser_mod.flush()

orig_blocks = parser_orig.blocks
mod_blocks = parser_mod.blocks

print(f"Original text blocks count: {len(orig_blocks)}")
print(f"Modified text blocks count: {len(mod_blocks)}")

print("\n--- Text blocks in Original but NOT in Modified (using substring matching) ---")
missing_count = 0
for block in orig_blocks:
    # See if it's in modified blocks (fuzzy match)
    found = False
    block_lower = block.lower()
    for m_block in mod_blocks:
        if block_lower in m_block.lower() or m_block.lower() in block_lower:
            found = True
            break
    if not found:
        # Also check if it's in raw modified HTML
        if block_lower not in mod_html.lower():
            print(f"- {block}")
            missing_count += 1

print(f"\nTotal missing text blocks: {missing_count}")
