import unittest

from src.block import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_extra_blank_lines(self):
        md = "first block\n\n\n\nsecond block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["first block", "second block"])

    def test_leading_trailing_whitespace_stripped(self):
        md = "  trimmed block  \n\n  another block  "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["trimmed block", "another block"])

    def test_single_block(self):
        md = "just one block"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["just one block"])

    def test_empty_string(self):
        blocks = markdown_to_blocks("")
        self.assertEqual(blocks, [])


if __name__ == "__main__":
    unittest.main()
