from tests.conftest import convert


class TestPreserveNumbers:
    """Test preserve_numbers configuration for ordered lists."""

    def test_preserve_numbers_disabled(self, md):
        """Test that default behavior doesn't preserve numbers."""
        input = "1. First\n" "2. Second\n" "2. Another second\n" "2. Yet another second\n" "3. Third"
        expected = (
            "<ol>\n"
            "<li>First</li>\n"
            "<li>Second</li>\n"
            "<li>Another second</li>\n"
            "<li>Yet another second</li>\n"
            "<li>Third</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_preserve_numbers_enabled(self, md_custom):
        """Test that preserve_numbers config preserves exact numbers."""
        md = md_custom(preserve_numbers=True)
        input = (
            "1. First\n" "2. Second\n" "2. Another second\n" "2. Yet another second\n" "3. Third\n" "3. Another third"
        )
        expected = (
            "<ol>\n"
            '<li value="1">First</li>\n'
            '<li value="2">Second</li>\n'
            '<li value="2">Another second</li>\n'
            '<li value="2">Yet another second</li>\n'
            '<li value="3">Third</li>\n'
            '<li value="3">Another third</li>\n'
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_preserve_numbers_non_sequential(self, md_custom):
        """Test preserve_numbers with non-sequential numbers."""
        md = md_custom(preserve_numbers=True)
        input = "1. First\n" "5. Fifth\n" "5. Another fifth\n" "10. Tenth"
        expected = (
            "<ol>\n"
            '<li value="1">First</li>\n'
            '<li value="5">Fifth</li>\n'
            '<li value="5">Another fifth</li>\n'
            '<li value="10">Tenth</li>\n'
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_preserve_numbers_starting_not_at_one(self, md_custom):
        """Test preserve_numbers with list starting at non-1."""
        md = md_custom(preserve_numbers=True)
        input = "7. Seventh\n" "7. Another seventh\n" "8. Eighth"
        expected = (
            '<ol start="7">\n'
            '<li value="7">Seventh</li>\n'
            '<li value="7">Another seventh</li>\n'
            '<li value="8">Eighth</li>\n'
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_preserve_numbers_complex(self, md_custom):
        """Test preserve_numbers with complex list."""
        md = md_custom(preserve_numbers=True)
        input = (
            "3. Item three\n"
            "\n"
            "  First paragraph in item three.\n"
            "\n"
            "  Second paragraph in item three.\n"
            "\n"
            "4. Item four in a new list\n"
            "  Paragraph in item four\n"
            "  that spans multiple\n"
            "  lines.\n"
            "\n"
            "  And another paragraph with a list:\n"
            "  - Subitem one\n"
            "  - Subitem two\n"
            "    * Sub-subitem\n"
            "      1. Deep item one\n"
            "      1. Deep item one again\n"
            "      2. Deep item two\n"
            "  - Subitem three\n"
            "5. Item five\n"
            "\n"
            "1. And a new list\n"
            "2. Continuing the new list\n"
            "2. Another two\n"
            "3. Ending the new list"
        )
        expected = (
            '<ol start="3">\n'
            '<li value="3">\n'
            "<p>Item three</p>\n"
            "<p>First paragraph in item three.</p>\n"
            "<p>Second paragraph in item three.</p>\n"
            "</li>\n"
            '<li value="4">\n'
            "<p>Item four in a new list\n"
            "  Paragraph in item four\n"
            "  that spans multiple\n"
            "  lines.</p>\n"
            "<p>And another paragraph with a list:</p>\n"
            "<ul>\n"
            "<li>Subitem one</li>\n"
            "<li>Subitem two<ul>\n"
            "<li>Sub-subitem<ol>\n"
            '<li value="1">Deep item one</li>\n'
            '<li value="1">Deep item one again</li>\n'
            '<li value="2">Deep item two</li>\n'
            "</ol>\n"
            "</li>\n"
            "</ul>\n"
            "</li>\n"
            "<li>Subitem three</li>\n"
            "</ul>\n"
            "</li>\n"
            '<li value="5">\n'
            "<p>Item five</p>\n"
            "</li>\n"
            '<li value="1">\n'
            "<p>And a new list</p>\n"
            "</li>\n"
            '<li value="2">Continuing the new list</li>\n'
            '<li value="2">Another two</li>\n'
            '<li value="3">Ending the new list</li>\n'
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected
