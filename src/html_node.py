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


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent node requires a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Parent nodes must have children")

        children_html = ""

        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"


# Leaf nodes cannot have children, value and tag are required, props is optional
class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f'<{self.tag or "no tag"}{self.props_to_html()}>{self.value or "no value"}</{self.tag or "no tag"}>'
