from enum import Enum
from .leaf_node import LeafNode


class TextType(Enum):
    PLAIN = "text"
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_note_to_html_node(text_node: TextNode):

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise Exception("Text node is not an existing type")


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str | None,
    text_type: TextType = TextType.TEXT,
) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        # Node is already not a text node
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_nodes: list[str] = node.text.split(delimiter, 2)

            if len(split_nodes) < 3:
                raise Exception("Invalid markdown - Closing Delimiter not found")

            my_nodes = [
                TextNode(split_nodes[0], TextType.TEXT),
                TextNode(split_nodes[1], text_type),
                TextNode(split_nodes[2], TextType.TEXT),
            ]

            new_nodes.extend(my_nodes)

    return new_nodes
