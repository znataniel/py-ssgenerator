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
from markdown_parsing import split_nodes_delimiter


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
