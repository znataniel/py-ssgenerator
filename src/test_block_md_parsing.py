import unittest
from block_md_parsing import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_para,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_ul,
    block_type_ol,
)


class TestMd2Blocks(unittest.TestCase):
    def test_sample(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item",
        ]
        self.assertEqual(expected, markdown_to_blocks(md))

    def test_many_new_lines(self):
        md = "# Heading\n\n\n\n*List\n*List\n*List"
        expected = ["# Heading", "*List\n*List\n*List"]
        self.assertEqual(expected, markdown_to_blocks(md))

    if __name__ == "__main__":
        unittest.main()


class TestBlockType(unittest.TestCase):
    def test_heading(self):
        blocks = [
            "# Heading",
            "## Heading",
            "### Heading",
            "#### Heading",
            "##### Heading",
            "###### Heading",
            "########## Heading",
            "####Heading",
        ]
        expected = [
            block_type_heading,
            block_type_heading,
            block_type_heading,
            block_type_heading,
            block_type_heading,
            block_type_heading,
            block_type_para,
            block_type_para,
        ]
        self.assertEqual(expected, [block_to_block_type(bl) for bl in blocks])

    def test_code(self):
        blocks = [
            """```
            This is code
                ```""",
            """```This is code also
                ```""",
            """```
                This is code too```""",
            "```We all code```",
            """``
                This ain't code
                ```""",
            """```
                This ain't codeeither
                `""",
        ]
        expected = [
            block_type_code,
            block_type_code,
            block_type_code,
            block_type_code,
            block_type_para,
            block_type_para,
        ]
        self.assertEqual(expected, [block_to_block_type(bl) for bl in blocks])

    def test_quote(self):
        blocks = [
            "> quote",
            """> Many quotes
> Many quotes
> Many quotes""",
            """> quote
> quote
>quote""",
            """> quote
> quote
# Not a quote""",
        ]
        expected = [
            block_type_quote,
            block_type_quote,
            block_type_quote,
            block_type_para,
        ]
        self.assertEqual(expected, [block_to_block_type(bl) for bl in blocks])

    if __name__ == "__main__":
        unittest.main()

    def test_ul(self):
        blocks = [
            "* single element",
            "- single element",
            "*- not an element",
            """* element
* element
* element""",
            """- element
- element
- element""",
            """* element
- element
- element""",
            """* element
element
- element""",
        ]
        expected = [
            block_type_ul,
            block_type_ul,
            block_type_para,
            block_type_ul,
            block_type_ul,
            block_type_para,
            block_type_para,
        ]
        self.assertEqual(expected, [block_to_block_type(bl) for bl in blocks])

    def test_ol(self):
        blocks = [
            "1. li",
            "1. li\n2. li\n3. li",
            "1. li\n4. li\n3. li",
            "1. li\n* li\n3. li",
        ]
        expected = [
            block_type_ol,
            block_type_ol,
            block_type_para,
            block_type_para,
        ]
        self.assertEqual(expected, [block_to_block_type(bl) for bl in blocks])

    def test_para(self):
        blocks = ["Lorem ipsum sit amet, qui adipisicing minim sint cupidatat."]
        expected = [block_type_para]
        self.assertEqual(expected, [block_to_block_type(bl) for bl in blocks])
