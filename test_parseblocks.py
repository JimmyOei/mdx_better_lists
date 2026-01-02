#!/usr/bin/env python3
"""Test what happens when we pass indented content to parseBlocks."""

import markdown

md = markdown.Markdown(
    extensions=['mdx_better_lists'],
    extension_configs={
        'mdx_better_lists': {
            'preserve_numbers': True
        }
    }
)

# Simulate what parseBlocks receives for the nested item
indented_content = """  - Subitem one
  - Subitem two"""

print("Testing with indented content:")
print(repr(indented_content))
print()

# Create a simple list item to parse into
from xml.etree import ElementTree as etree
parent = etree.Element('li')

# Parse the indented content
md.parser.parseBlocks(parent, [indented_content])

# See what we got
result = etree.tostring(parent, encoding='unicode', method='html')
print("Result:")
print(result)
print()

# Now test with dedented content
md.reset()
dedented_content = """- Subitem one
- Subitem two"""

print("Testing with dedented content:")
print(repr(dedented_content))
print()

parent2 = etree.Element('li')
md.parser.parseBlocks(parent2, [dedented_content])

result2 = etree.tostring(parent2, encoding='unicode', method='html')
print("Result:")
print(result2)
