import re
from enum import Enum


def markdown_to_blocks(markdown: str) -> list[str]:
    return list(filter(lambda a: a, map(lambda a: a.strip(), markdown.split("\n\n"))))


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    # headings
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    # Code Block
    if block[0:4] == "```\n" and block[-3:] == "```":
        return BlockType.CODE

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(re.match(r"^\d+\. ", line) for line in lines):
        return BlockType.ORDERED_LIST

    # Else its a paragraph
    return BlockType.PARAGRAPH
