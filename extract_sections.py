import re

with open("index.html", "r", encoding="utf-8") as f:
    content = f.read()

# Products in Action is:
# <section id="products-action" or similar, let's find the section tag
# It starts around character 71500. Let's find the surrounding <section> block
matches_section = re.finditer(r'<section\b[^>]*>', content)
sections = []
for m in matches_section:
    sections.append(m.start())

# Let's see which section covers 71676
# Let's find section details
def get_section_at_pos(pos):
    # Find the start tag just before pos
    start_pos = None
    for s in sections:
        if s <= pos:
            start_pos = s
        else:
            break
    # Find the matching </section>
    # We can do a simple balance or search for next </section>
    end_match = re.search(r'</section>', content[pos:])
    if end_match:
        end_pos = pos + end_match.end()
        return content[start_pos:end_pos]
    return None

print("--- PRODUCTS IN ACTION SECTION ---")
prod_sec = get_section_at_pos(71676)
if prod_sec:
    print(prod_sec[:1000] + "\n...\n" + prod_sec[-500:])
else:
    print("Not found")

print("\n--- OUR EXPERTISE SECTION ---")
exp_sec = get_section_at_pos(79429)
if exp_sec:
    print(exp_sec[:1000] + "\n...\n" + exp_sec[-500:])
else:
    print("Not found")

# Let's search style declarations for ad-stage, browser-mock, speed-badge, etc.
css_matches = re.findall(r'/\* =+ Products in Action =+ \*/(.*?)/\*', content, re.DOTALL | re.IGNORECASE)
if css_matches:
    print("\n--- PRODUCTS IN ACTION CSS ---")
    print(css_matches[0][:800] + "\n...\n")
else:
    # Try custom search
    styles = re.findall(r'\.ad-stage.*?\}', content, re.DOTALL)
    if styles:
        print("\n--- FOUND AD-STAGE CSS ---")
        print(styles[0])

# Let's check for scripts relating to products-action/slideshow
js_matches = re.findall(r'// Products in Action.*?//', content, re.DOTALL | re.IGNORECASE)
if js_matches:
    print("\n--- PRODUCTS IN ACTION JS ---")
    print(js_matches[0])
