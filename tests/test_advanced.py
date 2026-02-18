from tests.conftest import convert


class TestAdvanced:
    """Test advanced and complex list structures."""

    def test_ordered_list_starting_not_at_one(self, md):
        input = "5. Fifth item\n" "6. Sixth item\n" "7. Seventh item"
        expected = '<ol start="5">\n' "<li>Fifth item</li>\n" "<li>Sixth item</li>\n" "<li>Seventh item</li>\n" "</ol>"
        result = convert(md, input)
        assert result == expected

    def test_ordered_list_non_sequential_numbers(self, md):
        input = "1. First\n" "3. Third\n" "7. Seventh"
        expected = "<ol>\n" "<li>First</li>\n" "<li>Third</li>\n" "<li>Seventh</li>\n" "</ol>"
        result = convert(md, input)
        assert result == expected

    def test_single_item_list(self, md):
        input = "- Only one item"
        expected = "<ul>\n" "<li>Only one item</li>\n" "</ul>"
        result = convert(md, input)
        assert result == expected

    def test_list_item_with_trailing_spaces(self, md):
        input = "- Item with spaces\n" "- Normal item\n" "- More spaces     "
        expected = "<ul>\n" "<li>Item with spaces</li>\n" "<li>Normal item</li>\n" "<li>More spaces     </li>\n" "</ul>"
        result = convert(md, input)
        assert result == expected

    def test_very_long_list_item(self, md):
        input = "- This is a very long list item that contains a lot of text and should still be processed correctly without any issues even though it spans many characters and words and sentences."  # noqa: E501
        expected = (
            "<ul>\n"
            "<li>This is a very long list item that contains a lot of text and should still be processed correctly without any issues even though it spans many characters and words and sentences.</li>\n"  # noqa: E501
            "</ul>"
        )  # noqa: E501
        result = convert(md, input)
        assert result == expected

    def test_list_with_code_block(self, md):
        input = "- Item with code:\n" "\n" "      def hello():\n" '          print("world")\n' "\n" "- Next item"
        expected = (
            "<ul>\n"
            "<li>Item with code:<pre><code>def hello():\n"
            '    print("world")\n'
            "</code></pre>\n"
            "</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Next item</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_list_with_blockquote(self, md):
        input = "1. First item\n" "2. Item with quote:\n" "  > This is a quote\n" "3. Third item"
        expected = (
            "<ol>\n"
            "<li>First item</li>\n"
            "<li>Item with quote:<blockquote>\n"
            "<p>This is a quote</p>\n"
            "</blockquote>\n"
            "</li>\n"
            "<li>Third item</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_complex_nested_with_separation(self, md):
        """Test preserve_numbers with complex nested lists and separation."""
        input = (
            "- First list item\n"
            "  Paragraph in first item.\n"
            "\n"
            "  - Subitem one\n"
            "    - Sub-subitem one\n"
            "    - Sub-subitem two\n"
            "  - Subitem two\n"
            "- Second list item\n"
            "\n"
            "  This is a paragraph.\n"
            "\n"
            "- New list item\n"
            "  This item is of a new list.\n"
            "1. First ordered item\n"
            "   With paragraph in first ordered item.\n"
            "\n"
            "   1. Nested ordered one\n"
            "   2. Nested ordered two\n"
            "     1. Deep nested one\n"
            "       With a paragraph.\n"
            "\n"
            "       And another paragraph with a list:\n"
            "       1. Deep deep one\n"
            "       2. Deep deep two\n"
            "    3. Nested ordered three\n"
            "2. Second ordered item"
        )
        expected = (
            "<ul>\n"
            "<li>\n"
            "<p>First list item\n"
            "  Paragraph in first item.</p>\n"
            "<ul>\n"
            "<li>Subitem one<ul>\n"
            "<li>Sub-subitem one</li>\n"
            "<li>Sub-subitem two</li>\n"
            "</ul>\n"
            "</li>\n"
            "<li>Subitem two</li>\n"
            "</ul>\n"
            "</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>\n"
            "<p>Second list item</p>\n"
            "<p>This is a paragraph.</p>\n"
            "</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>\n"
            "<p>New list item\n"
            "  This item is of a new list.\n"
            "1. First ordered item\n"
            "   With paragraph in first ordered item.</p>\n"
            "<ol>\n"
            "<li>Nested ordered one</li>\n"
            "<li>Nested ordered two<ol>\n"
            "<li>\n"
            "<p>Deep nested one\n"
            "   With a paragraph.</p>\n"
            "<p>And another paragraph with a list:</p>\n"
            "<ol>\n"
            "<li>Deep deep one</li>\n"
            "<li>Deep deep two\n"
            "    3. Nested ordered three</li>\n"
            "</ol>\n"
            "</li>\n"
            "</ol>\n"
            "</li>\n"
            "</ol>\n"
            "</li>\n"
            "</ul>\n"
            '<ol start="2">\n'
            "<li>Second ordered item</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected
