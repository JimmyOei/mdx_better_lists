from tests.conftest import convert


class TestNestedLists:
    """Test nested lists behavior."""

    def test_nested_list_with_2_space_indent(self, md):
        input = "- Item 1\n" "  - Nested 1\n" "  - Nested 2\n" "- Item 2"
        expected = (
            "<ul>\n"
            "<li>Item 1<ul>\n"
            "<li>Nested 1</li>\n"
            "<li>Nested 2</li>\n"
            "</ul>\n"
            "</li>\n"
            "<li>Item 2</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_nested_list_with_4_space_indent(self, md_custom):
        md = md_custom(nested_indent=4)
        input = "- Item A\n" "    - Nested A1\n" "    - Nested A2\n" "- Item B"
        expected = (
            "<ul>\n"
            "<li>Item A<ul>\n"
            "<li>Nested A1</li>\n"
            "<li>Nested A2</li>\n"
            "</ul>\n"
            "</li>\n"
            "<li>Item B</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_mixed_nested_lists(self, md):
        input = "1. Item 1\n" "  - Subitem 1\n" "  - Subitem 2\n" "2. Item 2\n" "  1. Subitem 2.1\n" "  2. Subitem 2.2"
        expected = (
            "<ol>\n"
            "<li>Item 1<ul>\n"
            "<li>Subitem 1</li>\n"
            "<li>Subitem 2</li>\n"
            "</ul>\n"
            "</li>\n"
            "<li>Item 2<ol>\n"
            "<li>Subitem 2.1</li>\n"
            "<li>Subitem 2.2</li>\n"
            "</ol>\n"
            "</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_deeply_nested_lists(self, md):
        input = "- Level 1\n" "  - Level 2\n" "    - Level 3\n" "      - Level 4\n" "- Back to Level 1"
        expected = (
            "<ul>\n"
            "<li>Level 1<ul>\n"
            "<li>Level 2<ul>\n"
            "<li>Level 3<ul>\n"
            "<li>Level 4</li>\n"
            "</ul>\n"
            "</li>\n"
            "</ul>\n"
            "</li>\n"
            "</ul>\n"
            "</li>\n"
            "<li>Back to Level 1</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_preserve_numbers_with_nested_lists(self, md_custom):
        """Test preserve_numbers with nested ordered lists."""
        md = md_custom(preserve_numbers=True)
        input = (
            "1. First\n"
            "2. Second\n"
            "2. Another second\n"
            "  1. Nested first\n"
            "  2. Nested second\n"
            "  2. Nested repeat\n"
            "3. Third"
        )
        expected = (
            "<ol>\n"
            '<li value="1">First</li>\n'
            '<li value="2">Second</li>\n'
            '<li value="2">Another second<ol>\n'
            '<li value="1">Nested first</li>\n'
            '<li value="2">Nested second</li>\n'
            '<li value="2">Nested repeat</li>\n'
            "</ol>\n"
            "</li>\n"
            '<li value="3">Third</li>\n'
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_preserve_numbers_with_mixed_nested_lists(self, md_custom):
        """Test preserve_numbers with mixed nested lists."""
        md = md_custom(preserve_numbers=True)
        input = (
            "1. Outer one\n"
            "1. Outer one again\n"
            "  - Unordered nested\n"
            "  - Another unordered\n"
            "2. Outer two\n"
            "  3. Inner three\n"
            "  3. Inner three again\n"
            "  5. Inner five"
        )
        expected = (
            "<ol>\n"
            '<li value="1">Outer one</li>\n'
            '<li value="1">Outer one again<ul>\n'
            "<li>Unordered nested</li>\n"
            "<li>Another unordered</li>\n"
            "</ul>\n"
            "</li>\n"
            '<li value="2">Outer two<ol start="3">\n'
            '<li value="3">Inner three</li>\n'
            '<li value="3">Inner three again</li>\n'
            '<li value="5">Inner five</li>\n'
            "</ol>\n"
            "</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_preserve_numbers_deeply_nested(self, md_custom):
        """Test preserve_numbers with deeply nested ordered lists."""
        md = md_custom(preserve_numbers=True)
        input = (
            "1. Level 1\n"
            "1. Level 1 again\n"
            "  2. Level 2\n"
            "  2. Level 2 repeat\n"
            "    5. Level 3\n"
            "    5. Level 3 repeat\n"
            "2. Back to Level 1"
        )
        expected = (
            "<ol>\n"
            '<li value="1">Level 1</li>\n'
            '<li value="1">Level 1 again<ol start="2">\n'
            '<li value="2">Level 2</li>\n'
            '<li value="2">Level 2 repeat<ol start="5">\n'
            '<li value="5">Level 3</li>\n'
            '<li value="5">Level 3 repeat</li>\n'
            "</ol>\n"
            "</li>\n"
            "</ol>\n"
            "</li>\n"
            '<li value="2">Back to Level 1</li>\n'
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected
