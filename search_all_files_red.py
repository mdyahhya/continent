import re
import os

files_to_check = []
for root, dirs, files in os.walk('.'):
    # Exclude .git and .gemini dirs
    if '.git' in root or '.gemini' in root or 'node_modules' in root:
        continue
    for file in files:
        if file.endswith(('.html', '.css')):
            files_to_check.append(os.path.join(root, file))

red_hex_patterns = [
    r'#ef4444', r'#f87171', r'#dc2626', r'#b91c1c', r'#991b1b', r'#7f1d1d',
    r'#fca5a5', r'#fecaca', r'#fee2e2', r'#e11d48', r'#f43f5e', r'#be123c', r'#9f1239', r'#e11d48'
]

red_names = ['red', 'crimson', 'coral', 'firebrick', 'darkred', 'tomato', 'orangered']

print(f"Checking {len(files_to_check)} files...")
for file_path in files_to_check:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        # try fallback encoding
        try:
            with open(file_path, "r", encoding="latin-1") as f:
                content = f.read()
        except:
            continue
            
    # Search for styles/color rules
    # We'll search for 'red' names
    for rn in red_names:
        for m in re.finditer(r'\b' + rn + r'\b', content, re.IGNORECASE):
            # Only match if it's inside style or css
            start = max(0, m.start() - 40)
            end = min(len(content), m.end() + 40)
            print(f"RED NAME '{rn}' found in {file_path} (char {m.start()}): {repr(content[start:end])}")
            
    # Search for patterns
    for pat in red_hex_patterns:
        for m in re.finditer(pat, content, re.IGNORECASE):
            start = max(0, m.start() - 40)
            end = min(len(content), m.end() + 40)
            print(f"RED HEX '{pat}' found in {file_path} (char {m.start()}): {repr(content[start:end])}")
            
    # Search for rgb/rgba with red dominance
    rgb_matches = re.finditer(r'rgba?\((\d+)\s*,\s*(\d+)\s*,\s*(\d+)(?:\s*,\s*[\d.]+)?\)', content, re.IGNORECASE)
    for m in rgb_matches:
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if r > 180 and g < 80 and b < 80:
            start = max(0, m.start() - 40)
            end = min(len(content), m.end() + 40)
            print(f"RED RGB ({r},{g},{b}) found in {file_path} (char {m.start()}): {repr(content[start:end])}")
