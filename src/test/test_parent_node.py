import unittest

from src.leaf_node import LeafNode
from src.parent_node import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_renders_children(self):
        child = LeafNode("p", "This is a paragraph of text.")
        node = ParentNode("div", [child])
        self.assertEqual(
            node.to_html(), "<div><p>This is a paragraph of text.</p></div>"
        )

    def test_to_html_renders_multiple_children(self):
        child_one = LeafNode("b", "Bold")
        child_two = LeafNode(None, " and raw text")
        node = ParentNode("p", [child_one, child_two])
        self.assertEqual(node.to_html(), "<p><b>Bold</b> and raw text</p>")

    def test_to_html_includes_props(self):
        child = LeafNode("span", "Text")
        node = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(
            node.to_html(),
            '<div class="container"><span>Text</span></div>',
        )

    def test_to_html_requires_tag(self):
        node = ParentNode(None, [LeafNode("span", "Text")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_requires_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_requires_non_empty_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
