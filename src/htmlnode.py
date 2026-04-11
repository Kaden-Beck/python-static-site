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

        if self.props == None or len(self.props) == 0:
            return output
        
        for prop in self.props:
            output += f" {prop}={self.props[prop]}"
        
        return output
    

    def __repr__(self):
        return f"<{self.tag or "no tag"}{self.props_to_html()}>{self.value or "no value"}</{self.tag or "no tag"}> Children: {self.children or "no children"}"