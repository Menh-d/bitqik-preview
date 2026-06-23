import re
from html.parser import HTMLParser
import os

class ImageSrcParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.img_sources = []
        self.style_bg_images = []
        
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            for name, value in attrs:
                if name == 'src':
                    self.img_sources.append(value)
        for name, value in attrs:
            if name == 'style':
                bg_match = re.search(r'background(?:-image)?\s*:\s*url\(([^)]+)\)', value, re.IGNORECASE)
                if bg_match:
                    self.style_bg_images.append(bg_match.group(1).strip('\'" '))

html_files = [
    "index.html",
    "About Us - bitqik - We make crypto easy.html",
    "Careers - bitqik - We make crypto easy.html",
    "Download - bitqik - We make crypto easy.html"
]

base_dir = "/Users/graphic/.gemini/antigravity/scratch/bitqik-home"

for html_file in html_files:
    path = os.path.join(base_dir, html_file)
    if not os.path.exists(path):
        print(f"File not found: {html_file}")
        continue
        
    print(f"\n================ INSPECTING {html_file} ================")
    with open(path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    parser = ImageSrcParser()
    parser.feed(html_content)
    
    print("--- <img> sources ---")
    for src in sorted(list(set(parser.img_sources))):
        clean_src = src.split('?')[0].split('#')[0]
        if clean_src.startswith('data:'):
            continue
            
        if clean_src.startswith('http://') or clean_src.startswith('https://'):
            print(f"[REMOTE] {src}")
        else:
            local_path = os.path.join(base_dir, clean_src)
            import urllib.parse
            local_path_decoded = urllib.parse.unquote(local_path)
            
            # Remove escapes like \ in url
            local_path_decoded = local_path_decoded.replace('\\ ', ' ').replace('\\', '')
            local_path = local_path.replace('\\ ', ' ').replace('\\', '')
            
            if os.path.exists(local_path_decoded) or os.path.exists(local_path):
                print(f"[OK] {src}")
            else:
                print(f"[BROKEN] {src} (Checked: {local_path_decoded})")
                
    print("\n--- Inline background images ---")
    for bg in sorted(list(set(parser.style_bg_images))):
        clean_bg = bg.split('?')[0].split('#')[0]
        if clean_bg.startswith('http://') or clean_bg.startswith('https://'):
            print(f"[REMOTE] {bg}")
        else:
            local_path = os.path.join(base_dir, clean_bg)
            import urllib.parse
            local_path_decoded = urllib.parse.unquote(local_path)
            local_path_decoded = local_path_decoded.replace('\\ ', ' ').replace('\\', '')
            local_path = local_path.replace('\\ ', ' ').replace('\\', '')
            
            if os.path.exists(local_path_decoded) or os.path.exists(local_path):
                print(f"[OK] {bg}")
            else:
                print(f"[BROKEN] {bg} (Checked: {local_path_decoded})")
