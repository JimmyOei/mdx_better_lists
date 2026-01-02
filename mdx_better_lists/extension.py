"""
Extension module for mdx_better_lists.

Based on patterns from:
https://github.com/radude/mdx_truly_sane_lists
https://python-markdown.github.io/extensions/sane_lists/
"""

import re
from markdown import Extension
from markdown.blockprocessors import OListProcessor, ListIndentProcessor, BlockProcessor
from xml.etree import ElementTree as etree


class BetterListMixin(BlockProcessor):
    """Mixin for list processors to set custom tab_length."""
    better_list_tab_length = 2
    better_list_preserve_numbers = False

    def __init__(self, parser):
        super(BetterListMixin, self).__init__(parser)
        self.tab_length = self.better_list_tab_length
        self.preserve_numbers = self.better_list_preserve_numbers


class BetterListIndentProcessor(ListIndentProcessor, BetterListMixin):
    """ListIndentProcessor."""

    def __init__(self, *args):
        super(BetterListIndentProcessor, self).__init__(*args)


class BetterOListProcessor(OListProcessor, BetterListMixin):
    """OList processor."""

    def __init__(self, *args, **kwargs):
        super(BetterOListProcessor, self).__init__(*args, **kwargs)
        # Override CHILD_RE with tab_length-aware pattern (from sane_lists)
        self.CHILD_RE = re.compile(r'^[ ]{0,%d}((\d+\.))[ ]+(.*)' % (self.tab_length - 1))

    def run(self, parent, blocks):
        """Process ordered list with proper nested item handling."""
        block = blocks.pop(0)

        # Create iterator for block lines to extract numbers on-demand, if preserve_numbers is enabled
        block_lines = iter(block.split('\n')) if (self.preserve_numbers and self.TAG == "ol") else None

        items = self.get_items(block)

        if parent.tag in ["ol", "ul"]:
            lst = parent
        else:
            lst = etree.SubElement(parent, self.TAG)

            # Handle start attribute for non-1 starting lists
            if self.STARTSWITH and self.STARTSWITH != "1":
                lst.attrib["start"] = self.STARTSWITH

        self.parser.state.set("list")
        for item in items:
            if item.startswith(" " * self.tab_length):
                # Nested/continuation item
                self.parser.parseBlocks(lst[-1], [item])
            else:
                # New list item
                li = etree.SubElement(lst, "li")

                # Extract number from marker if preserve_numbers is enabled
                if block_lines:
                    for line in block_lines:
                        match = self.CHILD_RE.match(line)
                        if match:
                            number = match.group(2).rstrip('.')
                            li.attrib["value"] = number
                            break

                self.parser.parseBlocks(li, [item])
        self.parser.state.reset()


class BetterUListProcessor(BetterOListProcessor, BetterListMixin):
    """UList processor with custom tab_length - inherits run() from BetterOListProcessor."""
    TAG = "ul"

    def __init__(self, parser):
        super(BetterUListProcessor, self).__init__(parser)
        # Override RE and CHILD_RE with tab_length-aware patterns (from sane_lists)
        self.RE = re.compile(r'^[ ]{0,%d}[*+-][ ]+(.*)' % (self.tab_length - 1))
        self.CHILD_RE = re.compile(r'^[ ]{0,%d}(([*+-]))[ ]+(.*)' % (self.tab_length - 1))


class BetterListsExtension(Extension):
    """Python-Markdown extension for better list handling."""

    def __init__(self, **kwargs):
        self.config = {
            'nested_indent': [
                2,
                'Number of spaces for nested list indentation (default: 2)'
            ],
            'preserve_numbers': [
                False,
                'Preserve exact list numbers from markdown (default: False)'
            ],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        """Register the extension with the Markdown instance."""

        nested_indent = self.getConfig('nested_indent')
        preserve_numbers = self.getConfig('preserve_numbers')

        # Set the class variable for tab_length on the mixin
        BetterListMixin.better_list_tab_length = nested_indent
        BetterListMixin.better_list_preserve_numbers = preserve_numbers

        # Replace default OList and UList processors with our custom versions
        md.parser.blockprocessors.deregister('olist')
        md.parser.blockprocessors.register(
            BetterOListProcessor(md.parser), 'olist', 50
        )

        md.parser.blockprocessors.deregister('ulist')
        md.parser.blockprocessors.register(
            BetterUListProcessor(md.parser), 'ulist', 40
        )

        # Replace indent processor with custom version
        md.parser.blockprocessors.deregister('indent')
        md.parser.blockprocessors.register(
            BetterListIndentProcessor(md.parser), 'indent', 95
        )