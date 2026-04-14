import re
from typing import NamedTuple
from src.textnode import TextNode, TextType


class ImageTuple(NamedTuple):
    alt: str
    url: str


class LinkTuple(NamedTuple):
    text: str
    url: str


def extract_markdown_images(text: str) -> list[ImageTuple]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[LinkTuple]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


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

            if len(split) == 1:
                new_nodes.append(node)
                continue

            if len(split) < 3:
                raise Exception("Invalid markdown - Closing Delimiter not found")

            if split[0]:
                new_nodes.append(TextNode(split[0], TextType.TEXT))
            new_nodes.append(TextNode(split[1], type))
            if split[2]:
                new_nodes.append(TextNode(split[2], TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        remaining = node.text
        for image in images:
            sections = remaining.split(f"![{image[0]}]({image[1]})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            remaining = sections[1]

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        # Get links from string
        links = extract_markdown_links(node.text)
        # Check if there were links
        if len(links) == 0:
            new_nodes.append(node)
            continue

        remaining = node.text
        for link in links:
            sections = remaining.split(f"[{link[0]}]({link[1]})", 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            remaining = sections[1]

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]

    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(nodes, "**", TextType.BOLD),
                    "_",
                    TextType.ITALIC,
                ),
                "`",
                TextType.CODE,
            )
        )
    )
