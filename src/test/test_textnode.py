import unittest

from src.textnode import (
    TextNode,
    TextType,
    text_note_to_html_node,
)




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


class TestTextNodeParsing(unittest.TestCase):

    # Plain text node should return plain text
    def test_plain_text(self):
        node = TextNode("This is the sample text", TextType.TEXT)
        html = text_note_to_html_node(node).to_html()
        self.assertEqual(html, "This is the sample text")

    # Text Node -> Bold HTML
    def test_bold_html(self):
        self.assertEqual(
            "<b>This is a bold element</b>",
            text_note_to_html_node(
                TextNode("This is a bold element", TextType.BOLD)
            ).to_html(),
        )

    # Text Node -> Italic HTML
    def test_italic_html(self):
        self.assertEqual(
            "<i>This is an italic element</i>",
            text_note_to_html_node(
                TextNode("This is an italic element", TextType.ITALIC)
            ).to_html(),
        )

    # Text Node -> Code HTML
    def test_code_html(self):
        self.assertEqual(
            "<code>This is a code element</code>",
            text_note_to_html_node(
                TextNode("This is a code element", TextType.CODE)
            ).to_html(),
        )

    # Text Node -> Link HTML
    def test_link_html(self):
        self.assertEqual(
            '<a href="https://www.google.com">This is a Link element</a>',
            text_note_to_html_node(
                TextNode(
                    "This is a Link element", TextType.LINK, "https://www.google.com"
                )
            ).to_html(),
        )

    # Text Node -> Image HTML
    def test_image_html(self):
        self.assertEqual(
            '<img src="https://www.google.com" alt="Alt Text"></img>',
            text_note_to_html_node(
                TextNode("Alt Text", TextType.IMAGE, "https://www.google.com")
            ).to_html(),
        )

    # Pass an incorrect text type
    def test_bad_text_type(self):
        with self.assertRaises(Exception):
            text_note_to_html_node(TextNode("Not a real type", TextType.URL))




if __name__ == "__main__":
    unittest.main()
