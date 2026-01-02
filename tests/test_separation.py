import pytest
from tests.conftest import convert

class TestListSeparation:
    """Test list separation behavior."""

    def test_blank_line_separates_lists(self, md):
        text = \
"""- List 1 First
- List 1 Second

- List 2 First
- List 2 Second"""
        expected = \
"""<ul>
<li>List 1 First</li>
<li>List 1 Second</li>
</ul>
<ul>
<li>List 2 First</li>
<li>List 2 Second</li>
</ul>"""
        result = convert(md, text)
        assert result == expected

    def test_multiple_blank_lines_separate_lists(self, md):
        text = \
"""1. List A First
2. List A Second


1. List B First
2. List B Second"""
        expected = \
"""<ol>
<li>List A First</li>
<li>List A Second</li>
</ol>
<ol>
<li>List B First</li>
<li>List B Second</li>
</ol>"""
        result = convert(md, text)
        assert result == expected

    def test_heading_separates_lists(self, md):
        text = \
"""* List X First
* List X Second
# Heading Between Lists
* List Y First
* List Y Second"""
        expected = \
"""<ul>
<li>List X First</li>
<li>List X Second</li>
</ul>
<h1>Heading Between Lists</h1>
<ul>
<li>List Y First</li>
<li>List Y Second</li>
</ul>"""
        result = convert(md, text)
        assert result == expected

    def test_list_then_paragraph_then_list(self, md):
        input = \
"""- First list item
- Second list item

This is a paragraph between lists.

- Third list item
- Fourth list item"""
        expected = \
"""<ul>
<li>First list item</li>
<li>Second list item</li>
</ul>
<p>This is a paragraph between lists.</p>
<ul>
<li>Third list item</li>
<li>Fourth list item</li>
</ul>"""
        result = convert(md, input)
        assert result == expected

    def test_paragraph_then_list(self, md):
        input = \
"""This is a paragraph before the list.

- List item 1
- List item 2"""
        expected = \
"""<p>This is a paragraph before the list.</p>
<ul>
<li>List item 1</li>
<li>List item 2</li>
</ul>"""
        result = convert(md, input)
        assert result == expected

    def test_list_then_paragraph(self, md):
        input = \
"""- List item 1
- List item 2

This is a paragraph after the list."""
        expected = \
"""<ul>
<li>List item 1</li>
<li>List item 2</li>
</ul>
<p>This is a paragraph after the list.</p>"""
        result = convert(md, input)
        assert result == expected

    def test_heading(self, md):
        input = \
"""# Heading

- List item 1
- List item 2

Regular paragraph.

1. Ordered item 1
2. Ordered item 2"""
        expected = \
"""<h1>Heading</h1>
<ul>
<li>List item 1</li>
<li>List item 2</li>
</ul>
<p>Regular paragraph.</p>
<ol>
<li>Ordered item 1</li>
<li>Ordered item 2</li>
</ol>"""
        result = convert(md, input)
        assert result == expected
