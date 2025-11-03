from md2html import convert_emphasis, convert_paragraph

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

def test_multi_line_paragraph():
    s = "Line break after this. \n Line break before this."
    result = "<p>Line break after this. <br> Line break before this.</p>"
    assert convert_paragraph(s) == result

def test_single_line_paragraph():
    s = "No line breaks"
    result = "<p>No line breaks</p>"
    assert convert_paragraph(s) == result