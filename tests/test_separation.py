from tests.conftest import convert


class TestListSeparation:
    """Test list separation behavior."""

    def test_blank_line_lists(self, md):
        text = "- List 1 First\n" "- List 1 Second\n" "\n" "- List 1 Third\n" "- List 1 Fourth"
        expected = (
            "<ul>\n"
            "<li>List 1 First</li>\n"
            "<li>List 1 Second</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>List 1 Third</li>\n"
            "<li>List 1 Fourth</li>\n"
            "</ul>"
        )
        result = convert(md, text)
        assert result == expected

    def test_multiple_blank_lines_lists(self, md):
        text = "1. List A First\n" "2. List A Second\n" "\n" "\n" "\n" "3. List A Third\n" "\n" "\n" "4. List A Fourth"
        expected = (
            "<ol>\n"
            "<li>List A First</li>\n"
            "<li>\n"
            "<p>List A Second</p>\n"
            "</li>\n"
            "<li>\n"
            "<p>List A Third</p>\n"
            "</li>\n"
            "<li>\n"
            "<p>List A Fourth</p>\n"
            "</li>\n"
            "</ol>"
        )
        result = convert(md, text)
        assert result == expected

    def test_heading_separates_lists(self, md):
        text = "* List X First\n" "* List X Second\n" "# Heading Between Lists\n" "* List Y First\n" "* List Y Second"
        expected = (
            "<ul>\n"
            "<li>List X First</li>\n"
            "<li>List X Second</li>\n"
            "</ul>\n"
            "<h1>Heading Between Lists</h1>\n"
            "<ul>\n"
            "<li>List Y First</li>\n"
            "<li>List Y Second</li>\n"
            "</ul>"
        )
        result = convert(md, text)
        assert result == expected

    def test_list_then_paragraph_then_list(self, md):
        input = (
            "- List A first list item\n"
            "- List A second list item\n"
            "\n"
            "This is a paragraph between lists.\n"
            "\n"
            "- List B first list item\n"
            "- List B second list item"
        )
        expected = (
            "<ul>\n"
            "<li>List A first list item</li>\n"
            "<li>List A second list item</li>\n"
            "</ul>\n"
            "<p>This is a paragraph between lists.</p>\n"
            "<ul>\n"
            "<li>List B first list item</li>\n"
            "<li>List B second list item</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_paragraph_then_list(self, md):
        input = "This is a paragraph before the list.\n" "\n" "- List item 1\n" "- List item 2"
        expected = (
            "<p>This is a paragraph before the list.</p>\n"
            "<ul>\n"
            "<li>List item 1</li>\n"
            "<li>List item 2</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_list_then_paragraph(self, md):
        input = "- List item 1\n" "- List item 2\n" "\n" "This is a paragraph after the list."
        expected = (
            "<ul>\n"
            "<li>List item 1</li>\n"
            "<li>List item 2</li>\n"
            "</ul>\n"
            "<p>This is a paragraph after the list.</p>"
        )
        result = convert(md, input)
        assert result == expected

    def test_heading(self, md):
        input = (
            "# Heading\n"
            "\n"
            "- List item 1\n"
            "- List item 2\n"
            "\n"
            "Regular paragraph.\n"
            "\n"
            "1. Ordered item 1\n"
            "2. Ordered item 2"
        )
        expected = (
            "<h1>Heading</h1>\n"
            "<ul>\n"
            "<li>List item 1</li>\n"
            "<li>List item 2</li>\n"
            "</ul>\n"
            "<p>Regular paragraph.</p>\n"
            "<ol>\n"
            "<li>Ordered item 1</li>\n"
            "<li>Ordered item 2</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_preserve_numbers_with_separated_lists(self, md_custom):
        """Test preserve_numbers with separated lists."""
        md = md_custom(preserve_numbers=True)
        input = (
            "1. First list item\n"
            "2. Second list item\n"
            "2. Another second\n"
            "\n"
            "This is a paragraph separating lists.\n"
            "\n"
            "3. New list first item\n"
            "3. New list second item\n"
            "5. New list third item"
        )
        expected = (
            "<ol>\n"
            '<li value="1">First list item</li>\n'
            '<li value="2">Second list item</li>\n'
            '<li value="2">Another second</li>\n'
            "</ol>\n"
            "<p>This is a paragraph separating lists.</p>\n"
            '<ol start="3">\n'
            '<li value="3">New list first item</li>\n'
            '<li value="3">New list second item</li>\n'
            '<li value="5">New list third item</li>\n'
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected
