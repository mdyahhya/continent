import re
import os

files = ["index.html", "founder.html", "hosting.html", "projects.html", "startups.html", "about.html", "services.html"]

for f_name in files:
    if not os.path.exists(f_name):
        continue
    with open(f_name, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Let's search for "active" in the styles
    style_matches = re.finditer(r'<style>(.*?)</style>', content, re.DOTALL)
    for idx, sm in enumerate(style_matches):
        style_content = sm.group(1)
        if "active" in style_content:
            print(f"Found 'active' in style block {idx+1} of {f_name}")
            # Find lines containing active
            for line in style_content.splitlines():
                if "active" in line:
                    print("  -", line.strip())
        
        # Search for color names or hex codes in styles
        for color in ["red", "#f00", "#ff0000"]:
            if color in style_content.lower():
                print(f"Found color '{color}' in style block {idx+1} of {f_name}")
