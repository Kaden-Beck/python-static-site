import unittest

from html_node import HTMLNode


class TestHTMLNode(unittest.TestCase):
    ## Test two nodes with matching params
    def test_eq(self):
        node = HTMLNode("p", "This is a paragraph", None, {"style": "italic"})

        self.assertEqual(
            repr(node),
            f'<p style="italic">This is a paragraph</p> Children: no children',
        )

    ## Test no args passed
    def test_no_args(self):
        node = HTMLNode()
        self.assertEqual(repr(node), f"<no tag>no value</no tag> Children: no children")

    ## Test `None` args passed
    def test_none_args(self):
        node = HTMLNode(None)
        self.assertEqual(repr(node), "<no tag>no value</no tag> Children: no children")
