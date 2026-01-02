import pytest
from tests.conftest import convert

class TestNestedLists:
    """Test nested lists behavior."""

    def test_nested_list_with_2_space_indent(self, md):
        input = \
"""- Item 1
  - Nested 1
  - Nested 2
- Item 2"""
        expected = \
"""<ul>
<li>Item 1<ul>
<li>Nested 1</li>
<li>Nested 2</li>
</ul>
</li>
<li>Item 2</li>
</ul>"""
        result = convert(md, input)
        assert result == expected
        
    def test_nested_list_with_4_space_indent(self, md_custom):
        md = md_custom(nested_indent=4)
        input = \
"""- Item A
    - Nested A1
    - Nested A2
- Item B"""
        expected = \
"""<ul>
<li>Item A<ul>
<li>Nested A1</li>
<li>Nested A2</li>
</ul>
</li>
<li>Item B</li>
</ul>"""
        result = convert(md, input)
        assert result == expected
        
    def test_mixed_nested_lists(self, md):
        input = \
"""1. Item 1
  - Subitem 1
  - Subitem 2
2. Item 2
  1. Subitem 2.1
  2. Subitem 2.2"""
        expected = \
"""<ol>
<li>Item 1<ul>
<li>Subitem 1</li>
<li>Subitem 2</li>
</ul>
</li>
<li>Item 2<ol>
<li>Subitem 2.1</li>
<li>Subitem 2.2</li>
</ol>
</li>
</ol>"""
        result = convert(md, input)
        assert result == expected
        
    def test_deeply_nested_lists(self, md):
        input = \
"""- Level 1
  - Level 2
    - Level 3
      - Level 4
- Back to Level 1"""
        expected = \
"""<ul>
<li>Level 1<ul>
<li>Level 2<ul>
<li>Level 3<ul>
<li>Level 4</li>
</ul>
</li>
</ul>
</li>
</ul>
</li>
<li>Back to Level 1</li>
</ul>"""
        result = convert(md, input)
        assert result == expected