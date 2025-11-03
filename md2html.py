import re

def convert_emphasis(text: str) -> str:
  text = re.sub(r'\b___([^_]+)___\b', r'<em><strong>\1</strong></em>', text)
  text = re.sub(r'\*\*\*([^*]+)\*\*\*', r'<em><strong>\1</strong></em>', text)
  text = re.sub(r'\b__([^_]+)__\b', r'<strong>\1</strong>', text)
  text = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)
  text = re.sub(r'\b_([^_]+)_\b', r'<em>\1</em>', text)
  text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
  return text;


def convert_paragraph(text: str) -> str:
  text = re.sub(r'\n', r'<br>', text)
  return f'<p>{text}</p>'

def convert_headings(text: str) -> str:
    parts = text.split("\n")

    # ATX: "# ...", "## ...", up to "###### ..."
    if len(parts) == 1:
        line = parts[0]
        m = re.match(r'^(#{1,6})\s+(.+?)\s*$', line)
        if not m:
            return text
        level = len(m.group(1))
        body = m.group(2)
        return f"<h{level}>{body}</h{level}>"

    # Setext: "Title" + underline of ===... (H1) or ---... (H2)
    if len(parts) == 2:
        title, underline = parts[0].rstrip(), parts[1]
        if title.strip():
            if re.match(r'^\s*={2,}\s*$', underline):
                return f"<h1>{title.strip()}</h1>"
            if re.match(r'^\s*-{2,}\s*$', underline):
                return f"<h2>{title.strip()}</h2>"
        return text

   
    return None