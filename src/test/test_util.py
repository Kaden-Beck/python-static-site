import unittest
from src.util import split_nodes_delimiter, split_nodes_image, split_nodes_link, extract_markdown_images, extract_markdown_links, text_to_textnodes
from src.textnode import TextNode, TextType


class TestDelimiter(unittest.TestCase):
    # Delimiter issue
    def test_wrong_delimiter(self):
        with self.assertRaises(ValueError):
            split_nodes_delimiter(
                [TextNode("", TextType.TEXT)],
                delimiter="-",
            )

    # Only one delimiter (not closed)
    def test_missing_delimiter(self):
        with self.assertRaises(Exception):
            split_nodes_delimiter(
                [TextNode("no closing **bold", TextType.TEXT)],
                delimiter="**",
                text_type=TextType.BOLD,
            )

    # Bold
    def test_bold(self):
        nodes = split_nodes_delimiter(
            [TextNode("Hello **world** foo", TextType.TEXT)],
            delimiter="**",
            text_type=TextType.BOLD,
        )
        self.assertEqual(
            nodes,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.BOLD),
                TextNode(" foo", TextType.TEXT),
            ],
        )

    # Italic
    def test_italic(self):
        nodes = split_nodes_delimiter(
            [TextNode("Hello _world_ foo", TextType.TEXT)],
            delimiter="_",
            text_type=TextType.ITALIC,
        )
        self.assertEqual(
            nodes,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.ITALIC),
                TextNode(" foo", TextType.TEXT),
            ],
        )

    # Code
    def test_code(self):
        nodes = split_nodes_delimiter(
            [TextNode("Hello `world` foo", TextType.TEXT)],
            delimiter="`",
            text_type=TextType.CODE,
        )
        self.assertEqual(
            nodes,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("world", TextType.CODE),
                TextNode(" foo", TextType.TEXT),
            ],
        )


class TestImageParser(unittest.TestCase):
    def test_single_image(self):
        result = extract_markdown_images("![alt text](https://example.com/img.png)")
        self.assertEqual(result, [("alt text", "https://example.com/img.png")])

    def test_multiple_images(self):
        result = extract_markdown_images(
            "![first](https://example.com/1.png) and ![second](https://example.com/2.png)"
        )
        self.assertEqual(result, [
            ("first", "https://example.com/1.png"),
            ("second", "https://example.com/2.png"),
        ])

    def test_no_images(self):
        result = extract_markdown_images("just plain text with no images")
        self.assertEqual(result, [])

    def test_does_not_match_links(self):
        result = extract_markdown_images("[not an image](https://example.com)")
        self.assertEqual(result, [])


class TestLinkParser(unittest.TestCase):
    def test_single_link(self):
        result = extract_markdown_links("[click here](https://example.com)")
        self.assertEqual(result, [("click here", "https://example.com")])

    def test_multiple_links(self):
        result = extract_markdown_links(
            "[first](https://example.com/1) and [second](https://example.com/2)"
        )
        self.assertEqual(result, [
            ("first", "https://example.com/1"),
            ("second", "https://example.com/2"),
        ])

    def test_no_links(self):
        result = extract_markdown_links("just plain text with no links")
        self.assertEqual(result, [])

    def test_does_not_match_images(self):
        result = extract_markdown_links("![image](https://example.com/img.png)")
        self.assertEqual(result, [])


class TestSplitNodesImage(unittest.TestCase):
    def test_single_image(self):
        nodes = split_nodes_image(
            [TextNode("before ![alt](https://example.com/img.png) after", TextType.TEXT)]
        )
        self.assertEqual(nodes, [
            TextNode("before ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" after", TextType.TEXT),
        ])

    def test_multiple_images(self):
        nodes = split_nodes_image(
            [TextNode("![one](https://example.com/1.png) and ![two](https://example.com/2.png)", TextType.TEXT)]
        )
        self.assertEqual(nodes, [
            TextNode("one", TextType.IMAGE, "https://example.com/1.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "https://example.com/2.png"),
        ])

    def test_no_images_passthrough(self):
        node = TextNode("just plain text", TextType.TEXT)
        nodes = split_nodes_image([node])
        self.assertEqual(nodes, [node])

    def test_non_text_node_passthrough(self):
        node = TextNode("already bold", TextType.BOLD)
        nodes = split_nodes_image([node])
        self.assertEqual(nodes, [node])


class TestSplitNodesLink(unittest.TestCase):
    def test_single_link(self):
        nodes = split_nodes_link(
            [TextNode("before [click](https://example.com) after", TextType.TEXT)]
        )
        self.assertEqual(nodes, [
            TextNode("before ", TextType.TEXT),
            TextNode("click", TextType.LINK, "https://example.com"),
            TextNode(" after", TextType.TEXT),
        ])

    def test_multiple_links(self):
        nodes = split_nodes_link(
            [TextNode("[first](https://example.com/1) and [second](https://example.com/2)", TextType.TEXT)]
        )
        self.assertEqual(nodes, [
            TextNode("first", TextType.LINK, "https://example.com/1"),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.LINK, "https://example.com/2"),
        ])

    def test_no_links_passthrough(self):
        node = TextNode("just plain text", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(nodes, [node])

    def test_does_not_split_images(self):
        node = TextNode("![img](https://example.com/img.png)", TextType.TEXT)
        nodes = split_nodes_link([node])
        self.assertEqual(nodes, [node])


class TestTextToTextNodes(unittest.TestCase):
    def test_full_example(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])

    def test_plain_text(self):
        nodes = text_to_textnodes("just plain text")
        self.assertEqual(nodes, [TextNode("just plain text", TextType.TEXT)])

    def test_only_bold(self):
        nodes = text_to_textnodes("**bold**")
        self.assertEqual(nodes, [TextNode("bold", TextType.BOLD)])

    def test_only_link(self):
        nodes = text_to_textnodes("[click](https://boot.dev)")
        self.assertEqual(nodes, [TextNode("click", TextType.LINK, "https://boot.dev")])


if __name__ == "__main__":
    unittest.main()
