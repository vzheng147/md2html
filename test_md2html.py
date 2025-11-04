
from md2html import *

# Testing emphasis
def test_triple_star():
    assert convert_emphasis('***really important***') == '<em><strong>really important</strong></em>'

def test_triple_underscore_whole_word():
    assert convert_emphasis('___really important___') == '<em><strong>really important</strong></em>'

def test_triple_underscore_midword_stays():
    s = 'im___port___ant'
    assert convert_emphasis(s) == s

def test_double_star_midword_ok():
    assert convert_emphasis('g**litters**') == 'g<strong>litters</strong>'

def test_double_underscore_midword_stays():
    s = 'g__litters__'
    assert convert_emphasis(s) == s

def test_single_star_and_underscore():
    assert convert_emphasis('a *b* _c_') == 'a <em>b</em> <em>c</em>'

# Testing paragraph
def test_multi_line_paragraph():
    s = "Line break after this. \n Line break before this."
    result = "<p>Line break after this. <br> Line break before this.</p>"
    assert convert_paragraph(s) == result

def test_single_line_paragraph():
    s = "No line breaks"
    result = "<p>No line breaks</p>"
    assert convert_paragraph(s) == result

# Testing heading
    
def test_setext_h2_underline():
    md = "Subheading\n----"
    assert convert_headings(md) == "<h2>Subheading</h2>"

def test_atx_h4_hashes():
    md = "#### Deep Title"
    assert convert_headings(md) == "<h4>Deep Title</h4>"

# Testing order / unordered lists
    
def test_ol_basic_three_items():
    md = "1. First\n2. Second\n3. Third"
    html = convert_ordered_list(md)
    assert html == (
        "<ol>\n"
        "  <li>First</li>\n"
        "  <li>Second</li>\n"
        "  <li>Third</li>\n"
        "</ol>"
    )

def test_ul_basic_hyphen():
    md = "- Alpha\n- Beta\n- Gamma"
    html = convert_unordered_list(md)
    assert html == (
        "<ul>\n"
        "  <li>Alpha</li>\n"
        "  <li>Beta</li>\n"
        "  <li>Gamma</li>\n"
        "</ul>"
    )

# Testing code
    
def test_basic_code():
    s = "I prefer `pytest` over `unittest`."
    result = "I prefer <code>pytest</code> over <code>unittest</code>."
    assert(convert_code(s) == result)


# Testing link
    
def test_basic_link():
    s = '[docs](example.com)'
    result = '<a href="example.com">docs</a>'
    assert convert_link(s) == result