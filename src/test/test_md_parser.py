import unittest

from src.md_parser import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph_with_bold_and_italic(self):
        md = "This is a **test** of _my_ function"
        result = markdown_to_html_node(md)
        self.assertEqual(result.to_html(), "<div><p>This is a <b>test</b> of <i>my</i> function</p></div>")

    def test_h1_plain(self):
        md = "# TEST"
        result = markdown_to_html_node(md)
        self.assertEqual(result.to_html(), "<div><h1>TEST</h1></div>")

    def test_h2_with_bold(self):
        md = "## This is a **test**"
        result = markdown_to_html_node(md)
        self.assertEqual(result.to_html(), "<div><h2>This is a <b>test</b></h2></div>")

    def test_combined(self):
        md = "# TEST\n\nThis is a **test** of _my_ function\n\n## This is a **test**"
        result = markdown_to_html_node(md)
        self.assertEqual(
            result.to_html(),
            "<div><h1>TEST</h1><p>This is a <b>test</b> of <i>my</i> function</p><h2>This is a <b>test</b></h2></div>",
        )


if __name__ == "__main__":
    unittest.main()
