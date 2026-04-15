import unittest

from src.md_parser import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph_with_bold_and_italic(self):
        md = "This is a **test** of _my_ function"
        result = markdown_to_html_node(md)
        self.assertEqual(
            result.to_html(),
            "<div><p>This is a <b>test</b> of <i>my</i> function</p></div>",
        )

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

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quote_plain(self):
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(), "<div><blockquote>This is a quote</blockquote></div>"
        )

    def test_quote_with_inline(self):
        md = "> This is a **bold** quote"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>This is a <b>bold</b> quote</blockquote></div>",
        )

    def test_unordered_list_plain(self):
        md = "- item one\n- item two\n- item three"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>item one</li><li>item two</li><li>item three</li></ul></div>",
        )

    def test_unordered_list_with_inline(self):
        md = "- **bold** item\n- _italic_ item"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li><b>bold</b> item</li><li><i>italic</i> item</li></ul></div>",
        )

    def test_ordered_list_plain(self):
        md = "1. first\n2. second\n3. third"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )

    def test_ordered_list_with_inline(self):
        md = "1. **bold** first\n2. _italic_ second"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li><b>bold</b> first</li><li><i>italic</i> second</li></ol></div>",
        )


if __name__ == "__main__":
    unittest.main()
