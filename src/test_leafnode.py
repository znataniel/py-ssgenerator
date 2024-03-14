import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        l_node = LeafNode("p", "This is a para.", {"style": "margin-top: 1rem"})
        expected = '<p style="margin-top: 1rem">This is a para.</p>'
        self.assertEqual(l_node.to_html(), expected)

    def test_to_html_no_props(self):
        l_node = LeafNode("p", "This is a para.")
        expected = "<p>This is a para.</p>"
        self.assertEqual(l_node.to_html(), expected)

    def test_to_html_no_vals(self):
        l_node = LeafNode("p", None)
        self.assertRaises(ValueError, l_node.to_html)

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    if __name__ == "__main__":
        unittest.main()
