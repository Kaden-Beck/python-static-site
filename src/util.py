import re

from src.textnode import TextNode, TextType


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
            match delimiter:
                case "**":
                    type = TextType.BOLD
                case "_":
                    type = TextType.ITALIC
                case "`":
                    type = TextType.CODE
                case _:
                    raise ValueError("Delimiter not in accepted delimiters")

            split: list[str] = node.text.split(delimiter, 2)

            if len(split) < 3:
                raise Exception("Invalid markdown - Closing Delimiter not found")

            my_nodes = [
                TextNode(split[0], TextType.TEXT),
                TextNode(split[1], type),
                TextNode(split[2], TextType.TEXT),
            ]

            new_nodes.extend(my_nodes)

    return new_nodes


def extract_markdown_images(text: str):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
