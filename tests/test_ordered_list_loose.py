from tests.conftest import convert


class TestOrderedListLoose:
    """Test ordered_list_loose configuration."""

    def test_ordered_list_loose_enabled_default(self, md):
        """Test that blank lines create loose lists with <p> tags by default."""
        input = "1. one\n" "\n" "2. two\n" "\n" "3. three"
        expected = (
            "<ol>\n"
            "<li>\n"
            "<p>one</p>\n"
            "</li>\n"
            "<li>\n"
            "<p>two</p>\n"
            "</li>\n"
            "<li>\n"
            "<p>three</p>\n"
            "</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_ordered_list_loose_disabled(self, md_custom):
        """Test that disabling ordered_list_loose prevents <p> tag wrapping."""
        md = md_custom(ordered_list_loose=False)
        input = "1. one\n" "\n" "2. two\n" "\n" "3. three"
        expected = "<ol>\n" "<li>one</li>\n" "<li>two</li>\n" "<li>three</li>\n" "</ol>"
        result = convert(md, input)
        assert result == expected

    def test_ordered_list_loose_tight_list(self, md):
        """Test that tight lists (no blank lines) don't get <p> tags."""
        input = "1. one\n" "2. two\n" "3. three"
        expected = "<ol>\n" "<li>one</li>\n" "<li>two</li>\n" "<li>three</li>\n" "</ol>"
        result = convert(md, input)
        assert result == expected

    def test_ordered_list_loose_with_paragraphs(self, md):
        """Test loose lists with multiple paragraphs."""
        input = (
            "1. First item\n"
            "\n"
            "  First paragraph in first item.\n"
            "\n"
            "  Second paragraph in first item.\n"
            "\n"
            "2. Second item\n"
            "\n"
            "  Paragraph in second item."
        )
        expected = (
            "<ol>\n"
            "<li>\n"
            "<p>First item</p>\n"
            "<p>First paragraph in first item.</p>\n"
            "<p>Second paragraph in first item.</p>\n"
            "</li>\n"
            "<li>\n"
            "<p>Second item</p>\n"
            "<p>Paragraph in second item.</p>\n"
            "</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_ordered_list_loose_with_nested(self, md):
        """Test loose ordered lists with nested lists."""
        input = "1. First item\n" "\n" "  - Nested unordered\n" "  - Another nested\n" "\n" "2. Second item"
        expected = (
            "<ol>\n"
            "<li>\n"
            "<p>First item</p>\n"
            "<ul>\n"
            "<li>Nested unordered</li>\n"
            "<li>Another nested</li>\n"
            "</ul>\n"
            "</li>\n"
            "<li>\n"
            "<p>Second item</p>\n"
            "</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_ordered_list_loose_starting_not_at_one(self, md):
        """Test loose lists starting at numbers other than 1."""
        input = "5. Fifth\n" "\n" "6. Sixth\n" "\n" "7. Seventh"
        expected = (
            '<ol start="5">\n'
            "<li>\n"
            "<p>Fifth</p>\n"
            "</li>\n"
            "<li>\n"
            "<p>Sixth</p>\n"
            "</li>\n"
            "<li>\n"
            "<p>Seventh</p>\n"
            "</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_ordered_list_loose_with_preserve_numbers(self, md_custom):
        """Test loose lists with preserve_numbers enabled."""
        md = md_custom(ordered_list_loose=True, preserve_numbers=True)
        input = "1. First\n" "\n" "2. Second\n" "\n" "2. Another second"
        expected = (
            "<ol>\n"
            '<li value="1">\n'
            "<p>First</p>\n"
            "</li>\n"
            '<li value="2">\n'
            "<p>Second</p>\n"
            "</li>\n"
            '<li value="2">\n'
            "<p>Another second</p>\n"
            "</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_ordered_list_loose_disabled_with_preserve_numbers(self, md_custom):
        """Test tight lists with preserve_numbers enabled."""
        md = md_custom(ordered_list_loose=False, preserve_numbers=True)
        input = "1. First\n" "\n" "2. Second\n" "\n" "2. Another second"
        expected = (
            "<ol>\n"
            '<li value="1">First</li>\n'
            '<li value="2">Second</li>\n'
            '<li value="2">Another second</li>\n'
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_ordered_list_loose_with_code_block(self, md):
        """Test loose list with code block."""
        input = "1. Item with code\n" "\n" "      code block\n" "      more code\n" "\n" "2. Next item"
        expected = (
            "<ol>\n"
            "<li>\n"
            "<p>Item with code</p>\n"
            "<pre><code>code block\n"
            "more code\n"
            "</code></pre>\n"
            "</li>\n"
            "<li>\n"
            "<p>Next item</p>\n"
            "</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_ordered_list_loose_mixed_spacing(self, md):
        """Test list with mixed spacing (some blank lines, some not)."""
        input = "1. First\n" "\n" "2. Second\n" "3. Third\n" "\n" "4. Fourth"
        expected = (
            "<ol>\n"
            "<li>\n"
            "<p>First</p>\n"
            "</li>\n"
            "<li>\n"
            "<p>Second</p>\n"
            "</li>\n"
            "<li>\n"
            "<p>Third</p>\n"
            "</li>\n"
            "<li>\n"
            "<p>Fourth</p>\n"
            "</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected
