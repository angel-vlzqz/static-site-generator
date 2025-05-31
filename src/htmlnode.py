class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag           # string tag, like p, a, h1
        self.value = value       # string value, text inside a paragraph
        self.children = children # list of HTMLNode objects
        self.props = props       # don't know if i should use .copy() here

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if not self.props:
            return ''
        res = ''
        for prop in self.props:
            res += f' {prop}="{self.props[prop]}"'
        return res

    def __repr__(self):
        return f'HTMLNode: tag={self.tag}, value={self.value}, children={self.children}, props={self.props}'

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )