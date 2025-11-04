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

    # for "#"
    if len(parts) == 1:
        line = parts[0]
        m = re.match(r'^(#{1,6})\s+(.+?)\s*$', line)
        if not m:
            return text
        level = len(m.group(1))
        body = m.group(2)
        return f"<h{level}>{body}</h{level}>"

    # for "==" or "--"
    if len(parts) == 2:
        title, underline = parts[0], parts[1]
        if title.strip():
            if re.match(r'^\s*={2,}\s*$', underline):
                return f"<h1>{title.strip()}</h1>"
            if re.match(r'^\s*-{2,}\s*$', underline):
                return f"<h2>{title.strip()}</h2>"
        return text

    return None

def convert_unordered_list(text: str) -> str:
    lines = text.split('\n')
    result = "<ul>\n"
    
    # Loop through all lines
    for line in lines:
        # Skip the initial "+ ", "- ", or "* "
        list_item = line[2:]
        # Wrap in <li> tags
        result += "  <li>" + list_item + "</li>\n"
    
    result += "</ul>"
    return result

def convert_ordered_list(text: str) -> str:
    lines = text.split('\n')
    result = "<ol>\n"
    
    # Loop through all lines
    for line in lines:
        # Skip the initial "1. ", "2. ", or "3. "
        list_item = line[3:]
        # Wrap in <li> tags
        result += "  <li>" + list_item + "</li>\n"
    
    result += "</ol>"
    return result

def convert_code(text: str) -> str:
    # double backticks: ``code``
    text = re.sub(r'``([^`\n]+)``', r'<code>\1</code>', text)
    # single backticks: `code`
    text = re.sub(r'`([^`\n]+)`', r'<code>\1</code>', text)
    return text

def convert_link(text: str) -> str:
    # Parsing [label](url) 
    pattern = r'\[([^\]]+)\]\(([^)\s]+)\)'
    replacement = r'<a href="\2">\1</a>'
    # Do the substitution
    result = re.sub(pattern, replacement, text)
    return result