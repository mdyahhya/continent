with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = list(re.finditer(r'(loader|loading|spinner|preloader)', content, re.IGNORECASE))
print(f"Found {len(matches)} matches")
for m in matches[:10]:
    start = max(0, m.start() - 100)
    end = min(len(content), m.end() + 150)
    print(f"Match at {m.start()}: {repr(content[start:end])}")
