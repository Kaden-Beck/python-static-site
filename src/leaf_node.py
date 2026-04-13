from html_node import HTMLNode


# Leaf nodes cannot have children, value and tag are required, props is optional
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f'<{self.tag or "no tag"}{self.props_to_html()}>{self.value or "no value"}</{self.tag or "no tag"}>'
