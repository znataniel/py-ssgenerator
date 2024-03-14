import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_1nested(self):
        node = ParentNode(
            "p",
            [LeafNode("b", "Bold"), ParentNode("div", [LeafNode("p", "Inner para")])],
        )
        self.assertEqual(
            node.to_html(), "<p><b>Bold</b><div><p>Inner para</p></div></p>"
        )

    def test_to_html_2nested_with_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold"),
                ParentNode(
                    "div",
                    [
                        LeafNode("p", "Inner para"),
                        ParentNode(
                            "div",
                            [LeafNode("i", "italic", {"id": "ita"})],
                            {"id": "itaParent"},
                        ),
                    ],
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<p><b>Bold</b><div><p>Inner para</p><div id="itaParent"><i id="ita">italic</i></div></div></p>',
        )

    def test_to_html_no_tag1(self):
        node = ParentNode(
            None,
            [LeafNode("b", "Bold"), ParentNode("div", [LeafNode("p", "Inner para")])],
        )
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_tag2(self):
        node = ParentNode(
            "p",
            [LeafNode("b", "Bold"), ParentNode("", [LeafNode("p", "Inner para")])],
        )
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_children1(self):
        node = ParentNode(
            "p",
            [LeafNode("b", "Bold"), ParentNode("", [])],
        )
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_children2(self):
        node = ParentNode(
            "p",
            None,
        )
        self.assertRaises(ValueError, node.to_html)

    if __name__ == "__main__":
        unittest.main()
