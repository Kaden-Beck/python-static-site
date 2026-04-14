import unittest

from src.leaf_node import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_with_tag(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), "<p>This is a paragraph of text.</p>")

    def test_to_html_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )

    def test_to_html_without_tag_returns_raw_text(self):
        node = LeafNode(None, "Raw text")
        self.assertEqual(node.to_html(), "Raw text")

    def test_to_html_requires_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_repr_does_not_include_children(self):
        node = LeafNode("p", "Hello", {"class": "intro"})
        self.assertEqual(repr(node), '<p class="intro">Hello</p>')


if __name__ == "__main__":
    unittest.main()
