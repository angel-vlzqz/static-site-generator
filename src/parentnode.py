from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None):
        # Support positional arguments: ParentNode(tag, [children])
        if children is None and isinstance(value, list):
            children = value
            value = None
        if children is None:
            children = []
        super().__init__(tag, value, children, props) # tag and children are NOT optional

    def to_html(self):
        if self.tag is None:
            raise ValueError('missing tag for parentnode object')
        if not self.children:
            raise ValueError('missing children for parentnode object')

        # recursively convert children to html
        children_html = ''.join(child.to_html() for child in self.children)
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'
    
    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"
