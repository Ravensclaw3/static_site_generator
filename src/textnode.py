import re

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


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    #pattern = r"!\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    #pattern = r"\[(.*?)\]\((.*?)\)"
    matches = re.findall(pattern, text)
    return matches


#def split_nodes_image(old_nodes):
#    new_nodes = []
#    for old_node in old_nodes:
#        image_nodes = extract_markdown_images(old_node.text)
#        if len(image_nodes) == 0:
#            continue
#        image = image_nodes[0]
#        sections = old_node.text.split(f"![{image[0]}]({image[1]})", 1)
#        new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
#        new_nodes.append(TextNode(image[0], TextType.IMAGES, image[1]))
#        new_nodes.extend(split_nodes_image([TextNode(sections[1], TextType.NORMAL_TEXT)]))
#    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGES,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL_TEXT))
    return new_nodes


#def split_nodes_link(old_nodes):
#    new_nodes = []
#    for old_node in old_nodes:
#        link_nodes = extract_markdown_links(old_node.text)
#        if len(link_nodes) == 0:
#            continue
#        link = link_nodes[0]
#        sections = old_node.text.split(f"[{link[0]}]({link[1]})", 1)
#        new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
#        new_nodes.append(TextNode(link[0], TextType.LINKS, link[1]))
#        new_nodes.extend(split_nodes_link([TextNode(sections[1], TextType.NORMAL_TEXT)]))
#    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL_TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL_TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINKS, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL_TEXT))
    return new_nodes


def text_to_textnodes(text):
    textNode = [TextNode(text, TextType.NORMAL_TEXT)]
    boldnodes = split_nodes_delimiter(textNode, "**", TextType.BOLD_TEXT)
    italicnodes = split_nodes_delimiter(boldnodes, "*", TextType.ITALIC_TEXT)
    codenodes = split_nodes_delimiter(italicnodes, "`", TextType.CODE_TEXT)
    imagenodes = split_nodes_image(codenodes)
    linknodes = split_nodes_link(imagenodes)
    return linknodes
