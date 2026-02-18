"""Test for HTML in list items to ensure no codeblock creation."""

from tests.conftest import convert


class TestHtmlInLists:
    """Test that HTML elements in list items are preserved and not converted to code blocks."""

    def test_html_details_in_list_item(self, md):
        """Test that HTML details tag in list items doesn't become a code block."""
        input = \
"""* Testing html in list item `this is code`:

  <details markdown="1">
    <summary></summary>

  Hello test test hello

  </details>
  <br/>"""
        expected = \
"""<ul>
<li>
<p>Testing html in list item <code>this is code</code>:</p>
<details markdown="1">
    <summary></summary>

  Hello test test hello

  </details>
<p><br/></p>
</li>
</ul>"""
        result = convert(md, input)
        assert result == expected
        assert "<pre><code>" not in result

    def test_html_div_in_list_item(self, md):
        """Test that HTML div tag in list items doesn't become a code block."""
        input = \
"""* First item

  <div class="note">
  This is a note
  </div>

* Second item"""
        expected = \
"""<ul>
<li>
<p>First item</p>
<div class="note">
  This is a note
  </div>

</li>
</ul>
<ul>
<li>Second item</li>
</ul>"""
        result = convert(md, input)
        assert result == expected

    def test_multiple_html_blocks_in_list(self, md):
        """Test multiple HTML blocks within a list item."""
        input = \
"""1. First item with HTML:

   <div>First div</div>

   Some text between.

   <div>Second div</div>

2. Second item"""
        expected = \
"""<ol>
<li>
<p>First item with HTML:</p>
<div>First div</div>

<p>Some text between.</p>
<div>Second div</div>

</li>
<li>
<p>Second item</p>
</li>
</ol>"""
        result = convert(md, input)
        assert result == expected
