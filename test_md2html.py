from md2html import *
import pytest

# Test convert_emphasis
@pytest.mark.parametrize("input_md, expected_html", [
    # Normal cases
    ('**bold**', '<strong>bold</strong>'),
    ('__bold__', '<strong>bold</strong>'), 
    ('*italic*', '<em>italic</em>'),
    ('_italic_', '<em>italic</em>'),
    ('***bold italic***', '<em><strong>bold italic</strong></em>'),
    
    # Edge cases
    ('g**litters**', 'g<strong>litters</strong>'),  # Mid-word asterisk, OK
    ('g__litters__', 'g__litters__'),  # Mid-word underscore, NOT OK
    ('**bold** and **more**', '<strong>bold</strong> and <strong>more</strong>'),  # Multiple
    ('*italic* and **bold**', '<em>italic</em> and <strong>bold</strong>'),  # Mixed
])

def test_convert_emphasis(input_md, expected_html):
    assert convert_emphasis(input_md) == expected_html

# Test convert_headings  
@pytest.mark.parametrize("input_md, expected_html", [
    # Normal cases
    ('# H1', '<h1>H1</h1>'),
    ('## H2', '<h2>H2</h2>'),
    ('H1\n===', '<h1>H1</h1>'),
    ('H2\n---', '<h2>H2</h2>'),
    
    # Edge cases  
    ('####### H7', '####### H7'),  # Hashes greater than 6
    ('#', '#'),  # No text
    ('H1\n=', 'H1\n='),  # Only one =
])
def test_convert_headings(input_md, expected_html):
    assert convert_headings(input_md) == expected_html

# Test convert_paragraph
@pytest.mark.parametrize("input_md, expected_html", [
    ('Single line', '<p>Single line</p>'),
    ('Line 1\nLine 2', '<p>Line 1<br>Line 2</p>'),
    ('', '<p></p>'),  # Empty
    ('Text with **bold**', '<p>Text with **bold**</p>'),  # No inline processing
])
def test_convert_paragraph(input_md, expected_html):
    assert convert_paragraph(input_md) == expected_html


# Test convert_ordered_list 
@pytest.mark.parametrize("input_md, expected_html", [
    # Normal cases
    ("1. First item", "<ol>\n  <li>First item</li>\n</ol>"),
    ("1. First item\n2. Second item", "<ol>\n  <li>First item</li>\n  <li>Second item</li>\n</ol>"),
    ("1. First item\n1. Second item", "<ol>\n  <li>First item</li>\n  <li>Second item</li>\n</ol>"),
    ("1. Item with **bold**", "<ol>\n  <li>Item with **bold**</li>\n</ol>"),
    
    # Edge cases
    ("1.", "<ol>\n  <li></li>\n</ol>"),  # No text after number
])
def test_convert_ordered_list(input_md, expected_html):
    assert convert_ordered_list(input_md) == expected_html

# Test convert_unordered_list 
@pytest.mark.parametrize("input_md, expected_html", [
    # Normal cases (all three marker types)
    ("- First item", "<ul>\n  <li>First item</li>\n</ul>"),
    ("* First item", "<ul>\n  <li>First item</li>\n</ul>"),
    ("+ First item", "<ul>\n  <li>First item</li>\n</ul>"),
    ("- First item\n- Second item", "<ul>\n  <li>First item</li>\n  <li>Second item</li>\n</ul>"),
    ("- Item with *italic*", "<ul>\n  <li>Item with *italic*</li>\n</ul>"),
    
    # Edge cases
    ("-", "<ul>\n  <li></li>\n</ul>"),  # No text after marker
])
def test_convert_code(input_md, expected_html):  # ADDED THIS FUNCTION
    assert convert_code(input_md) == expected_html

# Test convert_code 
@pytest.mark.parametrize("input_md, expected_html", [
    # Normal cases
    ("`single backtick`", "<code>single backtick</code>"),
    ("``double backticks``", "<code>double backticks</code>"),
    ("Text with `code` inside", "Text with <code>code</code> inside"),
    ("`multiple` `code` `spans`", "<code>multiple</code> <code>code</code> <code>spans</code>"),
    
    # Edge cases
    ("`unclosed code", "`unclosed code"),  # Unclosed backticks
    ("``code`", "`<code>code</code>"),  # Mismatched backticks
])

def test_convert_code(input_md, expected_html):
    assert convert_code(input_md) == expected_html

# Test convert_code 
@pytest.mark.parametrize("input_md, expected_html", [
    # Normal cases
    ("`single backtick`", "<code>single backtick</code>"),
    ("``double backticks``", "<code>double backticks</code>"),
    ("Text with `code` inside", "Text with <code>code</code> inside"),
    ("`multiple` `code` `spans`", "<code>multiple</code> <code>code</code> <code>spans</code>"),
    
    # Edge cases
    ("`unclosed code", "`unclosed code"),  # Unclosed backticks
    ("``code`", "`<code>code</code>"),  # Mismatched backticks
])

def test_convert_code(input_md, expected_html):
    assert convert_code(input_md) == expected_html


# Test convert_link
@pytest.mark.parametrize("input_md, expected_html", [
    # Normal cases
    ("[text](url)", '<a href="url">text</a>'),
    ("[Google](https://google.com)", '<a href="https://google.com">Google</a>'),
    
    # Edge cases
    ("[text] (url)", '[text] (url)'),  # Space between ] and (, should not parse
    ("[]()", '[]()'),  # Empty text and URL
])
def test_convert_link(input_md, expected_html):
    assert convert_link(input_md) == expected_html

@pytest.fixture
def normal_document():
    return """# Main Title

This is a paragraph with ***bold and italic*** text and `code`.

## H2 Element

1. Ordered item Num 1
2. Num 2 Ordered item

- Unordered list item
- Another unordered list item
- Third item unordered

THIS IS A LINK: [YOUTUBE](https://youTUBE.com).
"""

@pytest.fixture
def edge_case_document():
    return """# TITLE

1.
Ordered list with no text after number

-
Unordered list with no text

[invalid link (missing closing)

**unclosed bold
"""


# Test convert
def test_convert_normal_case(normal_document):
    """Test convert function with a complete, well-formed markdown document"""
    html = convert(normal_document)
    
    # Test headings are properly converted
    assert "<h1>Main Title</h1>" in html
    assert "<h2>H2 Element</h2>" in html
    
    # Test emphasis combinations
    assert "<em><strong>bold and italic</strong></em>" in html
    
    # Test code inline element
    assert "<code>code</code>" in html
    
    # Test ordered list structure and content
    assert "<ol>" in html and "</ul>" in html
    assert "<li>Ordered item Num 1</li>" in html
    assert "<li>Num 2 Ordered item</li>" in html
    
    # Test unordered list structure and content  
    assert "<ul>" in html and "</ul>" in html
    assert "<li>Unordered list item</li>" in html
    assert "<li>Another unordered list item</li>" in html
    assert "<li>Third item unordered</li>" in html
    
    # Test link conversion
    assert '<a href="https://youTUBE.com">YOUTUBE</a>' in html
    
    # Test paragraph structure
    assert "<p>" in html
    assert "THIS IS A LINK:" in html

def test_convert_edge_case(edge_case_document):
    """Test that invalid markdown syntax is preserved as text"""
    html = convert(edge_case_document)
    
    # Test invalid list did not convert
    assert "<ol>" not in html
    assert "<ul>" not in html
    
    # Unclosed bold should not be converted
    assert "**unclosed bold" in html
    assert "<strong>unclosed bold</strong>" not in html
    
    # Invalid link syntax should remain as paragraph text
    assert "[invalid link (missing closing)" in html
