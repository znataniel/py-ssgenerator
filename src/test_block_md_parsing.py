import unittest
from block_md_parsing import (
    markdown_to_blocks,
)


class TestMd2Blocks(unittest.TestCase):
    def test_sample(self):
        md = "# This is a heading\n\nThis is a paragraph of text. It has some **bold** and *italic* words inside of it.\n\n* This is a list item\n* This is another list item"
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
