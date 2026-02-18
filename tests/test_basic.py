"""Basic tests for mdx_better_lists extension.

Write your TDD tests here! These examples show the testing pattern.
"""

from tests.conftest import convert


class TestSimpleUnorderedLists:
    """Test simple unordered lists."""

    def test_simple_minus_unordered_list(self, md):
        input = "- Item A\n" "- Item B\n" "- Item C"
        expected = "<ul>\n" "<li>Item A</li>\n" "<li>Item B</li>\n" "<li>Item C</li>\n" "</ul>"
        result = convert(md, input)
        assert result == expected

    def test_simple_plus_unordered_list(self, md):
        input = "+ Item 1\n" "+ Item 2\n" "+ Item 3"
        expected = "<ul>\n" "<li>Item 1</li>\n" "<li>Item 2</li>\n" "<li>Item 3</li>\n" "</ul>"
        result = convert(md, input)
        assert result == expected

    def test_simple_asterisk_unordered_list(self, md):
        input = "* Alpha\n" "* Beta\n" "* Gamma"
        expected = "<ul>\n" "<li>Alpha</li>\n" "<li>Beta</li>\n" "<li>Gamma</li>\n" "</ul>"
        result = convert(md, input)
        assert result == expected


class TestSimpleOrderedLists:
    """Test simple ordered lists."""

    def test_simple_numeric_ordered_list(self, md):
        input = "1. First\n" "2. Second\n" "3. Third"
        expected = "<ol>\n" "<li>First</li>\n" "<li>Second</li>\n" "<li>Third</li>\n" "</ol>"
        result = convert(md, input)
        assert result == expected
