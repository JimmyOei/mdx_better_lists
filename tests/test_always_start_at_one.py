from tests.conftest import convert


class TestAlwaysStartAtOne:
    """Test always_start_at_one configuration for ordered lists."""

    def test_always_start_at_one_disabled_default(self, md):
        """Test that default behavior preserves start attribute for non-1 starts."""
        input = "5. Fifth item\n" "6. Sixth item\n" "7. Seventh item"
        expected = '<ol start="5">\n' "<li>Fifth item</li>\n" "<li>Sixth item</li>\n" "<li>Seventh item</li>\n" "</ol>"
        result = convert(md, input)
        assert result == expected

    def test_always_start_at_one_enabled(self, md_custom):
        """Test that always_start_at_one forces lists to start at 1."""
        md = md_custom(always_start_at_one=True)
        input = "5. Fifth item\n" "6. Sixth item\n" "7. Seventh item"
        expected = "<ol>\n" "<li>Fifth item</li>\n" "<li>Sixth item</li>\n" "<li>Seventh item</li>\n" "</ol>"
        result = convert(md, input)
        assert result == expected

    def test_always_start_at_one_with_nested_lists(self, md_custom):
        """Test always_start_at_one with nested ordered lists."""
        md = md_custom(always_start_at_one=True)
        input = "3. Third item\n" "  5. Nested fifth\n" "  6. Nested sixth\n" "4. Fourth item"
        expected = (
            "<ol>\n"
            "<li>Third item<ol>\n"
            "<li>Nested fifth</li>\n"
            "<li>Nested sixth</li>\n"
            "</ol>\n"
            "</li>\n"
            "<li>Fourth item</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected

    def test_always_start_at_one_off_with_nested_lists(self, md):
        """Test always_start_at_one with nested ordered lists."""
        input = "3. Third item\n" "  5. Nested fifth\n" "  6. Nested sixth\n" "4. Fourth item"
        expected = (
            '<ol start="3">\n'
            '<li>Third item<ol start="5">\n'
            "<li>Nested fifth</li>\n"
            "<li>Nested sixth</li>\n"
            "</ol>\n"
            "</li>\n"
            "<li>Fourth item</li>\n"
            "</ol>"
        )
        result = convert(md, input)
        assert result == expected
