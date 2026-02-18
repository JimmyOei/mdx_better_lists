from tests.conftest import convert


class TestMarkerSeparation:
    """Test marker_separation configuration for unordered lists."""

    def test_marker_separation_enabled_default(self, md):
        """Test that default behavior separates different marker types."""
        input = "- Dash item\n" "+ Plus item\n" "* Star item"
        expected = (
            "<ul>\n"
            "<li>Dash item</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Plus item</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Star item</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_marker_separation_disabled(self, md_custom):
        """Test that disabling marker_separation allows mixed markers in same list."""
        md = md_custom(marker_separation=False)
        input = "- Dash item\n" "+ Plus item\n" "* Star item"
        expected = "<ul>\n" "<li>Dash item</li>\n" "<li>Plus item</li>\n" "<li>Star item</li>\n" "</ul>"
        result = convert(md, input)
        assert result == expected

    def test_marker_separation_same_marker_continues_list(self, md):
        """Test that same marker type continues the same list."""
        input = "- First dash\n" "- Second dash\n" "- Third dash"
        expected = "<ul>\n" "<li>First dash</li>\n" "<li>Second dash</li>\n" "<li>Third dash</li>\n" "</ul>"
        result = convert(md, input)
        assert result == expected

    def test_marker_separation_dash_to_plus(self, md):
        """Test separation when switching from dash to plus."""
        input = "- Dash item one\n" "- Dash item two\n" "+ Plus item one\n" "+ Plus item two"
        expected = (
            "<ul>\n"
            "<li>Dash item one</li>\n"
            "<li>Dash item two</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Plus item one</li>\n"
            "<li>Plus item two</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_marker_separation_dash_to_star(self, md):
        """Test separation when switching from dash to star."""
        input = "- Dash item\n" "* Star item"
        expected = "<ul>\n" "<li>Dash item</li>\n" "</ul>\n" "<ul>\n" "<li>Star item</li>\n" "</ul>"
        result = convert(md, input)
        assert result == expected

    def test_marker_separation_plus_to_star(self, md):
        """Test separation when switching from plus to star."""
        input = "+ Plus item\n" "* Star item"
        expected = "<ul>\n" "<li>Plus item</li>\n" "</ul>\n" "<ul>\n" "<li>Star item</li>\n" "</ul>"
        result = convert(md, input)
        assert result == expected

    def test_marker_separation_multiple_switches(self, md):
        """Test multiple marker switches."""
        input = "- Dash\n" "+ Plus\n" "- Dash again\n" "* Star\n" "- Dash once more"
        expected = (
            "<ul>\n"
            "<li>Dash</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Plus</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Dash again</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Star</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Dash once more</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_marker_separation_with_nested_lists(self, md):
        """Test marker separation with nested lists."""
        input = "- Outer dash\n" "  + Nested plus\n" "  + Another nested plus\n" "- Outer dash two\n" "+ Outer plus"
        expected = (
            "<ul>\n"
            "<li>Outer dash<ul>\n"
            "<li>Nested plus</li>\n"
            "<li>Another nested plus</li>\n"
            "</ul>\n"
            "</li>\n"
            "<li>Outer dash two</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Outer plus</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_marker_separation_disabled_with_nested(self, md_custom):
        """Test marker_separation=False with nested lists."""
        md = md_custom(marker_separation=False)
        input = "- Outer dash\n" "  + Nested plus\n" "* Outer star"
        expected = (
            "<ul>\n" "<li>Outer dash<ul>\n" "<li>Nested plus</li>\n" "</ul>\n" "</li>\n" "<li>Outer star</li>\n" "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_marker_separation_with_paragraphs(self, md):
        """Test marker separation with multi-paragraph items."""
        input = "- Dash item\n" "\n" "  Paragraph in dash item\n" "\n" "+ Plus item\n" "\n" "  Paragraph in plus item"
        expected = (
            "<ul>\n"
            "<li>\n"
            "<p>Dash item</p>\n"
            "<p>Paragraph in dash item</p>\n"
            "</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>\n"
            "<p>Plus item</p>\n"
            "<p>Paragraph in plus item</p>\n"
            "</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_marker_separation_explicit_paragraph_break(self, md):
        """Test that explicit paragraph breaks still separate lists."""
        input = "- Dash item\n" "\n" "Text between lists\n" "\n" "- Dash item again"
        expected = (
            "<ul>\n"
            "<li>Dash item</li>\n"
            "</ul>\n"
            "<p>Text between lists</p>\n"
            "<ul>\n"
            "<li>Dash item again</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected

    def test_marker_separation_complex_nested(self, md):
        """Test complex nested structure with marker separation."""
        input = (
            "- Outer dash one\n"
            "  * Nested star\n"
            "    + Deep nested plus\n"
            "    + Deep nested plus two\n"
            "  * Nested star two\n"
            "- Outer dash two\n"
            "+ Outer plus\n"
            "  - Nested dash\n"
            "* Outer star"
        )
        expected = (
            "<ul>\n"
            "<li>Outer dash one<ul>\n"
            "<li>Nested star<ul>\n"
            "<li>Deep nested plus</li>\n"
            "<li>Deep nested plus two</li>\n"
            "</ul>\n"
            "</li>\n"
            "<li>Nested star two</li>\n"
            "</ul>\n"
            "</li>\n"
            "<li>Outer dash two</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Outer plus<ul>\n"
            "<li>Nested dash</li>\n"
            "</ul>\n"
            "</li>\n"
            "</ul>\n"
            "<ul>\n"
            "<li>Outer star</li>\n"
            "</ul>"
        )
        result = convert(md, input)
        assert result == expected
