class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # String
        self.value = value  # String
        self.children = children  # [HTMLNode]
        self.props = props  # {prop: value, ...}

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        output = ""

        if self.props is None or len(self.props) == 0:
            return output

        for prop in self.props:
            output += f' {prop}="{self.props[prop]}"'

        return output

    def __repr__(self):
        return f'<{self.tag or "no tag"}{self.props_to_html()}>{self.value or "no value"}</{self.tag or "no tag"}> Children: {self.children or "no children"}'


def markdown_to_html_node(markdown: str) -> HTMLNode:
    # 1) Spilt into blocks
    # 2) For each block:
    #   - Determine BlockType
    #   - Based on block type, create a new HTMLNode
    #   - Parse (TextNode -> HTMLNode) and assign child HTML Nodes (recursive) to block (Create a text_to_children(str) -> list[HTMLNode])
    #   - For the code block : no inline parsing for children
    # 3) Add each of these parent HTMLNodes with children to one singular parent node which is a <div> element
    # 4) Add Unit Tests
    
    
    pass