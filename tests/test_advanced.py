import pytest
from tests.conftest import convert

class TestAdvancedScenarios:
    """Test advanced and complex list scenarios."""

    def test_empty_list_items(self, md):
        input = \
"""-
- Item with content
- """
        expected = "<ul><li></li><li>Item with content</li><li></li></ul>"
        result = convert(md, input)
        assert result == expected

    def test_ordered_list_starting_not_at_one(self, md):
        input = \
"""5. Fifth item
6. Sixth item
7. Seventh item"""
        expected = "<ol start=5><li>Fifth item</li><li>Sixth item</li><li>Seventh item</li></ol>"
        result = convert(md, input)
        assert result == expected

    def test_ordered_list_non_sequential_numbers(self, md):
        input = \
"""1. First
3. Third
7. Seventh"""
        expected = "<ol><li>First</li><li>Third</li><li>Seventh</li></ol>"
        result = convert(md, input)
        assert result == expected

    def test_single_item_list(self, md):
        input = "- Only one item"
        expected = "<ul><li>Only one item</li></ul>"
        result = convert(md, input)
        assert result == expected

    def test_list_item_with_trailing_spaces(self, md):
        input = \
"""- Item with spaces
- Normal item
- More spaces     """
        expected = "<ul><li>Item with spaces</li><li>Normal item</li><li>More spaces</li></ul>"
        result = convert(md, input)
        assert result == expected

    def test_mixed_marker_types_same_list(self, md):
        input = \
"""- Unordered item
+ Different marker
* Another marker"""
        expected = "<ul><li>Unordered item</li></ul><ul><li>Different marker</li></ul><ul><li>Another marker</li></ul>"
        result = convert(md, input)
        assert result == expected

    def test_very_long_list_item(self, md):
        input = "- This is a very long list item that contains a lot of text and should still be processed correctly without any issues even though it spans many characters and words and sentences."
        expected = "<ul><li>This is a very long list item that contains a lot of text and should still be processed correctly without any issues even though it spans many characters and words and sentences.</li></ul>"
        result = convert(md, input)
        assert result == expected

    def test_list_with_code_block(self, md):
        input = \
"""- Item with code:

      def hello():
          print("world")

- Next item"""
        expected = "<ul><li>Item with code:<pre><code>def hello():\n    print(\"world\")\n</code></pre></li><li>Next item</li></ul>"
        result = convert(md, input)
        assert result == expected

    def test_list_with_blockquote(self, md):
        input = \
"""1. First item
2. Item with quote:
  > This is a quote
3. Third item"""
        expected = "<ol><li>First item</li><li>Item with quote:<blockquote><p>This is a quote</p></blockquote></li><li>Third item</li></ol>"
        result = convert(md, input)
        assert result == expected
