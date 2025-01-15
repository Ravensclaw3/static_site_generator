from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    NORMAL_TEXT = "Normal text"
    BOLD_TEXT = "Bold text"
    ITALIC_TEXT = "Italic text"
    CODE_TEXT = "Code text"
    LINKS = "Links"
    IMAGES = "Images"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type 
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode('{self.text}', '{self.text_type.value}', '{self.url}')"


def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case (TextType.NORMAL_TEXT):
            return LeafNode(None, text_node.text)
        case (TextType.BOLD_TEXT):
            return LeafNode("b", text_node.text)
        case (TextType.ITALIC_TEXT):
            return LeafNode("i", text_node.text)
        case (TextType.CODE_TEXT):
            return LeafNode("code", text_node.text)
        case (TextType.LINKS):
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case (TextType.IMAGES):
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i, section in enumerate(sections):
            if section == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(section, TextType.NORMAL_TEXT))
            else:
                split_nodes.append(TextNode(section, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes