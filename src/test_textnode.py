import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    ## Test that two nodes without url are implemented consistently
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    ## Test text type differences
    def test_text_type(self):
        text = "This is a text node"
        bold_node = TextNode(text, TextType.BOLD)
        italic_node = TextNode(text, TextType.ITALIC)
        self.assertNotEqual(bold_node, italic_node)

    ## Test when is passed as url
    def test_none_url(self):
        text = "This is a text node"
        with_none = TextNode(text, TextType.PLAIN, url=None)
        with_omit = TextNode(text, TextType.PLAIN)
        self.assertEqual(with_none, with_omit)

    def test_link_eq(self):
        url = "https://boot.dev"
        text = "boot.dev"
        node = TextNode(text, TextType.LINK, url=url)
        node2 = TextNode(text, TextType.LINK, url=url)
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
