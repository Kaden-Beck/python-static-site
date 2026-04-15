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
    # Headings (1-6 '#' followed by a space)
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    # Code Block (Starts and end with "```" followed by a newline)
    if block[0:4] == "```\n" and block[-3:] == "```":
        return BlockType.CODE

    # If neither of the above, split block into lines
    lines = block.split("\n")
    # Check that each line in the block matches a pattern and use short-circuit to return  proper BlockType
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    if all(re.match(r"^\d+\. ", line) for line in lines):
        return BlockType.ORDERED_LIST

    # Else its a just paragraph block
    return BlockType.PARAGRAPH


def get_heading_level(p_block: str) -> int:
    level = 0
    for char in p_block:
        if char == " ":
            return level
        elif char == "#":
            level += 1
        else:
            raise Exception(f"Error parsing heading:\n{p_block}")
