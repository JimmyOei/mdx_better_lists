from tests.conftest import convert


class TestUnorderedListSeparation:
    """Test unordered_list_separation configuration."""

    def test_unordered_list_separation_enabled_default(self, md):
        """Test that blank lines separate unordered lists by default."""
        input = "- First\n" "\n" "- Second\n" "- Third"
        expected = "<ul>\n" "<li>First</li>\n" "</ul>\n" "<ul>\n" "<li>Second</li>\n" "<li>Third</li>\n" "</ul>"
        result = convert(md, input)
        assert result == expected

    def test_unordered_list_separation_disabled(self, md_custom):
        """Test that disabling unordered_list_separation keeps lists together."""
        md = md_custom(unordered_list_separation=False)
        input = "- First\n" "\n" "- Second\n" "- Third"
        expected = "<ul>\n" "<li>First</li>\n" "<li>Second</li>\n" "<li>Third</li>\n" "</ul>"
        result = convert(md, input)
        assert result == expected

    def test_unordered_list_separation_tight_list(self, md):
        """Test that tight lists stay together."""
        input = "- First\n" "- Second\n" "- Third"
        expected = "<ul>\n" "<li>First</li>\n" "<li>Second</li>\n" "<li>Third</li>\n" "</ul>"
        result = convert(md, input)
        assert result == expected

    def test_unordered_list_separation_multiple_blanks(self, md):
        """Test separation with multiple blank lines."""
        input = "- First\n" "\n" "\n" "- Second\n" "\n" "\n" "- Third"
        expected = (
            "<ul>\n"
            "<li>First</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Second</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Third</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_unordered_list_separation_with_paragraphs(self, md):
        """Test list separation with paragraphs in items."""
        input = "- First item\n" "\n" "  Paragraph in first.\n" "\n" "- Second item\n" "\n" "  Paragraph in second."
        expected = (
            "<ul>\n"
            "<li>\n"
            "<p>First item</p>\n"
            "<p>Paragraph in first.</p>\n"
            "</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>\n"
            "<p>Second item</p>\n"
            "<p>Paragraph in second.</p>\n"
            "</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_unordered_list_separation_disabled_with_paragraphs(self, md_custom):
        """Test that disabled separation keeps lists with paragraphs together."""
        md = md_custom(unordered_list_separation=False)
        input = "- First item\n" "\n" "  Paragraph in first.\n" "\n" "- Second item\n" "\n" "  Paragraph in second."
        expected = (
            "<ul>\n"
            "<li>\n"
            "<p>First item</p>\n"
            "<p>Paragraph in first.</p>\n"
            "</li>\n"
            "<li>\n"
            "<p>Second item</p>\n"
            "<p>Paragraph in second.</p>\n"
            "</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_unordered_list_separation_with_nested(self, md):
        """Test separation with nested lists."""
        input = "- Outer one\n" "  - Nested\n" "  - Another nested\n" "\n" "- Outer two"
        expected = (
            "<ul>\n"
            "<li>Outer one<ul>\n"
            "<li>Nested</li>\n"
            "<li>Another nested</li>\n"
            "</ul>\n"
            "</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Outer two</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_unordered_list_separation_with_code(self, md):
        """Test separation with code blocks."""
        input = "- Item with code\n" "\n" "      code here\n" "\n" "- Next item"
        expected = (
            "<ul>\n"
            "<li>Item with code<pre><code>code here\n"
            "</code></pre>\n"
            "</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Next item</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected
