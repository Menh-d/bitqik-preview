import re

ocr_path = "/Users/graphic/.gemini/antigravity/scratch/bitqik-home/all_parts_ocr.txt"
desktop_html_path = "/Users/graphic/Desktop/bitqik/Artwork/Website/Web test/Home - bitqik - We make crypto easy.html"

with open(ocr_path, 'r', encoding='utf-8') as f:
    ocr_lines = f.readlines()

with open(desktop_html_path, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Let's clean the HTML content (remove tags) to do plain text comparisons
# We replace HTML tags with spaces so we don't accidentally join words
text_only_html = re.sub(r'<[^>]+>', ' ', html_content)
# Clean multiple spaces
text_only_html = re.sub(r'\s+', ' ', text_only_html).lower()

print("--- Checking OCR phrases against original Desktop HTML ---")
missing_phrases = []

for line in ocr_lines:
    # Format: [x, y, w, h]: text or part markers
    if line.startswith("==="):
        continue
    
    match = re.match(r'^\[.*\]:\s*(.*)$', line.strip())
    if match:
        phrase = match.group(1).strip()
        # Skip small/short strings
        if not phrase or len(phrase) < 5:
            continue
        
        # Clean the OCR phrase for comparison (lowercase, basic cleaning)
        clean_phrase = phrase.lower()
        # Remove common OCR noise
        clean_phrase = re.sub(r'[^\w\s]', '', clean_phrase).strip()
        
        if not clean_phrase or len(clean_phrase) < 5:
            continue
            
        # Check if clean_phrase is in text_only_html
        if clean_phrase not in text_only_html:
            # Let's check if a word from the phrase is present to see if it's just OCR typo
            words = clean_phrase.split()
            # If all major words are not in html, then it's probably missing
            matching_words = [w for w in words if len(w) > 3 and w in text_only_html]
            if len(matching_words) == 0:
                print(f"MISSING: {phrase}")
                missing_phrases.append(phrase)

print(f"\nTotal completely missing phrases: {len(missing_phrases)}")
