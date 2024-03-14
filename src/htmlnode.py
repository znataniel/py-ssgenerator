class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        str_props = ""
        if self.props is None:
            return str_props
        for prop in self.props:
            str_props += f' {prop}="{self.props[prop]}"'
        return str_props

    def __repr__(self):
        children_str = ""
        if self.children is not None:
            for child in self.children:
                children_str += f"{child.tag}+"
            children_str = children_str[:-1]
        else:
            children_str = self.children
        return f"HTMLNode\ntag: {self.tag}\nvalue: {self.value}\nchildren:{children_str}\nprops: {self.props_to_html()}"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError()
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("HTML tag not provided")
        if self.children is None:
            raise ValueError("Element has no children")
        # if self.children is None or not len(self.children):
        #     raise ValueError("Element has no children")
        children_str = ""
        for child in self.children:
            children_str += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_str}</{self.tag}>"
