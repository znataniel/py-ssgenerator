import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html1(self):
        hnode_1 = HTMLNode(
            "a", "GNU Webpage", None, {"href": "gnu.org", "target": "_blank"}
        )
        hnode_1_expected = ' href="gnu.org" target="_blank"'
        self.assertEqual(hnode_1.props_to_html(), hnode_1_expected)

    def test_props_to_html2(self):
        hnode_2 = HTMLNode(
            "img",
            None,
            None,
            {"href": "https://boot.dev/bootspic.png", "alt": "Cute Picture of Boots."},
        )
        hnode_2_expected = (
            ' href="https://boot.dev/bootspic.png" alt="Cute Picture of Boots."'
        )
        self.assertEqual(hnode_2.props_to_html(), hnode_2_expected)

    def test_to_html_exc(self):
        hnode_1 = HTMLNode(
            "a", "GNU Webpage", None, {"href": "gnu.org", "target": "_blank"}
        )
        self.assertRaises(NotImplementedError, hnode_1.to_html)

    if __name__ == "__main__":
        unittest.main()


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
