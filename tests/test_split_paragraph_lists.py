"""Tests for the split_paragraph_lists configuration option."""

from tests.conftest import convert


class TestSplitParagraphLists:
    """Test split_paragraph_lists configuration."""

    def test_split_paragraph_lists_disabled_default(self, md):
        """Test that split_paragraph_lists is disabled by default."""
        input = "This is a paragraph before the list.\n" "- First item\n" "- Second item"
        expected = "<p>This is a paragraph before the list.\n" "- First item\n" "- Second item</p>"
        result = convert(md, input)
        assert result == expected

    def test_split_paragraph_lists_enabled(self, md_custom):
        """Test split_paragraph_lists when enabled."""
        md = md_custom(split_paragraph_lists=True)
        input = "This is a paragraph before the list.\n" "- First item\n" "- Second item"
        expected = (
            "<p>This is a paragraph before the list.</p>\n"
            "<ul>\n"
            "<li>First item</li>\n"
            "<li>Second item</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_split_paragraph_lists_ordered_list(self, md_custom):
        """Test split_paragraph_lists with ordered lists."""
        md = md_custom(split_paragraph_lists=True)
        input = "This is a paragraph before the list.\n" "1. First item\n" "2. Second item"
        expected = (
            "<p>This is a paragraph before the list.</p>\n"
            "<ol>\n"
            "<li>First item</li>\n"
            "<li>Second item</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_split_paragraph_lists_disabled(self, md_custom):
        """Test split_paragraph_lists when disabled."""
        md = md_custom(split_paragraph_lists=False)
        input = "This is a paragraph before the list.\n" "- First item\n" "- Second item"
        expected = "<p>This is a paragraph before the list.\n" "- First item\n" "- Second item</p>"
        result = convert(md, input)
        assert result == expected

    def test_split_paragraph_lists_disabled_ordered(self, md_custom):
        """Test split_paragraph_lists disabled with ordered lists."""
        md = md_custom(split_paragraph_lists=False)
        input = "This is a paragraph before the list.\n" "1. First item\n" "2. Second item"
        expected = "<p>This is a paragraph before the list.\n" "1. First item\n" "2. Second item</p>"
        result = convert(md, input)
        assert result == expected

    def test_split_paragraph_lists_multiple_paragraphs(self, md_custom):
        """Test split_paragraph_lists with multiple paragraphs and lists."""
        md = md_custom(split_paragraph_lists=True)
        input = (
            "First paragraph.\n"
            "- First list item\n"
            "- Second list item\n"
            "\n"
            "Another paragraph.\n"
            "1. First ordered item\n"
            "2. Second ordered item"
        )
        expected = (
            "<p>First paragraph.</p>\n"
            "<ul>\n"
            "<li>First list item</li>\n"
            "<li>Second list item</li>\n"
            "</ul>\n"
            "<p>Another paragraph.</p>\n"
            "<ol>\n"
            "<li>First ordered item</li>\n"
            "<li>Second ordered item</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_split_paragraph_lists_with_blank_line(self, md_custom):
        """Test that blank lines still work as expected."""
        md = md_custom(split_paragraph_lists=True)
        input = "This is a paragraph before the list.\n" "\n" "- First item\n" "- Second item"
        expected = (
            "<p>This is a paragraph before the list.</p>\n"
            "<ul>\n"
            "<li>First item</li>\n"
            "<li>Second item</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_split_paragraph_lists_nested_context(self, md_custom):
        """Test that properly indented list markers become nested lists."""
        md = md_custom(split_paragraph_lists=True)
        input = "- First item\n" "  This is a paragraph\n" "  1. This becomes a nested list\n" "- Second item"
        expected = (
            "<ul>\n"
            "<li>First item\n"
            "  This is a paragraph<ol>\n"
            "<li>This becomes a nested list</li>\n"
            "</ol>\n"
            "</li>\n"
            "<li>Second item</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_split_paragraph_lists_different_markers(self, md_custom):
        """Test split_paragraph_lists with different list markers."""
        md = md_custom(split_paragraph_lists=True)
        input = "Paragraph before plus marker.\n" "+ First item\n" "+ Second item\n" "* First item\n" "- First item"
        expected = (
            "<p>Paragraph before plus marker.</p>\n"
            "<ul>\n"
            "<li>First item</li>\n"
            "<li>Second item</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>First item</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>First item</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_split_paragraph_lists_multiline_paragraph(self, md_custom):
        """Test split with multiline paragraph before list."""
        md = md_custom(split_paragraph_lists=True)
        input = (
            "This is a longer paragraph\n"
            "that spans multiple lines\n"
            "before the list starts.\n"
            "- First item\n"
            "- Second item"
        )
        expected = (
            "<p>This is a longer paragraph\n"
            "that spans multiple lines\n"
            "before the list starts.</p>\n"
            "<ul>\n"
            "<li>First item</li>\n"
            "<li>Second item</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_split_paragraph_lists_ordered_starting_not_at_one(self, md_custom):
        """Test split with ordered list not starting at 1."""
        md = md_custom(split_paragraph_lists=True)
        input = "This is a paragraph.\n" "3. Third item\n" "4. Fourth item"
        expected = (
            "<p>This is a paragraph.</p>\n" '<ol start="3">\n' "<li>Third item</li>\n" "<li>Fourth item</li>\n" "</ol>"
        )
        result = convert(md, input)
        assert result == expected
