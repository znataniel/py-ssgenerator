import unittest

from htmlnode import HTMLNode


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
