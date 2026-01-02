import pytest
from tests.conftest import convert

class TestAdvancedScenarios:
    """Test advanced and complex list scenarios."""

    def test_ordered_list_starting_not_at_one(self, md):
        input = \
"""5. Fifth item
6. Sixth item
7. Seventh item"""
        expected = \
"""<ol start="5">
<li>Fifth item</li>
<li>Sixth item</li>
<li>Seventh item</li>
</ol>"""
        result = convert(md, input)
        assert result == expected

    def test_ordered_list_non_sequential_numbers(self, md):
        input = \
"""1. First
3. Third
7. Seventh"""
        expected = \
"""<ol>
<li>First</li>
<li>Third</li>
<li>Seventh</li>
</ol>"""
        result = convert(md, input)
        assert result == expected

    def test_single_item_list(self, md):
        input = "- Only one item"
        expected = \
"""<ul>
<li>Only one item</li>
</ul>"""
        result = convert(md, input)
        assert result == expected

    def test_list_item_with_trailing_spaces(self, md):
        input = \
"""- Item with spaces
- Normal item
- More spaces     """
        expected = \
"""<ul>
<li>Item with spaces</li>
<li>Normal item</li>
<li>More spaces     </li>
</ul>"""
        result = convert(md, input)
        assert result == expected

    def test_mixed_marker_types_same_list(self, md):
        input = \
"""- Unordered item
+ Different marker
* Another marker"""
        expected = \
"""<ul>
<li>Unordered item</li>
<li>Different marker</li>
<li>Another marker</li>
</ul>"""
        result = convert(md, input)
        assert result == expected

    def test_very_long_list_item(self, md):
        input = "- This is a very long list item that contains a lot of text and should still be processed correctly without any issues even though it spans many characters and words and sentences."
        expected = \
"""<ul>
<li>This is a very long list item that contains a lot of text and should still be processed correctly without any issues even though it spans many characters and words and sentences.</li>
</ul>"""
        result = convert(md, input)
        assert result == expected

    def test_list_with_code_block(self, md):
        input = \
"""- Item with code:

      def hello():
          print("world")

- Next item"""
        expected = \
"""<ul>
<li>Item with code:<pre><code>def hello():
    print("world")
</code></pre>
</li>
</ul>
<ul>
<li>Next item</li>
</ul>"""
        result = convert(md, input)
        assert result == expected

    def test_list_with_blockquote(self, md):
        input = \
"""1. First item
2. Item with quote:
  > This is a quote
3. Third item"""
        expected = \
"""<ol>
<li>First item</li>
<li>Item with quote:<blockquote>
<p>This is a quote</p>
</blockquote>
</li>
<li>Third item</li>
</ol>"""
        result = convert(md, input)
        assert result == expected

    def test_preserve_numbers_disabled(self, md):
        """Test that default behavior doesn't preserve numbers."""
        input = \
"""1. First
2. Second
2. Another second
2. Yet another second
3. Third"""
        expected = \
"""<ol>
<li>First</li>
<li>Second</li>
<li>Another second</li>
<li>Yet another second</li>
<li>Third</li>
</ol>"""
        result = convert(md, input)
        assert result == expected

    def test_preserve_numbers_enabled(self, md_custom):
        """Test that preserve_numbers config preserves exact numbers."""
        md = md_custom(preserve_numbers=True)
        input = \
"""1. First
2. Second
2. Another second
2. Yet another second
3. Third
3. Another third"""
        expected = \
"""<ol>
<li value="1">First</li>
<li value="2">Second</li>
<li value="2">Another second</li>
<li value="2">Yet another second</li>
<li value="3">Third</li>
<li value="3">Another third</li>
</ol>"""
        result = convert(md, input)
        assert result == expected

    def test_preserve_numbers_non_sequential(self, md_custom):
        """Test preserve_numbers with non-sequential numbers."""
        md = md_custom(preserve_numbers=True)
        input = \
"""1. First
5. Fifth
5. Another fifth
10. Tenth"""
        expected = \
"""<ol>
<li value="1">First</li>
<li value="5">Fifth</li>
<li value="5">Another fifth</li>
<li value="10">Tenth</li>
</ol>"""
        result = convert(md, input)
        assert result == expected

    def test_preserve_numbers_starting_not_at_one(self, md_custom):
        """Test preserve_numbers with list starting at non-1."""
        md = md_custom(preserve_numbers=True)
        input = \
"""7. Seventh
7. Another seventh
8. Eighth"""
        expected = \
"""<ol start="7">
<li value="7">Seventh</li>
<li value="7">Another seventh</li>
<li value="8">Eighth</li>
</ol>"""
        result = convert(md, input)
        assert result == expected

    def test_preserve_numbers_complex(self, md_custom):
        """Test preserve_numbers with complex list."""
        md = md_custom(preserve_numbers=True)
        input = \
"""3. Item three

  First paragraph in item three.
    
  Second paragraph in item three.

4. Item four in a new list
  Paragraph in item four
  that spans multiple
  lines.

  And another paragraph with a list:
  - Subitem one
  - Subitem two
    * Sub-subitem
      1. Deep item one
      1. Deep item one again
      2. Deep item two
  - Subitem three
5. Item five

1. And a new list
2. Continuing the new list
2. Another two
3. Ending the new list"""
        expected = \
"""<ol start="3">
<li value="3">
<p>Item three</p>
<p>First paragraph in item three.</p>
<p>Second paragraph in item three.</p>
</li>
</ol>
<ol start="4">
<li value="4">
<p>Item four in a new list
  Paragraph in item four
  that spans multiple
  lines.</p>
<p>And another paragraph with a list:</p>
<ul>
<li>Subitem one</li>
<li>Subitem two<ul>
<li>Sub-subitem<ol start="1">
<li value="1">Deep item one</li>
<li value="1">Deep item one again</li>
<li value="2">Deep item two</li>
</ol>
</li>
</ul>
</li>
<li>Subitem three</li>
</ul>
</li>
<li value="5">Item five</li>
</ol>
<ol>
<li value="1">And a new list</li>
<li value="2">Continuing the new list</li>
<li value="2">Another two</li>
<li value="3">Ending the new list</li>
</ol>"""
        result = convert(md, input)
        assert result == expected