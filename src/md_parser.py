from src.block import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
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
    block_nodes: list[HTMLNode] = []
    for block in markdown_to_blocks(markdown):
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                block_nodes.append(paragraph_block_to_html(block))
            case BlockType.HEADING:
                block_nodes.append(heading_block_to_html(block))
            case BlockType.CODE:
                block_nodes.append(code_block_to_html(block))
            case BlockType.QUOTE:
                block_nodes.append(quote_block_to_html(block))
            case BlockType.UNORDERED_LIST:
                children = text_to_children(block)
                pass
            case BlockType.ORDERED_LIST:
                children = text_to_children(block)
                pass
            case _:
                raise ValueError("Invalid block type was passed")

    return ParentNode("div", block_nodes)


def paragraph_block_to_html(p_block: str) -> HTMLNode:
    children = text_to_children(p_block)

    if children:
        return ParentNode(tag="p", children=children)
    else:
        return LeafNode(tag="p", value=p_block)


def heading_block_to_html(h_block: str) -> HTMLNode:
    level = 0
    for char in h_block:
        if char == " ":
            break
        elif char == "#":
            level += 1

    content = h_block[level + 1 :]
    children = text_to_children(content)

    if children:
        return ParentNode(tag=f"h{level}", children=children)
    else:
        return LeafNode(tag=f"h{level}", value=content)


def code_block_to_html(c_block: str) -> LeafNode:
    # Remove the first and last lines, retaining white space characters before appending
    return LeafNode(tag="code", value="".join(c_block.splitlines(keepends=True)[1:-1]))


def quote_block_to_html(q_block: str) -> HTMLNode:

    new_lines: list[str] = []
    for line in q_block.splitlines():
        new_line = line[2:] if len(line) > 1 and line[1] == " " else line[1:]
        new_lines.append(new_line)

    content = "\n".join(new_lines)
    children = text_to_children(content)

    if children:
        return ParentNode(tag="blockquote", children=children)
    else:
        return LeafNode(tag="blockquote", value=content)
