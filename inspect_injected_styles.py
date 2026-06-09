import re

files = ["index.html", "founder.html", "hosting.html", "projects.html", "startups.html"]
for f_name in files:
    with open(f_name, "r", encoding="utf-8") as f:
        content = f.read()
    
    print(f"=== File: {f_name} ===")
    
    # Let's print style tags count and length of each style block
    styles = re.findall(r'<style>(.*?)</style>', content, re.DOTALL)
    print(f"Found {len(styles)} style block(s)")
    for i, s in enumerate(styles):
        print(f"  Block {i+1} length: {len(s)} chars")
        # Check if there is any mention of red or color codes
        red_mentions = [line for line in s.splitlines() if "red" in line.lower() or "#ff" in line.lower() or "#f00" in line.lower()]
        if red_mentions:
            print("  Red mentions in block:")
            for rm in red_mentions:
                print("    -", rm.strip())
                
    # Check if there are any unclosed style tags or tags out of order
    style_opens = len(re.findall(r'<style>', content, re.IGNORECASE))
    style_closes = len(re.findall(r'</style>', content, re.IGNORECASE))
    print(f"style open tags: {style_opens}, close tags: {style_closes}")
    
    body_opens = len(re.findall(r'<body>', content, re.IGNORECASE))
    body_closes = len(re.findall(r'</body>', content, re.IGNORECASE))
    print(f"body open tags: {body_opens}, close tags: {body_closes}")
    print("-" * 50)
