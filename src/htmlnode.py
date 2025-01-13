class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(list(map(lambda x:f" {x[0]}=\"{str(x[1])}\"" , self.props.items())))

    def __repr__(self):
        return f"HTMLNode('{self.tag}', '{self.value}', '{self.children}', '{self.props}')"
