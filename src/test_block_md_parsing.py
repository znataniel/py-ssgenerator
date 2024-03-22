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
    markdown_to_html_node,
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

    if __name__ == "__main__":
        unittest.main()


class TestMd2HtmlNode(unittest.TestCase):
    def test_mix1(self):
        md = """### This is a heading

* This is element 1 of ul
* This is element 2 of ul
* This is element 3 of ul
* This is element 4 of ul
* This is element 5 of ul

And this is a regular paragraph with `inline code`"""
        expected = "<div><h3>This is a heading</h3><ul><li>This is element 1 of ul</li><li>This is element 2 of ul</li><li>This is element 3 of ul</li><li>This is element 4 of ul</li><li>This is element 5 of ul</li></ul><p>And this is a regular paragraph with <code>inline code</code></p></div>"
        self.assertEqual(expected, markdown_to_html_node(md).to_html())

    def test_mix2(self):
        md = """### This is a heading

1. This is element 1 of ul
2. This is element 2 of ul
3. This is element 3 of ul
4. This is element 4 of ul
5. This is element 5 of ul

And this is a regular paragraph with `inline code`"""
        expected = "<div><h3>This is a heading</h3><ol><li>This is element 1 of ul</li><li>This is element 2 of ul</li><li>This is element 3 of ul</li><li>This is element 4 of ul</li><li>This is element 5 of ul</li></ol><p>And this is a regular paragraph with <code>inline code</code></p></div>"
        self.assertEqual(expected, markdown_to_html_node(md).to_html())

    def test_mix2(self):
        self.maxDiff = None
        md = """### This is a heading

* This is element 1 of ul
* This is element 2 of ul
* This is element 3 of ul
* This is element 4 of ul
* This is element 5 of ul

1. This is element 1 of ol
2. This is element 2 of ol
3. This is element 3 of ol
4. This is element 4 of ol
5. This is element 5 of ol

And this is a regular paragraph with `inline code`, some **bold text**,
some *italic text*, an ![image](https://image.url)
and a [link, just for fun.](https://justfor.fun)"""
        # expected = "<div><h3>This is a heading</h3><ol><li>This is element 1 of ul</li><li>This is element 2 of ul</li><li>This is element 3 of ul</li><li>This is element 4 of ul</li><li>This is element 5 of ul</li></ol><p>And this is a regular paragraph with <code>inline code</code></p></div>"
        expected = """<div>
<h3>This is a heading</h3>
<ul>
<li>This is element 1 of ul</li>
<li>This is element 2 of ul</li>
<li>This is element 3 of ul</li>
<li>This is element 4 of ul</li>
<li>This is element 5 of ul</li>
</ul>
<ol>
<li>This is element 1 of ol</li>
<li>This is element 2 of ol</li>
<li>This is element 3 of ol</li>
<li>This is element 4 of ol</li>
<li>This is element 5 of ol</li>
</ol>
<p>
And this is a regular paragraph with <code>inline code</code>, some <b>bold text</b>,
 some <i>italic text</i>, an <img src="https://image.url" alt="image"></img>
 and a <a href="https://justfor.fun">link, just for fun.</a>
</p>
</div>"""
        self.assertEqual(
            "".join(expected.split("\n")), markdown_to_html_node(md).to_html()
        )

    if __name__ == "__main__":
        unittest.main()
