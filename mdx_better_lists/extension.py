"""
Extension module for mdx_better_lists.

Based on patterns from:
https://github.com/radude/mdx_truly_sane_lists
https://python-markdown.github.io/extensions/sane_lists/
"""

import re
from markdown import Extension
from markdown.blockprocessors import OListProcessor, ListIndentProcessor, BlockProcessor, ParagraphProcessor
from markdown.preprocessors import Preprocessor
from xml.etree import ElementTree as etree


class BetterListPreprocessor(Preprocessor):
    """Preprocessor to handle block splitting (currently disabled)."""
    
    def __init__(self, md, tab_length=2):
        super().__init__(md)
        self.tab_length = tab_length
    
    def run(self, lines):
        """Pass through - block splitting is handled by processors."""
        return lines


class BetterListMixin(BlockProcessor):
    """Mixin for list processors to set custom tab_length."""
    better_list_tab_length = 2
    better_list_preserve_numbers = False
    always_start_at_one = False
    marker_separation = True

    def __init__(self, parser):
        super(BetterListMixin, self).__init__(parser)
        self.tab_length = self.better_list_tab_length
        self.preserve_numbers = self.better_list_preserve_numbers
        self.always_start_at_one = self.always_start_at_one
        self.marker_separation = self.marker_separation


