import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)
from inline_md_parsing import (
    split_nodes_delimiter,
    extract_markdown_links,
    extract_markdown_images,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestSplitNodesFn(unittest.TestCase):
    def test_bold_delimiter(self):
        input_nodes = [
            TextNode("H*T*B", text_type_text),
            TextNode("E*Q*H", text_type_text),
        ]
        expected_output = [
            TextNode("H", text_type_text),
            TextNode("T", text_type_bold),
            TextNode("B", text_type_text),
            TextNode("E", text_type_text),
            TextNode("Q", text_type_bold),
            TextNode("H", text_type_text),
        ]
        self.assertEqual(
            expected_output, split_nodes_delimiter(input_nodes, "*", text_type_bold)
        )

    def test_two_bold_delimiter(self):
        input_nodes = [
            TextNode("H*T*B*P*", text_type_text),
            TextNode("E*Q*H", text_type_text),
        ]
        expected_output = [
            TextNode("H", text_type_text),
            TextNode("T", text_type_bold),
            TextNode("B", text_type_text),
            TextNode("P", text_type_bold),
            TextNode("E", text_type_text),
            TextNode("Q", text_type_bold),
            TextNode("H", text_type_text),
        ]
        self.assertEqual(
            expected_output, split_nodes_delimiter(input_nodes, "*", text_type_bold)
        )

    def test_double_two_bold_delimiter(self):
        input_nodes = [
            TextNode("H*T*B*P*", text_type_text),
            TextNode("E*Q*H*X*", text_type_text),
        ]
        expected_output = [
            TextNode("H", text_type_text),
            TextNode("T", text_type_bold),
            TextNode("B", text_type_text),
            TextNode("P", text_type_bold),
            TextNode("E", text_type_text),
            TextNode("Q", text_type_bold),
            TextNode("H", text_type_text),
            TextNode("X", text_type_bold),
        ]
        self.assertEqual(
            expected_output, split_nodes_delimiter(input_nodes, "*", text_type_bold)
        )

    def test_code_mixed_delimiter(self):
        input_nodes = [
            TextNode("H*T`*B*`P*", text_type_text),
            TextNode("E*_Q*H_*X*", text_type_text),
        ]
        expected_output = [
            TextNode("H*T", text_type_text),
            TextNode("*B*", text_type_code),
            TextNode("P*", text_type_text),
            TextNode("E*_Q*H_*X*", text_type_text),
        ]
        self.assertEqual(
            expected_output, split_nodes_delimiter(input_nodes, "`", text_type_code)
        )

    def test_multiple_character_delimiter(self):
        input_nodes = [
            TextNode("H*T*C", text_type_text),
            TextNode("E__XD__A", text_type_text),
        ]
        expected_output = [
            TextNode("H*T*C", text_type_text),
            TextNode("E", text_type_text),
            TextNode("XD", text_type_bold),
            TextNode("A", text_type_text),
        ]
        self.assertEqual(
            expected_output, split_nodes_delimiter(input_nodes, "__", text_type_bold)
        )

    def test_split_error1(self):
        input_nodes = [
            TextNode("H*T`*B*`P*", text_type_text),
            TextNode("E`*_Q*H_*X*", text_type_text),
        ]
        self.assertRaises(
            Exception,
            split_nodes_delimiter,
            input_nodes,
            "`",
            text_type_code,
        )

    def test_split_error2(self):
        input_nodes = [
            TextNode("H*T`*B*`P*`", text_type_text),
        ]
        self.assertRaises(
            Exception,
            split_nodes_delimiter,
            input_nodes,
            "`",
            text_type_code,
        )

    def test_split_error3(self):
        input_nodes = [
            TextNode("H*T*C", text_type_text),
            TextNode("E__XD_A", text_type_text),
        ]
        self.assertRaises(
            Exception,
            split_nodes_delimiter,
            input_nodes,
            "__",
            text_type_bold,
        )

    if __name__ == "__main__":
        unittest.main()


class TestExtractImgLinkFn(unittest.TestCase):
    def test_img_1(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        expected_output = [
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("another", "https://i.imgur.com/dfsdkjfd.png"),
        ]
        self.assertEqual(expected_output, extract_markdown_images(text))

    def test_link_1(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected_output = [
            ("link", "https://www.example.com"),
            ("another", "https://www.example.com/another"),
        ]
        self.assertEqual(expected_output, extract_markdown_links(text))

    if __name__ == "__main__":
        unittest.main()


class TestSplitNodesImg(unittest.TestCase):
    def test_equal_two_img(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode(
                "second image", text_type_image, "https://i.imgur.com/3elNhQu.png"
            ),
        ]
        self.assertEqual(expected, split_nodes_image([node]))

    def test_equal_image_last(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(expected, split_nodes_image([node]))

    def test_equal_image_first(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) this is text",
            text_type_text,
        )
        expected = [
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" this is text", text_type_text),
        ]
        self.assertEqual(expected, split_nodes_image([node]))

    if __name__ == "__main__":
        unittest.main()


class TestSplitNodesLink(unittest.TestCase):
    def test_equal_two_link(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            text_type_text,
        )
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_link, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode("second image", text_type_link, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertEqual(expected, split_nodes_link([node]))

    def test_equal_link_last(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png)",
            text_type_text,
        )
        expected = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_link, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertEqual(expected, split_nodes_link([node]))

    def test_equal_link_first(self):
        node = TextNode(
            "[image](https://i.imgur.com/zjjcJKZ.png) this is text",
            text_type_text,
        )
        expected = [
            TextNode("image", text_type_link, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" this is text", text_type_text),
        ]
        self.assertEqual(expected, split_nodes_link([node]))

    if __name__ == "__main__":
        unittest.main()


class TestTxtToTxtnode(unittest.TestCase):
    def test_mix_1(self):
        self.maxDiff = None
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(expected, text_to_textnodes(text))

    def test_mix_2(self):
        self.maxDiff = None
        text = "This is **text** with **another bold** word and another **BOOOLD** and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with ", text_type_text),
            TextNode("another bold", text_type_bold),
            TextNode(" word and another ", text_type_text),
            TextNode("BOOOLD", text_type_bold),
            TextNode(" and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(expected, text_to_textnodes(text))

    def test_no_text_type(self):
        self.maxDiff = None
        text = "**text another bold BOOOLD**`code block`![image](https://i.imgur.com/zjjcJKZ.png)[link](https://boot.dev)"
        expected = [
            TextNode("text another bold BOOOLD", text_type_bold),
            TextNode("code block", text_type_code),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(expected, text_to_textnodes(text))

    if __name__ == "__main__":
        unittest.main()
