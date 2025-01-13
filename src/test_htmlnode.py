import unittest

from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()