class BetterListIndentProcessor(ListIndentProcessor, BetterListMixin):
    """ListIndentProcessor that can recognize nested lists within indented blocks."""

    def __init__(self, *args):
        super(BetterListIndentProcessor, self).__init__(*args)
        # Pattern to detect list markers at the start of a line (after indentation)
        self.LIST_MARKER_RE = re.compile(r'^[ ]*([*+-]|\d+\.)[ ]+')

    def run(self, parent, blocks):
        block = blocks[0]

        # Check if this indented block contains lines with insufficient indentation
        lines = block.split('\n')
        split_idx = -1

        for i, line in enumerate(lines):
            # Skip empty lines
            if not line.strip():
                continue

            # Check if line doesn't have proper indentation (should have at least tab_length spaces)
            if not line.startswith(' ' * self.tab_length):
                # This line doesn't belong in an indented block
                split_idx = i
                break

        # If we found improperly indented content, split it out
        if split_idx > 0:
            before_split = '\n'.join(lines[:split_idx])
            after_split = '\n'.join(lines[split_idx:])
            blocks[0] = before_split
            blocks.insert(1, after_split)
        
        # Check if this indented block contains list markers after splitting
        block = blocks[0]
        lines = block.split('\n')
        has_list_marker = False
        first_list_line_idx = -1
        
        for i, line in enumerate(lines):
            # Remove leading indentation (up to tab_length spaces)
            dedented_line = line[self.tab_length:] if line.startswith(' ' * self.tab_length) else line
            if self.LIST_MARKER_RE.match(dedented_line):
                has_list_marker = True
                first_list_line_idx = i
                break
        
        # If we found a list marker, split the block at that point
        if has_list_marker and first_list_line_idx > 0:
            before_list = '\n'.join(lines[:first_list_line_idx])
            from_list = '\n'.join(lines[first_list_line_idx:])
            
            blocks[0] = before_list
            blocks.insert(1, from_list)
        
        super(BetterListIndentProcessor, self).run(parent, blocks)

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

        # Check for sibling list to continue
        sibling = self.lastChild(parent)

        if parent.tag in ["ol", "ul"]:
            # Nested list - use parent
            lst = parent
        elif sibling is not None and sibling.tag == self.TAG:
            # Continue the sibling list
            lst = sibling
        else:
            # Create new list
            lst = etree.SubElement(parent, self.TAG)

            # Handle start attribute for non-1 starting lists
            if not self.always_start_at_one and self.STARTSWITH and self.STARTSWITH != "1":
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
        # Track markers for each list element (using id() as key)
        self.list_markers = {}

    def run(self, parent, blocks):
        """Process unordered list with marker separation support."""
        block = blocks.pop(0)

        # Extract the marker type from the first line
        first_line = block.split('\n')[0]
        match = self.CHILD_RE.match(first_line)
        current_marker = match.group(2) if match else None

        # If marker_separation is enabled, split block by marker type
        if self.marker_separation and current_marker:
            lines = block.split('\n')
            same_marker_lines = []
            different_marker_lines = []
            in_same_marker = True

            for line in lines:
                if not line.strip():
                    # Empty line
                    if in_same_marker:
                        same_marker_lines.append(line)
                    else:
                        different_marker_lines.append(line)
                    continue

                line_match = self.CHILD_RE.match(line)
                if line_match:
                    line_marker = line_match.group(2)
                    if line_marker == current_marker:
                        if in_same_marker:
                            same_marker_lines.append(line)
                        else:
                            # We've hit a line with the original marker after switching
                            # This should be a new list, so add to different markers
                            different_marker_lines.append(line)
                    else:
                        # Different marker - split here
                        in_same_marker = False
                        different_marker_lines.append(line)
                elif line.startswith(' ' * self.tab_length):
                    # Indented line - continuation of current item
                    if in_same_marker:
                        same_marker_lines.append(line)
                    else:
                        different_marker_lines.append(line)
                else:
                    # Non-list line
                    if in_same_marker:
                        same_marker_lines.append(line)
                    else:
                        different_marker_lines.append(line)

            # Reconstruct block with only same-marker items
            block = '\n'.join(same_marker_lines)

            # Put different-marker items back for next processing
            if different_marker_lines:
                blocks.insert(0, '\n'.join(different_marker_lines))

        items = self.get_items(block)

        sibling = self.lastChild(parent)

        if parent.tag in ["ol", "ul"]:
            # Nested list - use parent
            lst = parent
        elif sibling is not None and sibling.tag == self.TAG:
            # Check if we should continue the sibling list
            sibling_marker = self.list_markers.get(id(sibling), None) if self.marker_separation else None

            # If marker_separation is enabled and markers differ, create new list
            if self.marker_separation and sibling_marker and current_marker and sibling_marker != current_marker:
                lst = etree.SubElement(parent, self.TAG)
            else:
                # Continue the sibling list
                lst = sibling
        else:
            # Create new list
            lst = etree.SubElement(parent, self.TAG)

        if current_marker and self.marker_separation:
            self.list_markers[id(lst)] = current_marker

        self.parser.state.set("list")
        for item in items:
            if item.startswith(" " * self.tab_length):
                # Nested/continuation item
                self.parser.parseBlocks(lst[-1], [item])
            else:
                # New list item
                li = etree.SubElement(lst, "li")
                self.parser.parseBlocks(li, [item])
        self.parser.state.reset()
        
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
            'always_start_at_one': [
                False,
                'Always start ordered lists at 1 (default: False)'
            ],
            'marker_separation': [
                True,
                'Ensure different marker types (-, *, +) generate separate lists (default: True)'
            ]
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        """Register the extension with the Markdown instance."""

        nested_indent = self.getConfig('nested_indent')
        preserve_numbers = self.getConfig('preserve_numbers')
        always_start_at_one = self.getConfig('always_start_at_one')
        marker_separation = self.getConfig('marker_separation')

        BetterListMixin.better_list_tab_length = nested_indent
        BetterListMixin.better_list_preserve_numbers = preserve_numbers
        BetterListMixin.always_start_at_one = always_start_at_one
        BetterListMixin.marker_separation = marker_separation

        md.preprocessors.register(
            BetterListPreprocessor(md, nested_indent), 'better_list_prep', 25
        )

        md.parser.blockprocessors.deregister('olist')
        md.parser.blockprocessors.register(
            BetterOListProcessor(md.parser), 'olist', 50
        )

        md.parser.blockprocessors.deregister('ulist')
        md.parser.blockprocessors.register(
            BetterUListProcessor(md.parser), 'ulist', 40
        )

        md.parser.blockprocessors.deregister('indent')
        md.parser.blockprocessors.register(
            BetterListIndentProcessor(md.parser), 'indent', 95
        )