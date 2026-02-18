from tests.conftest import convert


class TestParagraphsInLists:
    """Test paragraph handling in lists."""

    def test_paragraph_item_lists(self, md):
        input = "- Item 1\n" "this is a paragraph in item 1.\n" "- Item 2\n" "this is a paragraph in item 2."
        expected = (
            "<ul>\n"
            "<li>Item 1\n"
            "this is a paragraph in item 1.</li>\n"
            "<li>Item 2\n"
            "this is a paragraph in item 2.</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_indented_paragraph_item_lists(self, md):
        input = "1. Item 1\n" "  this is a paragraph in item 1.\n" "2. Item 2\n" "  this is a paragraph in item 2."
        expected = (
            "<ol>\n"
            "<li>Item 1\n"
            "  this is a paragraph in item 1.</li>\n"
            "<li>Item 2\n"
            "  this is a paragraph in item 2.</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_weird_indented_paragraph_item_lists(self, md):
        input = (
            "* Item 1\n"
            " this is a paragraph in item 1.\n"
            "* Item 2\n"
            "    this is a paragraph in item 2.\n"
            "* Item 3\n"
            "     this is a paragraph in item 3."
        )
        expected = (
            "<ul>\n"
            "<li>Item 1\n"
            " this is a paragraph in item 1.</li>\n"
            "<li>Item 2\n"
            "    this is a paragraph in item 2.</li>\n"
            "<li>Item 3\n"
            "     this is a paragraph in item 3.</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_multi_line_paragraphs_in_list_items(self, md):
        input = (
            "1. Item 1\n"
            "This is a paragraph in item 1\n"
            "that continues here,\n"
            "and even here.\n"
            "2. Item 2\n"
            "  This is a paragraph in item 2\n"
            "  that also continues here."
        )
        expected = (
            "<ol>\n"
            "<li>Item 1\n"
            "This is a paragraph in item 1\n"
            "that continues here,\n"
            "and even here.</li>\n"
            "<li>Item 2\n"
            "  This is a paragraph in item 2\n"
            "  that also continues here.</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_multiple_paragraphs_in_list_items(self, md):
        input = (
            "- Item 1\n"
            "\n"
            "  This is the first paragraph in item 1.\n"
            "\n"
            "  This is the second paragraph in item 1.\n"
            "\n"
            "- Item 2\n"
            "\n"
            "  This is the first paragraph in item 2.\n"
            "\n"
            "  This is the second paragraph in item 2.\n"
            "\n"
            "  This is the third paragraph in item 2."
        )
        expected = (
            "<ul>\n"
            "<li>\n"
            "<p>Item 1</p>\n"
            "<p>This is the first paragraph in item 1.</p>\n"
            "<p>This is the second paragraph in item 1.</p>\n"
            "</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>\n"
            "<p>Item 2</p>\n"
            "<p>This is the first paragraph in item 2.</p>\n"
            "<p>This is the second paragraph in item 2.</p>\n"
            "<p>This is the third paragraph in item 2.</p>\n"
            "</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_preserve_numbers_with_paragraphs(self, md_custom):
        """Test preserve_numbers with paragraphs in list items."""
        md = md_custom(preserve_numbers=True)
        input = (
            "1. First item\n"
            "This is a paragraph in first item.\n"
            "2. Second item\n"
            "2. Another second item\n"
            "This is a paragraph in another second item.\n"
            "3. Third item"
        )
        expected = (
            "<ol>\n"
            '<li value="1">First item\n'
            "This is a paragraph in first item.</li>\n"
            '<li value="2">Second item</li>\n'
            '<li value="2">Another second item\n'
            "This is a paragraph in another second item.</li>\n"
            '<li value="3">Third item</li>\n'
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_multiple_paragraphs_with_preserve_numbers(self, md_custom):
        """Test preserve_numbers with multiple paragraphs in list items."""
        md = md_custom(preserve_numbers=True)
        input = (
            "1. First item\n"
            "\n"
            "  This is the first paragraph in first item.\n"
            "\n"
            "  This is the second paragraph in first item.\n"
            "\n"
            "2. Second item\n"
            "\n"
            "  This is the first paragraph in second item.\n"
            "\n"
            "2. Another second item\n"
            "\n"
            "  This is the first paragraph in another second item.\n"
            "\n"
            "  This is the second paragraph in another second item.\n"
            "\n"
            "3. Third item"
        )
        expected = (
            "<ol>\n"
            '<li value="1">\n'
            "<p>First item</p>\n"
            "<p>This is the first paragraph in first item.</p>\n"
            "<p>This is the second paragraph in first item.</p>\n"
            "</li>\n"
            '<li value="2">\n'
            "<p>Second item</p>\n"
            "<p>This is the first paragraph in second item.</p>\n"
            "</li>\n"
            '<li value="2">\n'
            "<p>Another second item</p>\n"
            "<p>This is the first paragraph in another second item.</p>\n"
            "<p>This is the second paragraph in another second item.</p>\n"
            "</li>\n"
            '<li value="3">\n'
            "<p>Third item</p>\n"
            "</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected
