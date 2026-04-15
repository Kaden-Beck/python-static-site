from src.block import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    get_heading_level,
)
from src.html_node import HTMLNode, ParentNode, LeafNode
from src.inline import text_to_textnodes
from src.textnode import text_node_to_html_node


def text_to_children(block: str) -> list[HTMLNode]:

    html_nodes: list[HTMLNode] = []

    for text_node in text_to_textnodes(block):
        html_nodes.append(text_node_to_html_node(text_node))

    if len(html_nodes) > 1:
        return html_nodes
    else:
        return None


def markdown_to_html_node(markdown: str) -> HTMLNode:
    # 2) For each block:
    #   - Based on block type, create a new HTMLNode
    #   - Parse (TextNode -> HTMLNode) and assign child HTML Nodes (recursive) to block (Create a text_to_children(str) -> list[HTMLNode])
    #   - For the code block : no inline parsing for children
    # 3) Add each of these parent HTMLNodes with children to one singular parent node which is a <div> element
    # 4) Add Unit Tests

    # Split up blocks and iterate through each block
    html_blocks: list[HTMLNode] = []
    for block in markdown_to_blocks(markdown):
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                children = text_to_children(block)

                if children:
                    html_blocks.append(ParentNode(tag="p", children=children))
                else:
                    html_blocks.append(LeafNode(tag="p", value=block))
            case BlockType.HEADING:
                h_level = get_heading_level(block)

                content = block[h_level + 1 :]
                children = text_to_children(content)

                if children:
                    html_blocks.append(ParentNode(tag=f"h{h_level}", children=children))
                else:
                    html_blocks.append(LeafNode(tag=f"h{h_level}", value=content))
            case BlockType.CODE:
                pass
            case BlockType.QUOTE:
                children = text_to_children(block)
                pass
            case BlockType.UNORDERED_LIST:
                children = text_to_children(block)
                pass
            case BlockType.ORDERED_LIST:
                children = text_to_children(block)
                pass
            case _:
                raise ValueError("Invalid block type was passed")

    return ParentNode("div", html_blocks)
