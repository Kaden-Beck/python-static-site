import unittest
from src.util import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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


if __name__ == "__main__":
    unittest.main()
