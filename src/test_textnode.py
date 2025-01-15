import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq_bold(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_eq_normal(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a text node", TextType.NORMAL_TEXT)
        self.assertEqual(node, node2)

    def test_eq_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertEqual(node, node2)

    def test_eq_link(self):
        node = TextNode("This is a text node", TextType.LINKS, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINKS, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_text_type(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.LINKS, "http://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINKS, "https://www.boot.dev")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(repr(node), "TextNode('This is a text node', 'Bold text', 'None')")

class TestMain(unittest.TestCase):
    def test_normal(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        result = text_node_to_html_node(node).to_html()
        expect = "This is a text node"
        self.assertEqual(expect, result)

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        result = text_node_to_html_node(node).to_html()
        expect = "<b>This is a text node</b>"
        self.assertEqual(expect, result)

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC_TEXT)
        result = text_node_to_html_node(node).to_html()
        expect = "<i>This is a text node</i>"
        self.assertEqual(expect, result)

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE_TEXT)
        result = text_node_to_html_node(node).to_html()
        expect = "<code>This is a code node</code>"
        self.assertEqual(expect, result)

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINKS, "https://www.google.com")
        result = text_node_to_html_node(node).to_html()
        expect = "<a href=\"https://www.google.com\">This is a link node</a>"
        self.assertEqual(expect, result)

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGES, "url/of/image.jpg")
        result = text_node_to_html_node(node)
        self.assertEqual(result.tag, "img")
        self.assertEqual(result.value, "")
        self.assertEqual(
            result.props,
            {"src": "url/of/image.jpg", "alt": "This is an image node"},
        )

if __name__ == "__main__":
    unittest.main()
