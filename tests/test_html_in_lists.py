"""Test for HTML in list items to ensure no codeblock creation."""

from tests.conftest import convert


class TestHtmlInLists:
    """Test that HTML elements in list items are preserved and not converted to code blocks."""

    def test_html_details_in_list_item(self, md):
        """Test that HTML details tag in list items doesn't become a code block."""
        input = (
            "* Testing html in list item `this is code`:\n"
            "\n"
            '  <details markdown="1">\n'
            "    <summary></summary>\n"
            "\n"
            "  Hello test test hello\n"
            "\n"
            "  </details>\n"
            "  <br/>"
        )
        expected = (
            "<ul>\n"
            "<li>\n"
            "<p>Testing html in list item <code>this is code</code>:</p>\n"
            '<details markdown="1">\n'
            "    <summary></summary>\n"
            "\n"
            "  Hello test test hello\n"
            "\n"
            "  </details>\n"
            "<p><br/></p>\n"
            "</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected
        assert "<pre><code>" not in result

    def test_html_div_in_list_item(self, md):
        """Test that HTML div tag in list items doesn't become a code block."""
        input = "* First item\n" "\n" '  <div class="note">\n' "  This is a note\n" "  </div>\n" "\n" "* Second item"
        expected = (
            "<ul>\n"
            "<li>\n"
            "<p>First item</p>\n"
            '<div class="note">\n'
            "  This is a note\n"
            "  </div>\n"
            "\n"
            "</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Second item</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_multiple_html_blocks_in_list(self, md):
        """Test multiple HTML blocks within a list item."""
        input = (
            "1. First item with HTML:\n"
            "\n"
            "   <div>First div</div>\n"
            "\n"
            "   Some text between.\n"
            "\n"
            "   <div>Second div</div>\n"
            "\n"
            "2. Second item"
        )
        expected = (
            "<ol>\n"
            "<li>\n"
            "<p>First item with HTML:</p>\n"
            "<div>First div</div>\n"
            "\n"
            "<p>Some text between.</p>\n"
            "<div>Second div</div>\n"
            "\n"
            "</li>\n"
            "<li>\n"
            "<p>Second item</p>\n"
            "</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected
