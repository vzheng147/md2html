import re
import sys
from pathlib import Path


# DETECTOR FUNCTIONS

def is_heading(block: str) -> bool:
    lines = block.split('\n')

    # For "#", up to 6
    if len(lines) == 1:
        s = lines[0]
        if not s or s[0] != '#':
            return False
        # count leading #
        i = 0
        while i < len(s) and s[i] == '#':
            i += 1
        if i == 0 or i > 6:
            return False
        # must have a space after the leading #s
        if i >= len(s) or s[i] != ' ':
            return False
        # must have some text after that space
        return s[i+1:].strip() != ""

    # "====" H1 or "----" H2
    if len(lines) == 2:
        text = lines[0].strip()
        symbols = lines[1].strip()
        if not text or text == "": # text is empty
            return False
        if len(symbols) >= 2:
            ch = symbols[0]
            if ch not in ('=', '-'):
                return False
            # must be the same symbol
            for c in symbols:
                if c != ch:
                    return False
            return True
    return False


def is_ordered_list(block: str) -> bool:
    lines = [l.strip() for l in block.split('\n') if l.strip() != ""]
    if not lines:
        return False

    def parse(s):
        # read leading digits
        i = 0
        while i < len(s) and s[i].isdigit():
            i += 1
        if i == 0:
            return False
        # must be ". " after the number
        if i + 1 >= len(s) or s[i] != '.' or s[i + 1] != ' ':
            return False
        content = s[i + 2:].strip()
        if content == "":
            return False
        return True
    # check every line
    for line in lines:
        if parse(line) == False:
            return False
    
    # must start at 1.
    string_0 = lines[0]
    j = 0
    while j < len(string_0) and string_0[j].isdigit():
        j += 1
    if j == 0 or int(string_0[:j]) != 1:
        return False
    
    return True


def is_unordered_list(block: str) -> bool:
    lines = [l.strip() for l in block.split('\n') if l.strip() != ""]
    if not lines:
        return False

    def parse(line):
        s = line.strip()
        if len(s) < 3:
            return False
        if s[0] in {'-', '*', '+'} and s[1] == ' ':
            return s[2:].strip() != ""
        # content is not empty, after the initial signs
        return False
            
    for line in lines:
        if parse(line) == False:
            return False
    return True


def detect_element(block: str) -> str:
    """
    Returns one of: "heading", "ordered_list", "unordered_list", "paragraph".
    Assumes 'block' contains no blank-line separators (i.e., already chunked).
    """
    if is_heading(block):
        return "heading"
    if is_ordered_list(block):
        return "ordered_list"
    if is_unordered_list(block):
        return "unordered_list"
    return "paragraph"


# CONVERTING FUNCTIONS
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

    return text

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
    
    first_item = 1
    # Loop through all lines
    for line in lines:
        # Skip the initial number
        i = 0
        while i < len(line) and line[i].isdigit():
            i += 1

        content = line[i+2:]
        # Wrap in <li> tags
        result += "  <li>" + content + "</li>\n"
    
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

def convert(text: str) -> str:

    # 1) split into blocks on blank lines
    blocks = re.split(r'\n\s*\n+', text) if text else []

    # 2) parse every block as an HTML element
    html_parts = []
    for block in blocks:
        # 3) Inline conversions first
        inline = convert_code(block)
        inline = convert_link(inline)
        inline = convert_emphasis(inline)

        # 4) Detect using the original block
        type = detect_element(block)

        # 5) Convert based on the element type
        if type == "heading":
            html_parts.append(convert_headings(inline))
        elif type == "ordered_list":
            html_parts.append(convert_ordered_list(inline))
        elif type == "unordered_list":
            html_parts.append(convert_unordered_list(inline))
        else:  # anything else is a paragraph
            html_parts.append(convert_paragraph(inline))

    # 6) join blocks with a blank line for readability
    return "\n\n".join(html_parts)


# MAIN FUNCTION

def main() -> None:
    args_arr = sys.argv[1:]
    # check input length
    if len(args_arr) not in {1, 2}:
        print("usage: python md2html.py <input.md> [output.html]")
        sys.exit(1)
    # check if input file exists
    input_file = Path(args_arr[0])
    if not input_file.exists():
        sys.stderr.write("Error: Input must be an existing .md file")
        sys.exit(1)
    # construct output file name, if not provided
    output_file = ""
    if len(args_arr) == 2:
        output_file = Path(args_arr[1])
    else:
        output_file = Path(input_file.stem + ".html")
    # read the input file, convert it to html, write it to output file
    read_buffer = input_file.read_text(encoding="utf-8")
    html = convert(read_buffer)  # calling the convert function

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(html, encoding="utf-8")

if __name__ == "__main__":
    main()
  
