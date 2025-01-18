import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        self.assertRaises(NotImplementedError, HTMLNode().to_html)

    def props_to_html(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        expect = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(expect, node.props_to_html())

    def test_repr(self):
        node = HTMLNode("p", "Test HTML node.", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(repr(node), "HTMLNode('p', 'Test HTML node.', 'None', '{'href': 'https://www.google.com', 'target': '_blank'}')")


class TestLeafNode(unittest.TestCase):
    def test_to_html_error(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()

    def test_to_html_no_props(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expect = '<p>This is a paragraph of text.</p>'
        self.assertEqual(expect, node.to_html())

    def test_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expect = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(expect, node.to_html())

    def test_to_html_no_children(self):
        node = LeafNode("p", "Hello, world!")
        expect = "<p>Hello, world!</p>"
        self.assertEqual(expect, node.to_html())

    def test_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        expect = "Hello, world!"
        self.assertEqual(expect, node.to_html())

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)
        expect = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(expect, node.to_html())

    def test_to_html_children(self):
        node = ParentNode(
    "div",
    [
        ParentNode("p", [LeafNode("i", "italic text"),]),        
    ],
)
        expect = "<div><p><i>italic text</i></p></div>"
        self.assertEqual(expect, node.to_html())

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()
