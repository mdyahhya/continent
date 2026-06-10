import html.parser

class StackTracker(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.found_stack_path = None
        self.errors = []

    def handle_starttag(self, tag, attrs):
        self_closing = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 
                        'link', 'meta', 'param', 'source', 'track', 'wbr'}
        attrs_dict = dict(attrs)
        class_val = attrs_dict.get('class', '')
        id_val = attrs_dict.get('id', '')
        tag_desc = f"{tag}"
        if class_val:
            tag_desc += f".{class_val.replace(' ', '.')}"
        if id_val:
            tag_desc += f"#{id_val}"
            
        if tag not in self_closing:
            self.stack.append((tag_desc, self.getpos()))
            if 'fixed-contact-stack' in class_val:
                self.found_stack_path = [t[0] for t in self.stack]

    def handle_endtag(self, tag):
        self_closing = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 
                        'link', 'meta', 'param', 'source', 'track', 'wbr'}
        if tag in self_closing:
            return
        if not self.stack:
            self.errors.append(f"Unexpected end tag </{tag}> at line {self.getpos()[0]}")
            return
        expected_tag, pos = self.stack.pop()
        expected_tag_name = expected_tag.split('.')[0].split('#')[0]
        if expected_tag_name != tag:
            self.errors.append(f"Mismatched tag: expected </{expected_tag_name}> (opened at line {pos[0]}), but found </{tag}> at line {self.getpos()[0]}")
            self.stack.append((expected_tag, pos))

tracker = StackTracker()
with open('index.html', 'r', encoding='utf-8') as f:
    tracker.feed(f.read())

if tracker.found_stack_path:
    print("PATH TO FIXED CONTACT STACK:")
    print(" -> ".join(tracker.found_stack_path))
else:
    print("fixed-contact-stack not found in HTML!")

if tracker.errors:
    print("\nTAG ERRORS:")
    for err in tracker.errors[:10]:
        print(err)
